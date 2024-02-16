
'''
Title: IDS for event handling
Author: Thomas E. Baulch
Date: 03/03/2024
Description: Simple HIDS to monitor file system changes on a specified directory.
'''

# Importing necessary libraries
import os
import time
from datetime import datetime  # For timestamping events
import pytz  # For UK timezone handling
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Log file path where notifications will be saved
log_file_path = 'C:\\Users\\tom\\Desktop\\hids_notifications.txt'

# Custom class to handle file system events
class TomFileWatcher(FileSystemEventHandler):
    def __init__(self):
        # Initialize to track time between logged events
        self.last_logged_time = 0

    def log_event(self, message):
        # Current time in seconds since the epoch
        current_time = time.time()
        # Log events message to both console and file.
        # Only logs if 1 second has passed to avoid spam
        if current_time - self.last_logged_time > 1:
            # Fetch UK current time
            uk_time = datetime.now(pytz.timezone('Europe/London'))
            # Format the timestamp
            formatted_time = uk_time.strftime('%Y-%m-%d %H:%M:%S %Z')
            # Append timestamp to the log message
            message_with_timestamp = f"{formatted_time} - {message}"
            print(message_with_timestamp)
            with open(log_file_path, 'a') as log_file:
                log_file.write(message_with_timestamp + '\n')
            # Update last logged time
            self.last_logged_time = current_time

    # Handles when a file is modified
    def on_modified(self, event):
        self.log_event(f'Alert: {event.src_path} was just modified. Keep an eye on this!')

    # Handles when a new file is created
    def on_created(self, event):
        self.log_event(f'Heads up! A new file: {event.src_path} has appeared. Could be something or nothing.')

    # Handles when a file is deleted
    def on_deleted(self, event):
        self.log_event(f'Just so you know, {event.src_path} was deleted. Hope it was expected.')

if __name__ == "__main__":
    # Path to monitor for changes
    path_to_watch = 'C:\\Users\\tom\\Desktop'
    event_handler = TomFileWatcher()
    observer = Observer()
    # Scheduling the observer to monitor the specified path
    observer.schedule(event_handler, path=path_to_watch, recursive=True)
    observer.start()

    try:
        # Running the observer in a loop to keep the script active
        print("Monitoring started on: " + path_to_watch + ". Press CTRL+C to stop.")
        while True:
            # Loop sleep time, can be adjusted as needed
            time.sleep(10)
    except KeyboardInterrupt:
        # Handling user interrupt to gracefully stop the monitoring
        print("Monitoring stopped by user.")
        observer.stop()
    observer.join()

