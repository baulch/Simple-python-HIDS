
'''
Title: IDS for event handling
author: Thomas E. Baulch
Date: 03/03/2024
Description: Simple HIDS to monitor file system changes on a specified directory.
'''

# Importing necessary libraries
import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
#Log file path
log_file_path = 'C:\\Users\\tom\\Desktop\\hids_notifications.txt'
# Custom class to handle file system events
class TomFileWatcher(FileSystemEventHandler):
    def __init__(self):
        self.last_logged_time = 0


    def log_event(self, message):
        current_time = time.time()
        ##Log events message to both console and file.
        if current_time - self.last_logged_time > 1: ## Only logs if 1 second has passed
            print(message)
            with open(log_file_path, 'a') as log_file:
                log_file.write(message + '\n')
            self.last_logged_time = current_time

    #Class to handle file system changes such as file modifications, creations, and deletions

    def on_modified(self, event):
        ## Notifies when a file is modified
        self.log_event(f'Alert: {event.src_path} was just modified. Keep an eye on this!')

    def on_created(self, event):
        ## Notifies when a new file is created
        self.log_event(f'Heads up! A new file: {event.src_path} has appeared. Could be something or nothing.')

    def on_deleted(self, event):
        # Notifies when a file is deleted
        self.log_event(f'Just so you know, {event.src_path} was deleted. Hope it was expected.')

if __name__ == "__main__":
    path_to_watch = 'C:\\Users\\tom\\Desktop'  # Path to monitor for changes
    event_handler = TomFileWatcher()
    observer = Observer()
    observer.schedule(event_handler, path=path_to_watch, recursive=True)
    observer.start()

    try:
        # Running the observer in a loop to keep the script active
        print("Monitoring started on: " + path_to_watch + ". Press CTRL+C to stop.")
        while True:
            time.sleep(10)  # Adjust the sleep time as needed
    except KeyboardInterrupt:
        print("Monitoring stopped by user.")
        observer.stop()
    observer.join()

