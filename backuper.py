#    mysqldump -P [port] -h [host] -u [user] -p [password] [db_name] | gzip > db_backup.sql.gz

import subprocess
import json
import os
from glob import glob
from datetime import datetime

def main():
    print("Starting database backup process...")
    with open('access.json', 'r') as f:
        access_info = json.load(f)
    for db in access_info:
        port = db['port']
        host = db['host']
        user = db['user']
        password = db['password']
        db_name = db['db_name']
        number_of_backups = db.get('number_of_backups', 3)

        try:
            backup_database(port, host, user, password, db_name)
            prune_backup_files(db_name, number_of_backups)
        except Exception as e:
            print(f"Error backing up {db_name}: {e}")

def prune_backup_files(db_name, number_of_backups):
    """
    Prune old backup files, keeping only the most recent ones.

    :param db_name: Name of the database
    :param number_of_backups: Number of backups to keep
    """
    backup_file_pattern = f"{db_name}_*.sql.gz"

    # List all matching backup files
    files = sorted(glob(backup_file_pattern))

    # Remove old backups if they exceed the limit
    while len(files) > number_of_backups:
        file_to_remove = files.pop(0)
        print(f"Removing old backup file: {file_to_remove}")
        os.remove(file_to_remove)

def backup_database(port, host, user, password, db_name):
    """
    Back up a MySQL database using mysqldump and gzip.

    :param port: MySQL port number
    :param host: MySQL server IP address
    :param user: MySQL username
    :param password: MySQL password
    :param db_name: Name of the database to back up
    """
    command = [
        'mysqldump',
        '-P', str(port),
        '-h', host,
        '-u', user,
        f'--password={password}',
        db_name
    ]

    datestamp = datetime.today().strftime('%Y-%m-%d')
    backup_file = f"{db_name}_{datestamp}.sql.gz"

    with open(backup_file, 'wb') as f:
        process = subprocess.Popen(command, stdout=subprocess.PIPE)
        gzip_process = subprocess.Popen(['gzip'], stdin=process.stdout, stdout=f)
        process.stdout.close()  # Allow process to receive a SIGPIPE if gzip exits.
        gzip_process.communicate()  # Wait for gzip to finish.
    print(f"Backup for database: {db_name} completed: {backup_file}.")

main()
