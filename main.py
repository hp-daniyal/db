import sqlite3
from sqlite3 import Error

def create_connection(db_file):
    """Create a database connection to a SQLite database."""
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(f"SQLite Database connected. SQLite version: {sqlite3.version}")
    except Error as e:
        print(e)
    return conn

def create_tables(conn):
    """Create tables for the snapp database."""
    try:
        cursor = conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS Users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            phone TEXT,
            password TEXT NOT NULL,
            registered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS Drivers (
            driver_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            phone TEXT,
            password TEXT NOT NULL,
            license_number TEXT UNIQUE NOT NULL,
            vehicle_id INTEGER,
            rating REAL DEFAULT 0,
            registered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (vehicle_id) REFERENCES Vehicles(vehicle_id)
        );
        """)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS Vehicles (
            vehicle_id INTEGER PRIMARY KEY AUTOINCREMENT,
            driver_id INTEGER UNIQUE NOT NULL,
            make TEXT NOT NULL,
            model TEXT NOT NULL,
            year INTEGER,
            license_plate TEXT UNIQUE NOT NULL,
            color TEXT,
            capacity INTEGER DEFAULT 4,
            FOREIGN KEY (driver_id) REFERENCES Drivers(driver_id)
        );
        """)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS Rides (
            ride_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            driver_id INTEGER NOT NULL,
            origin TEXT NOT NULL,
            destination TEXT NOT NULL,
            distance REAL,
            duration INTEGER,
            fare REAL,
            status TEXT DEFAULT 'requested',
            requested_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            completed_at TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES Users(user_id),
            FOREIGN KEY (driver_id) REFERENCES Drivers(driver_id)
        );
        """)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS Payments (
            payment_id INTEGER PRIMARY KEY AUTOINCREMENT,
            ride_id INTEGER NOT NULL,
            amount REAL NOT NULL,
            payment_method TEXT,
            payment_status TEXT DEFAULT 'pending',
            paid_at TIMESTAMP,
            FOREIGN KEY (ride_id) REFERENCES Rides(ride_id)
        );
        """)

        conn.commit()
        print("All tables created successfully.")
    except Error as e:
        print(f"Error creating tables: {e}")

def list_tables(conn):
    """List all tables in the database."""
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        print("Tables in the database:")
        for table in tables:
            print(table[0])
    except Error as e:
        print(f"Error listing tables: {e}")

def insert_sample_data(conn):
    """Insert sample data into Users and Drivers tables."""
    try:
        cursor = conn.cursor()
        cursor.execute("""
        INSERT INTO Users (name, email, phone, password)
        VALUES (?, ?, ?, ?);
        """, ("ali abbasi", "aliabbasi@example.com", "0918545565", "securepassword"))

        cursor.execute("""
        INSERT INTO Drivers (name, email, phone, password, license_number)
        VALUES (?, ?, ?, ?, ?);
        """, ("majid salami", "salamimajid@example.com", "0913876543", "driverpassword", "5568i75"))

        cursor.execute("""
        INSERT INTO Vehicles (driver_id, make, model, year, license_plate, color, capacity)
        VALUES (?, ?, ?, ?, ?, ?, ?);
        """, (1, "Pride", "Saipa", 2020, "57z767_66", "Blue", 4))

        conn.commit()
        print("Sample data inserted successfully.")
    except Error as e:
        print(f"Error inserting sample data: {e}")

def close_connection(conn):
    """Close the database connection."""
    if conn:
        conn.close()
        print("Database connection closed.")

def main():
    database = "snapp.db"
    conn = create_connection(database)

    if conn is not None:
        create_tables(conn)
        list_tables(conn)
        insert_sample_data(conn)
        close_connection(conn)
    else:
        print("Error! Cannot create the database connection.")

if __name__ == '__main__':
    main()