import argparse
import os
import time
import tkinter as tk

from ai_client import ask_ai


PALETTE = {
    "bg": "#03070f",
    "bg2": "#050c1a",
    "panel": "#091428",
    "ink": "#d6deff",
    "cyan": "#4de2ff",
    "magenta": "#ff5de2",
    "amber": "#ffc35a",
    "danger": "#ff5c5c",
    "muted": "#7d8ebf",
}

SIGILS = {
    "spider": [
        r"      /\  /\      ",
        r"  ___/  \/  \___  ",
        r" /  _  /\  /  _  \ ",
        r" | /_\/_ \/ _\/_\ | ",
        r" | \__/  ||  \__/ | ",
        r"  \_____/  \_____/  ",
        r"    /  / __ \  \    ",
        r"   /__/ /  \ \__\   ",
    ],
    "raccoon": [
        r"   ___  ____  ___   ",
        r"  / _ \/ __ \/ _ \  ",
        r" | | | / /\ \ | | | ",
        r" | | | \ \/ / | | | ",
        r" | |_| |\__/| |_| | ",
        r"  \___/  --  \___/  ",
        r"   /  __/\__  \     ",
        r"  /__/  KOR \__\    ",
    ],
    "sly": [
        r"   _________   _____ ",
        r"  /  ___   /  / ___/ ",
        r" /  /  /  /  / /__   ",
        r"/__/  /__/   \___/   ",
        r"  __   ____   __     ",
        r" / /  / __ \ / /     ",
        r"/ /__/ /_/ // /__    ",
        r"\____/\____/\____/   ",
    ],
}


def get_mem():
    with open("/proc/meminfo", "r", encoding="utf-8") as handle:
        lines = handle.readlines()

    meminfo = {}
    for line in lines:
        parts = line.split()
        meminfo[parts[0].rstrip(":")] = int(parts[1])

    total = meminfo["MemTotal"] // 1024
    available = meminfo["MemAvailable"] // 1024
    used = total - available
    return used, total


def get_cpu_percent():
    with open("/proc/stat", "r", encoding="utf-8") as handle:
        cpu = handle.readline().split()[1:]

    values = [int(x) for x in cpu]
    idle = values[3] + values[4]
    total = sum(values)
    return idle, total


def get_uptime():
    with open("/proc/uptime", "r", encoding="utf-8") as handle:
        uptime_seconds = float(handle.readline().split()[0])
    minutes = int(uptime_seconds / 60)
    hours = minutes // 60
    mins = minutes % 60
    return f"{hours:02d}:{mins:02d}"


def get_mode(ram_percent, cpu_percent):
    if ram_percent < 40 and cpu_percent < 35:
        return "STEALTH", ".."
    if ram_percent < 70 and cpu_percent < 65:
        return "SCOUTING", "oo"
    return "COMBAT", "!!"


class PraxisGui:
    def __init__(self, root, sigil_name="spider"):
        self.root = root
        self.sigil_name = sigil_name if sigil_name in SIGILS else "spider"
        self.cpu_prev = get_cpu_percent()

        self.root.title("PRAXIS // KOR")
        self.root.geometry("800x480")
        self.root.configure(bg=PALETTE["bg"])

        self.root.bind("<Escape>", self.exit_app)
        self.root.bind("<Control-q>", self.exit_app)

        self.build_layout()
        self.update_dashboard()

    def enable_kiosk(self):
        self.root.attributes("-fullscreen", True)

    def exit_app(self, _event=None):
        self.root.destroy()

    def build_layout(self):
        top = tk.Frame(self.root, bg=PALETTE["bg"])
        top.pack(fill="x", padx=18, pady=(8, 2))

        self.title_label = tk.Label(
            top,
            text="PRAXIS // KOR",
            font=("Courier", 24, "bold"),
            fg=PALETTE["cyan"],
            bg=PALETTE["bg"],
        )
        self.title_label.pack(side="left")

        self.clock_label = tk.Label(
            top,
            text="00:00:00",
            font=("Courier", 14, "bold"),
            fg=PALETTE["amber"],
            bg=PALETTE["bg"],
        )
        self.clock_label.pack(side="right")

        subtitle = tk.Label(
            self.root,
            text=f"SIGIL: {self.sigil_name.upper()}  |  ESC to exit kiosk",
            font=("Courier", 10),
            fg=PALETTE["muted"],
            bg=PALETTE["bg"],
        )
        subtitle.pack(anchor="w", padx=20, pady=(0, 6))

        split = tk.PanedWindow(self.root, sashwidth=6, bg=PALETTE["bg"], bd=0)
        split.pack(fill="both", expand=True, padx=16, pady=(0, 14))

        left = tk.Frame(split, bg=PALETTE["panel"], highlightbackground=PALETTE["magenta"], highlightthickness=2)
        right = tk.Frame(split, bg=PALETTE["panel"], highlightbackground=PALETTE["cyan"], highlightthickness=2)
        split.add(left, minsize=280)
        split.add(right, minsize=420)

        tk.Label(
            left,
            text="CYBERDECK STATUS",
            font=("Courier", 14, "bold"),
            fg=PALETTE["amber"],
            bg=PALETTE["panel"],
        ).pack(anchor="w", padx=16, pady=(14, 8))

        sigil_block = "\n".join(SIGILS[self.sigil_name])
        self.sigil = tk.Label(
            left,
            text=sigil_block,
            justify="left",
            font=("Courier", 10, "bold"),
            fg=PALETTE["magenta"],
            bg=PALETTE["bg2"],
            padx=10,
            pady=8,
        )
        self.sigil.pack(fill="x", padx=16, pady=(0, 10))

        self.ram_label = tk.Label(left, text="RAM: --", font=("Courier", 12), fg=PALETTE["ink"], bg=PALETTE["panel"])
        self.ram_label.pack(anchor="w", padx=16, pady=2)

        self.cpu_label = tk.Label(left, text="CPU: --", font=("Courier", 12), fg=PALETTE["ink"], bg=PALETTE["panel"])
        self.cpu_label.pack(anchor="w", padx=16, pady=2)

        self.uptime_label = tk.Label(left, text="UPTIME: --", font=("Courier", 12), fg=PALETTE["ink"], bg=PALETTE["panel"])
        self.uptime_label.pack(anchor="w", padx=16, pady=2)

        self.mode_label = tk.Label(left, text="MODE: --", font=("Courier", 12, "bold"), fg=PALETTE["cyan"], bg=PALETTE["panel"])
        self.mode_label.pack(anchor="w", padx=16, pady=6)

        self.face_label = tk.Label(left, text="[ .. ]", font=("Courier", 28, "bold"), fg=PALETTE["cyan"], bg=PALETTE["panel"])
        self.face_label.pack(pady=(6, 0))

        tk.Label(
            right,
            text="KOR COMMS",
            font=("Courier", 14, "bold"),
            fg=PALETTE["cyan"],
            bg=PALETTE["panel"],
        ).pack(anchor="w", padx=14, pady=(14, 6))

        self.chat_log = tk.Text(
            right,
            bg=PALETTE["bg2"],
            fg=PALETTE["ink"],
            insertbackground=PALETTE["ink"],
            font=("Courier", 10),
            wrap="word",
            borderwidth=0,
            height=12,
            padx=10,
            pady=10,
        )
        self.chat_log.pack(fill="both", expand=True, padx=14, pady=(0, 8))
        self.chat_log.insert("end", "KOR: Link online. Ask anything.\n\n")

        input_row = tk.Frame(right, bg=PALETTE["panel"])
        input_row.pack(fill="x", padx=14, pady=(0, 12))

        self.input_box = tk.Entry(
            input_row,
            bg="#111d36",
            fg=PALETTE["ink"],
            insertbackground=PALETTE["ink"],
            font=("Courier", 11),
            relief="flat",
        )
        self.input_box.pack(side="left", fill="x", expand=True, ipady=6)
        self.input_box.bind("<Return>", self.send_message)

        self.send_button = tk.Button(
            input_row,
            text="TRANSMIT",
            command=self.send_message,
            bg="#1d2e52",
            fg=PALETTE["cyan"],
            activebackground="#2f467a",
            activeforeground=PALETTE["amber"],
            font=("Courier", 10, "bold"),
            relief="flat",
            padx=12,
        )
        self.send_button.pack(side="left", padx=(8, 0))

    def update_dashboard(self):
        used, total = get_mem()
        uptime = get_uptime()

        idle_now, total_now = get_cpu_percent()
        idle_prev, total_prev = self.cpu_prev
        idle_delta = max(1, idle_now - idle_prev)
        total_delta = max(1, total_now - total_prev)
        cpu_percent = int((1 - (idle_delta / total_delta)) * 100)
        cpu_percent = max(0, min(cpu_percent, 100))
        self.cpu_prev = (idle_now, total_now)

        ram_percent = int((used / max(1, total)) * 100)
        mode, eyes = get_mode(ram_percent, cpu_percent)

        self.clock_label.config(text=time.strftime("%H:%M:%S"))
        self.ram_label.config(text=f"RAM: {used} MB / {total} MB  ({ram_percent}%)")
        self.cpu_label.config(text=f"CPU: {cpu_percent}%")
        self.uptime_label.config(text=f"UPTIME: {uptime}")
        self.mode_label.config(text=f"MODE: {mode}")
        self.face_label.config(text=f"[ {eyes} ]")

        if mode == "COMBAT":
            self.mode_label.config(fg=PALETTE["danger"])
            self.face_label.config(fg=PALETTE["danger"])
        elif mode == "SCOUTING":
            self.mode_label.config(fg=PALETTE["amber"])
            self.face_label.config(fg=PALETTE["amber"])
        else:
            self.mode_label.config(fg=PALETTE["cyan"])
            self.face_label.config(fg=PALETTE["cyan"])

        self.root.after(1200, self.update_dashboard)

    def send_message(self, _event=None):
        prompt = self.input_box.get().strip()
        if not prompt:
            return

        self.chat_log.insert("end", f"YOU: {prompt}\n")
        self.input_box.delete(0, "end")
        self.chat_log.insert("end", "KOR: Contemplating...\n")
        self.chat_log.see("end")
        self.root.update_idletasks()

        response = ask_ai(prompt)
        self.chat_log.delete("end-2l", "end-1l")
        self.chat_log.insert("end", f"KOR: {response}\n\n")
        self.chat_log.see("end")


def parse_args():
    parser = argparse.ArgumentParser(description="PRAXIS cyberdeck UI")
    parser.add_argument("--windowed", action="store_true", help="run in a window instead of fullscreen kiosk")
    parser.add_argument(
        "--sigil",
        choices=sorted(SIGILS.keys()),
        default=os.environ.get("PRAXIS_SIGIL", "spider"),
        help="pick branding sigil shown on the status panel",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    root = tk.Tk()
    app = PraxisGui(root, sigil_name=args.sigil)
    if not args.windowed:
        app.enable_kiosk()
    root.mainloop()


if __name__ == "__main__":
    main()