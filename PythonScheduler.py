from datetime import datetime
import schedule
import os
import sys
import shutil
import configparser


def read_config():
    config = configparser.ConfigParser()
    config.read('config.ini')
    return config

def get_log_directory():
    config = read_config()
    return config.get('Settings', 'log_directory', fallback='.')

def add_to_startup(executable_path, startup_folder=None):
    try:
        if not startup_folder:
            # Default startup folder for the current user
            startup_folder = os.path.join(os.getenv('APPDATA'), 'Microsoft', 'Windows', 'Start Menu', 'Programs', 'Startup')

        # Check if the executable is already in the startup folder
        destination_path = os.path.join(startup_folder, os.path.basename(executable_path))
        if not os.path.exists(destination_path):
            # Copy the executable to the startup folder
            shutil.copy2(executable_path, destination_path)
            print(f"Executable copied to the Startup folder: {destination_path}")
        else:
            print("Executable is already in the Startup folder.")

    except Exception as e:
        print(f"Error adding to startup: {e}")

def write_timestamp_to_file(file_path="timestamp_log.txt"):
    try:
        # Get the log directory from the configuration
        log_directory = get_log_directory()

        # Use the log directory for the log file path
        file_path = os.path.join(log_directory, file_path)

        # Check if the log file exists
        if not os.path.exists(file_path):
            # If the file doesn't exist, create it
            with open(file_path, 'w') as new_file:
                pass  # Create an empty file

        # Get the current timestamp
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Open the file in append mode and write the timestamp
        with open(file_path, "a") as file:
            file.write(current_time + "\n")

        print(f"Timestamp '{current_time}' has been written to '{file_path}'.")
    except Exception as e:
        print(f"Error writing timestamp to file: {e}")

if __name__ == "__main__":

    # Change the current working directory to the log directory
    #exe_dir = os.path.dirname(os.path.abspath(__file__))
    exe_dir = 'D:\\PythonWorkspace\\PythonExe\\dist'
    os.chdir(exe_dir)
    print(f"This Exe is running from: {exe_dir}")
    
    # Get the path of the currently running script (executable)
    script_path = os.path.abspath(sys.argv[0])

    # Add the script to startup
    ##add_to_startup(script_path)
    
    # Schedule a job (e.g., write timestamp every minute)
    schedule.every(5).seconds.do(write_timestamp_to_file)

    # Run the scheduled jobs
    while True:
        schedule.run_pending()
