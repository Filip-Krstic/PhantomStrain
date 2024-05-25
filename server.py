import socket
import cv2
import numpy as np
import threading
import tkinter as tk
from tkinter import messagebox
import time
from ctypes import windll

global START_VID_PORT
global HOST
global VIDEO_PORT
global COMMAND_PORT

HOST = '0.0.0.0'  # Modify this
VIDEO_PORT = 9999
COMMAND_PORT = 65432
START_VID_PORT = 1111

def try_start():
    global button_pressed
    global startnconner
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, START_VID_PORT))
        s.listen()
        print("Server is listening for connections...")
        startnconner, addr = s.accept()
        with startnconner:
            print('Connected by', addr)


hello_thread = threading.Thread(target=try_start)
hello_thread.start()

video_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
video_socket.bind((HOST, VIDEO_PORT))
video_socket.listen(1)

command_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
command_socket.bind((HOST, COMMAND_PORT))
command_socket.listen()

clients = {}

button_pressed = False

def recvall(sock, count):
    buf = b''
    while count:
        newbuf = sock.recv(count)
        if not newbuf:
            return None
        buf += newbuf
        count -= len(newbuf)
    return buf

def ahandle_video_connections():
    global clients
    while True:
        video_client_socket, video_client_addr = video_socket.accept()
        client_key = f"VC: {video_client_addr[0]}"
        print("Video client connected:", video_client_addr)
        clients_listbox.insert(tk.END, client_key)
        clients[client_key] = (video_client_socket, video_client_addr)
        root.update_idletasks()
        root.update()
        threading.Thread(target=receive_video, args=(video_client_socket, client_key), daemon=True).start()

def handle_video_connections():
    global clients
    while True:
        try:
            video_client_socket, video_client_addr = video_socket.accept()
            print("Video client connected:", video_client_addr)
            client_key = f"VC: {video_client_addr[0]}"
            if client_key not in clients:
                video_client_socket, video_client_addr = video_socket.accept()
                client_key = f"VC: {video_client_addr[0]}"
                print("Video client connected:", video_client_addr)
                clients_listbox.insert(tk.END, client_key)
                clients[client_key] = (video_client_socket, video_client_addr)
                root.update_idletasks()
                root.update()
                threading.Thread(target=receive_video, args=(video_client_socket, client_key), daemon=True).start()
            else:
                remove_client(client_key)
                video_client_socket, video_client_addr = video_socket.accept()
                client_key = f"VC: {video_client_addr[0]}"
                print("Video client connected:", video_client_addr)
                clients_listbox.insert(tk.END, client_key)
                clients[client_key] = (video_client_socket, video_client_addr)
                root.update_idletasks()
                root.update()
                threading.Thread(target=receive_video, args=(video_client_socket, client_key), daemon=True).start()
                receive_video(video_client_socket, client_key)

            root.update_idletasks()
            root.update()
        except Exception as e:
            print(f"Error handling command client connection: {e}")
            remove_client(client_key)
            break            

def receive_video(video_client_socket, selected_client_ip):
    while True:
        try:
            frame_length = recvall(video_client_socket, 16)
            if not frame_length:
                print("No frame length received.")
                break
            frame_length = int(frame_length)
            frame_data = recvall(video_client_socket, frame_length)
            if not frame_data:
                print("No frame data received.")
                break
            frame_array = np.frombuffer(frame_data, dtype=np.uint8)
            frame = cv2.imdecode(frame_array, cv2.IMREAD_COLOR)
            cv2.imshow(selected_client_ip, frame)
            key = cv2.waitKey(1)
            if key == ord('q'):
                break
        except Exception as e:
            print(f"Error receiving video: {e}")
            
            break

def handle_command_connections():
    global clients
    while True:
        try:
            command_client_socket, command_client_address = command_socket.accept()
            print(f"Connected to {command_client_address}")
            client_key = f"CC: {command_client_address[0]}"
            if client_key not in clients:
                clients_listbox.insert(tk.END, f"CC: {command_client_address[0]}")
                clients[client_key] = command_client_socket
            else:
                command_client_socket.close()
            root.update_idletasks()
            root.update()
        except Exception as e:
            print(f"Error handling command client connection: {e}")
            remove_client(client_key)
            break

def send_command_to_client():
    try:
        index = clients_listbox.curselection()
        if index:
            client_name = clients_listbox.get(index)
            if client_name.startswith("CC:"):
                client_key = f"CC: {client_name.split(': ')[1]}"
                if client_key in clients:
                    client_socket = clients[client_key]
                    command = command_entry.get("1.0", tk.END).strip()
                    if command:
                        client_socket.sendall(command.encode())
                        output = client_socket.recv(1024).decode()
                        output_text.config(state=tk.NORMAL)
                        output_text.delete(1.0, tk.END)
                        output_text.insert(tk.END, "Output from client:\n")
                        output_text.insert(tk.END, output + "\n\n")
                        output_text.config(state=tk.DISABLED)
                    else:
                        messagebox.showwarning("Warning", "Please enter a command.")
                else:
                    messagebox.showerror("Error", "Client not found in the clients dictionary.")
            else:
                messagebox.showerror("Error", "Please select a command client.")
        else:
            messagebox.showerror("Error", "Please select a client.")
    except ConnectionResetError:
        messagebox.showerror("Error", "Connection with client closed unexpectedly.")
        remove_client(client_key)

def remove_client(client_key):
    clients_listbox.delete(clients_listbox.index(f"CC: {client_key.split(':')[1]}"))
    del clients[client_key]
    clients_listbox.delete(clients_listbox.index(f"VC: {client_key.split(':')[1]}"))
    del clients[client_key]

def toggle_view_camera():
    global button_pressed
    global startnconner
    button_pressed = True
    message = "start_video_transmission"
    for client_key in clients:
        if client_key.startswith("CC:"):
            client_socket = clients[client_key]
            client_socket.sendall(message.encode())

color_index=0
def update_border_color():
    r = int((np.sin(time.time() * 2) + 1) * 127)
    g = int((np.sin(time.time() * 3) + 1) * 127)
    b = int((np.sin(time.time() * 4) + 1) * 127)
    color = '#%02x%02x%02x' % (r, g, b)
    root.configure(bg=color)
    root.after(30, update_border_color)

def update_label_color():
    r = int((np.sin(time.time() * 2) + 1) * 127)
    g = int((np.sin(time.time() * 3) + 1) * 127)
    b = int((np.sin(time.time() * 4) + 1) * 127)
    color = '#%02x%02x%02x' % (r, g, b)
    clients_label.config(fg=color)
    command_entry_label.config(fg=color)
    send_command_button.config(fg=color)
    view_camera_button.config(fg=color)
    clients_listbox.config(fg=color)
    root.after(30, update_label_color)

def move_window(event):
    x, y = event.x, event.y
    root.geometry(f"+{x_root - x}+{y_root - y}")

def get_cursor_position(event):
    global x_root, y_root
    x_root, y_root = event.x_root, event.y_root


root = tk.Tk()
root.title("Server")
update_border_color()
root.rowconfigure(0, weight=1)
root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=1)
clients_frame = tk.Frame(root, bg="black")
clients_frame.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
clients_label = tk.Label(clients_frame, text="Connected Clients:", fg="red", bg="black", font=("Fixedsys", 19, "bold", "underline"))
clients_label.grid(row=0, column=0, sticky="w")
clients_listbox = tk.Listbox(clients_frame, fg="red", bg="black", font=("Fixedsys"))
clients_listbox.grid(row=1, column=0, sticky="nsew")
clients_scrollbar = tk.Scrollbar(clients_frame, orient=tk.VERTICAL, command=clients_listbox.yview)
clients_scrollbar.grid(row=1, column=1, sticky="ns")
clients_listbox.config(yscrollcommand=clients_scrollbar.set)
command_frame = tk.Frame(root, bg="black")
command_frame.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")
command_entry_label = tk.Label(command_frame, text="Enter command to send:", fg="red", bg="black", font=("Fixedsys", 19, "bold", "underline"))
command_entry_label.grid(row=0, column=0, sticky="w")
command_entry = tk.Text(command_frame, bg="black", fg="green", height=3)
command_entry.grid(row=1, column=0, columnspan=3, padx=1.5, pady=(1.5, 1.5), sticky="ew")
send_command_button = tk.Button(command_frame, text="Send Command", command=send_command_to_client, bg="black", fg="red", font=("Fixedsys"))
send_command_button.grid(row=2, column=0, padx=1.5, pady=1.5, sticky="ew")
view_camera_button = tk.Button(command_frame, text="View Client Camera", command=toggle_view_camera, bg="black", fg="red", font=("Fixedsys"))
view_camera_button.grid(row=2, column=1, padx=1.5, pady=1.5, sticky="ew")
output_text = tk.Text(root, fg="red", bg="black")
output_text.grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")
update_label_color()
clients_frame.rowconfigure(1, weight=1)
clients_frame.columnconfigure(0, weight=1)
command_frame.rowconfigure(1, weight=1)
command_frame.rowconfigure(2, weight=1)
command_frame.columnconfigure(0, weight=1)
command_frame.columnconfigure(1, weight=1)
command_frame.columnconfigure(2, weight=1)
threading.Thread(target=handle_video_connections, daemon=True).start()
threading.Thread(target=handle_command_connections, daemon=True).start()
root.bind('<Button-1>', get_cursor_position)
root.bind('<B1-Motion>', move_window)
root.mainloop()
