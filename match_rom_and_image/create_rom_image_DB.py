import os
import sqlite3
from pathlib import Path

# Define the directory you want to scan
directory_to_scan = '/media/pi/INTENSO/emulators_ROM_EXTRA/roms/mastersystems'
#----------------------------
# Define the SQLite database file
database_file = 'ROM_IMAGE.db'

# Connect to SQLite database. It will be created if it doesn't exist.
conn = sqlite3.connect(database_file)
cursor = conn.cursor()

# Create table if it doesn't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS ROMS
    (id INTEGER PRIMARY KEY AUTOINCREMENT, 
     file_path TEXT, 
     file_name TEXT, 
     file_size INTEGER)
''')
# Create table if it doesn't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS IMAGES
    (id INTEGER PRIMARY KEY AUTOINCREMENT, 
     file_path TEXT, 
     file_name TEXT, 
     file_size INTEGER)
''')
#----------------------------
def scan_directory(directory):
    file_info_list = []
    for entry in os.scandir(directory):
        if entry.is_file():
            file_path = entry.path
            file_name = entry.name
            file_size = entry.stat().st_size
            file_info_list.append((file_path, file_name, file_size))
            print(f"Found file: {file_path}")
        elif entry.is_dir():
            file_info_list.extend(scan_directory(entry.path))
    return file_info_list
#----------------------------
def upload_to_roms(file_info_list):
    try:
        cursor.executemany('''
            INSERT INTO roms (file_path, file_name, file_size)
            VALUES (?, ?, ?)
        ''', file_info_list)
        conn.commit()
        print(f"Uploaded {len(file_info_list)} files to database.")
    except sqlite3.Error as e:
        print(f"Error uploading to database: {e}")
#----------------------------
def upload_to_images(file_info_list):
    try:
        cursor.executemany('''
            INSERT INTO images (file_path, file_name, file_size)
            VALUES (?, ?, ?)
        ''', file_info_list)
        conn.commit()
        print(f"Uploaded {len(file_info_list)} files to database.")
    except sqlite3.Error as e:
        print(f"Error uploading to database: {e}")
#----------------------------
def main():
    directory_to_scan1 = '/media/pi/INTENSO/emulators_ROM_EXTRA/roms/mastersystems'

    file_info_list = scan_directory(directory_to_scan1)
    upload_to_roms(file_info_list)
    

    directory_to_scan2 = '/media/pi/INTENSO/emulators_ROM_EXTRA/downloaded_images/mastersystem'
    file_info_list = scan_directory(directory_to_scan2)
    upload_to_images(file_info_list)
    conn.close()

if __name__ == "__main__":
    main()

