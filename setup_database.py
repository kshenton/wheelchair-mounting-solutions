import sqlite3
import csv
import os

def create_tables(conn):
    cursor = conn.cursor()
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS wheelchairs (
        id INTEGER PRIMARY KEY,
        model TEXT,
        frame_clamps TEXT,
        location TEXT
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS aac_devices (
        id INTEGER PRIMARY KEY,
        name TEXT,
        weight REAL
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS mounts (
        id INTEGER PRIMARY KEY,
        name TEXT,
        weight_capacity REAL
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS product_urls (
        id INTEGER PRIMARY KEY,
        product_name TEXT,
        url TEXT
    )
    ''')

    conn.commit()

def import_csv_to_table(conn, csv_file, table_name):
    cursor = conn.cursor()
    
    with open(csv_file, 'r', encoding='utf-8-sig') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            placeholders = ', '.join(['?' for _ in row])
            columns = ', '.join(row.keys())
            sql = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
            cursor.execute(sql, tuple(row.values()))
    
    conn.commit()

def main():
    db_path = 'mounting_solutions.db'
    conn = sqlite3.connect(db_path)
    
    create_tables(conn)
    
    csv_files = {
        'wheelchairs': 'wheelchairs.csv',
        'aac_devices': 'aac_devices.csv',
        'mounts': 'mounts.csv',
        'product_urls': 'product_urls.csv'
    }
    
    for table, csv_file in csv_files.items():
        import_csv_to_table(conn, csv_file, table)
    
    conn.close()
    print("Database setup complete.")

if __name__ == "__main__":
    main()