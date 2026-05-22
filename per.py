import winreg

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

        print(f"[+] Added '{app_name}' to startup")

    except Exception as e:
        print(f"[-] Error: {e}")


# Programs you want to auto-run
programs = {
    "Notepad": r"C:\Windows\System32\notepad.exe",
}


for name, path in programs.items():
    add_to_startup(name, path)