# SerialChat

Python Multithreading Chat over Serial Port with Qt interface and Encryption

---
## Description
The purpose of this project is to provide a **multi-threading** chat application with a friendly qt interface.

The idea behind *serialChat* is **half-duplex** communication over radio through serial port.

The *serialChat* now supports **Python 3.11+**

---
## Dependencies
The *serialChat* depends on:

- PySide6 (Qt6 bindings)
- pyserial
- pycryptodome (replaces pycrypto)

Install all dependencies with:
```bash
pip install -r requirements.txt
```

---
## Installation
1. Clone the project
2. Create and activate a virtual environment (recommended)
3. Install dependencies
4. Run the application

```bash
git clone https://github.com/yourusername/SerialChat.git
cd SerialChat
python -m venv .env
.env\Scripts\activate  # Windows
pip install -r requirements.txt
python serialChat.py
```

**Tested on:**
 
* WIN_XP
* WIN7
* WIN10 
* Linux

---

## Create Executable File ( OneFile ) 

```bash
pip install pyinstaller
```
Inside the folder of SerialChat enter the command

```bash
pyinstaller --noconsole --onefile --icon resources\icons\chat.ico serialChat.py
```
Now put the **serialChat.exe** from the folder **dist** in the same folder with the folders **config** and **resources** and then you will able to run the serialChat by clicking on the **serialChat.exe**

---

## Usage


After you start the application, you can go to the *settings* menu item and configure the *serialChat* with your specific configuration.

1. Choose your serial port from the dropdown list.
2. Change the serial port configuration to your needs.
3. Enable ACP-127 text based protocol (optional).
4. Enable AES-CBC encryption (optional).
5. Enter your nickname.
6. Change the path with one that you wish the incoming files to be saved. 


Then you're ready to GO...

