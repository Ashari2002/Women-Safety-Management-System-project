import mysql.connector
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Database connection configuration
db_config = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'user': os.getenv('DB_USER', 'root'),
    'password': os.getenv('DB_PASSWORD', ''),
}

# Database and tables creation
def init_db():
    # Connect to MySQL server
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    
    # Create database if not exists
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {os.getenv('DB_NAME', 'women_safety_db')}")
    cursor.execute(f"USE {os.getenv('DB_NAME', 'women_safety_db')}")
    
    # Create users table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(100) NOT NULL,
        email VARCHAR(100) NOT NULL UNIQUE,
        password VARCHAR(255) NOT NULL,
        phone VARCHAR(15) NOT NULL,
        address TEXT,
        latitude DECIMAL(10, 8),
        longitude DECIMAL(11, 8),
        role ENUM('user', 'admin', 'police') NOT NULL DEFAULT 'user',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
    )
    ''')
    
    # Create emergency_contacts table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS emergency_contacts (
        id INT AUTO_INCREMENT PRIMARY KEY,
        user_id INT NOT NULL,
        name VARCHAR(100) NOT NULL,
        phone VARCHAR(15) NOT NULL,
        relationship VARCHAR(50),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
    )
    ''')
    
    # Create police_stations table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS police_stations (
        id INT AUTO_INCREMENT PRIMARY KEY,
        station_name VARCHAR(100) NOT NULL,
        address TEXT NOT NULL,
        phone VARCHAR(15) NOT NULL,
        email VARCHAR(100) NOT NULL UNIQUE,
        password VARCHAR(255) NOT NULL,
        latitude DECIMAL(10, 8) NOT NULL,
        longitude DECIMAL(11, 8) NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
    )
    ''')
    
    # Create sos_alerts table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS sos_alerts (
        id INT AUTO_INCREMENT PRIMARY KEY,
        user_id INT NOT NULL,
        police_station_id INT NOT NULL,
        latitude DECIMAL(10, 8) NOT NULL,
        longitude DECIMAL(11, 8) NOT NULL,
        message TEXT,
        status ENUM('pending', 'resolved', 'rejected', 'fraud') DEFAULT 'pending',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
        FOREIGN KEY (police_station_id) REFERENCES police_stations(id) ON DELETE CASCADE
    )
    ''')
    
    # Create admin user if not exists
    cursor.execute("SELECT * FROM users WHERE email = 'admin@example.com'")
    admin_exists = cursor.fetchone()
    
    if not admin_exists:
        # Store raw password
        admin_password = 'admin123'
        
        # Insert admin user
        cursor.execute('''
        INSERT INTO users (name, email, password, phone, role)
        VALUES (%s, %s, %s, %s, %s)
        ''', ('Admin User', 'admin@example.com', admin_password, '1234567890', 'admin'))
    
    # Create sample police stations
    cursor.execute("SELECT COUNT(*) FROM police_stations")
    station_count = cursor.fetchone()[0]
    
    if station_count == 0:
        police_stations = [
            ('Central Police Station', '123 Main St, City Center', '9876543210', 'central@police.gov', 'police123', 37.7749, -122.4194),
            ('North Police Station', '456 North Ave, North District', '9876543211', 'north@police.gov', 'police123', 37.8044, -122.4194),
            ('South Police Station', '789 South Blvd, South District', '9876543212', 'south@police.gov', 'police123', 37.7449, -122.4194),
            ('East Police Station', '101 East Rd, East District', '9876543213', 'east@police.gov', 'police123', 37.7749, -122.3894),
            ('West Police Station', '202 West St, West District', '9876543214', 'west@police.gov', 'police123', 37.7749, -122.4494)
        ]
        
        for station in police_stations:
            cursor.execute('''
            INSERT INTO police_stations (station_name, address, phone, email, password, latitude, longitude)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            ''', station)
    
    # Commit changes and close connection
    conn.commit()
    cursor.close()
    conn.close()
    
    print("Database initialized successfully!")

if __name__ == "__main__":
    init_db() 