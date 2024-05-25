======================================================
           PhantomStrain README           
======================================================

Welcome to the PhantomStrain project! This project aims to demonstrate various malicious activities that can be performed on Windows systems. It consists of a server-side application and several client-side applications designed to carry out different malicious tasks.

### Features:

#### CLIENT
- **Corrupt Antiviruses**: Corrupts antivirus software to bypass security measures.
- **Disable Antivirus Popups**: Disables antivirus popups using registry modifications.
- **Click on Antivirus Popups**: Automatically clicks on antivirus popups to allow malware to run.
- **Copy to Startup Folder**: Copies the client application to the Windows startup folder for persistence.
- **Spreads Over LAN**: Spreads itself over the Local Area Network (LAN) using File Transfer Protocol (FTP).
- **Execute Commands**: Executes commands received from the server.
- **Send Video Transmission**: Sends live video transmission to the server.
- **Sends Data Over TCP**: Communicates with the server over TCP protocol.

#### SERVER
- **Receive Video Transmission**: Receives live video transmission from client applications.
- **Send Commands**: Sends commands to client applications.
- **Navigate Between Multiple Clients**: Manages multiple client connections.
- **GUI**: Provides a graphical user interface for easy interaction.

### Installation:

1. Clone the repository to your local machine.
2. Install all the pre-reqisites using setup.py and the command 'pip install .'.
3. Run the server application (`server.py`) on a host machine.
4. Run the desired client applications (`windows_acceptor.py`, `ac.py`, etc.) on target machines (they will be autorun when spoofed file is clicked).
5. For testing usage it is reccomended that all the client files are compiled and run as console-less, window only. The server as well.
6. For viewing how it could be used maliciously subsitute the prints in the scripts for " " or "pass" depending their positions.

### Script Names
- server.py		/ the server
- windows_acceptor.py   / connects with server and does main operations
- ac.py     		/ corrupts the antivirus
- dnc.py    		/ edits windows registry
- nn.py	    		/ clicks on antivirus popups to allow malicous codes to run (overrides safe windows)

### Usage:

- Make sure to be in a safe testing environment such as a VM.
- Start the server application to listen for client connections.
- Run the client applications on target machines to perform various malicious activities.
- Use the GUI provided by the server to manage and interact with connected clients.
- To modify server's ip and ports change the following variables:
	HOST			/ servers ip
	VIDEO_PORT		/ video port
	COMMAND_PORT		/ command port
	START_VID_PORT		/ video start port
- To modify clients's ip and ports change the following variables:
	SERVER_HOST		/ servers ip
	VIDEO_PORT		/ servers video port
	COMMAND_PORT		/ servers command port
	START_VID_PORT		/ servers video start port


### How To Spoof Client Scripts For Testing/Educational Purposes:

To create a spoofed shortcut that runs all the client scripts without needing their paths, follow these steps:

1. Place all the client application executables in a folder.
2. Create a batch script (`run_all.bat`) in the same folder with the content:
	@echo off
	for %%i in (*.exe) do start "" "%%i"
(batch will not work if the client scripts are not compiled)
3. Create a shortcut to the batch script and place it in a location accessible to the target user.
4. Right-click on the shortcut, select "Properties", and append the path to the batch script in the "Target" field.
5. When the user double-clicks on the spoofed shortcut, all the client scripts will be executed.

### Disclaimer:

This project is for educational purposes only. Unauthorized use of this software may violate local, state, or federal laws. The authors assume no liability and are not responsible for any misuse or damage caused by this software.
This project is protected by the GNU Affero General Public License v3.0.

For more information or any question email: HellwareStudios06@gmail.com
I will try to answer and help the best I can during my free time.

======================================================
