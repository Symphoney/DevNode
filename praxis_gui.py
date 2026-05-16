import tkinter as tk
import time
from ai_client import ask_ai

def get_mem():
    with open('/proc/meminfo', 'r') as f:
        lines = f.readlines()

    meminfo = {}
    for line in lines:
        parts = line.split()
        meminfo[parts[0].rstrip(':')] = int(parts[1])

    total = meminfo["MemTotal"] // 1024
    available = meminfo["MemAvailable"] // 1024
    used = total - available
    return used, total

def get_uptime():
    with open('/proc/uptime', 'r') as f:
        uptime_seconds = float(f.readline().split()[0])
    minutes = int(uptime_seconds / 60)
    return str(minutes) + " min"

def get_mode(used):
    if used < 150:
        return "LURKING", "( -_- )"
    elif used < 300:
        return "SCANNING", "◣   ◢
  ▬"
    else:
        return "COMPROMISED", "( >_< )"

def update_dashboard():
    used, total = get_mem()
    uptime = get_uptime()
    mode, face = get_mode(used)

    ram_label.config(text="RAM: {} MB / {} MB".format(used, total))
    uptime_label.config(text="UPTIME: {}".format(uptime))
    mode_label.config(text="MODE: {}".format(mode))
    face_label.config(text=face)

    root.after(1500, update_dashboard)

def send_message():
    prompt = input_box.get()
    if prompt.strip() == "":
        return

    chat_log.insert(tk.END, "YOU: " + prompt + "\n")
    input_box.delete(0, tk.END)

    chat_log.insert(tk.END, "KOR: Contemplating...\n")
    root.update()

    response = ask_ai(prompt)
    chat_log.insert(tk.END, "KOR: " + response + "\n\n")
    chat_log.see(tk.END)

root = tk.Tk()
root.overrideredirect(True)
root.attributes("-fullscreen", True)
root.title("PRAXIS")
root.geometry("800x480")
root.configure(bg="#050814")

# Colors
BG = "#050814"
PANEL = "#0b1020"
CYAN = "#47d7ff"
GOLD = "#d7a84f"
TEXT = "#e6e0d6"
RED = "#ff5c5c"

title = tk.Label(
    root,
    text="PRAXIS",
    font=("Courier", 28, "bold"),
    fg=CYAN,
    bg=BG
)
title.pack(pady=12)

main_frame = tk.Frame(root, bg=BG)
main_frame.pack(fill="both", expand=True, padx=20, pady=10)

left = tk.Frame(main_frame, bg=PANEL, highlightbackground=CYAN, highlightthickness=2)
left.pack(side="left", fill="both", expand=True, padx=(0, 10))

right = tk.Frame(main_frame, bg=PANEL, highlightbackground=GOLD, highlightthickness=2)
right.pack(side="right", fill="both", expand=True, padx=(10, 0))

status_title = tk.Label(left, text="MISSION STATUS", font=("Courier", 16, "bold"), fg=GOLD, bg=PANEL)
status_title.pack(pady=10)

ram_label = tk.Label(left, text="RAM:", font=("Courier", 13), fg=TEXT, bg=PANEL)
ram_label.pack(anchor="w", padx=20, pady=4)

uptime_label = tk.Label(left, text="UPTIME:", font=("Courier", 13), fg=TEXT, bg=PANEL)
uptime_label.pack(anchor="w", padx=20, pady=4)

mode_label = tk.Label(left, text="MODE:", font=("Courier", 13, "bold"), fg=CYAN, bg=PANEL)
mode_label.pack(anchor="w", padx=20, pady=4)

face_label = tk.Label(left, text="( -_- )", font=("Courier", 38, "bold"), fg=CYAN, bg=PANEL)
face_label.pack(pady=35)

chat_title = tk.Label(right, text="KOR INTERFACE", font=("Courier", 16, "bold"), fg=CYAN, bg=PANEL)
chat_title.pack(pady=10)

chat_log = tk.Text(
    right,
    height=12,
    width=40,
    bg="#070b16",
    fg=TEXT,
    insertbackground=TEXT,
    font=("Courier", 10),
    wrap="word",
    borderwidth=0
)
chat_log.pack(padx=12, pady=8, fill="both", expand=True)

input_box = tk.Entry(
    right,
    bg="#10182c",
    fg=TEXT,
    insertbackground=TEXT,
    font=("Courier", 11),
    borderwidth=0
)
input_box.pack(fill="x", padx=12, pady=(0, 8))
input_box.bind("<Return>", lambda event: send_message())

send_button = tk.Button(
    right,
    text="SEND",
    command=send_message,
    bg="#15213a",
    fg=CYAN,
    activebackground="#1e2f52",
    activeforeground=GOLD,
    font=("Courier", 10, "bold")
)
send_button.pack(pady=(0, 12))

update_dashboard()
root.mainloop()
