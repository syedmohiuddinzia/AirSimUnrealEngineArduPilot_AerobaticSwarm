import tkinter as tk
from tkinter import messagebox
import subprocess
import os
import threading
import time

# ----------- SETTINGS -----------------
MAVPROXY_CMD = "mavproxy.py"
MASTER = "udp:127.0.0.1:14550"
SCRIPTS_DIR = os.path.expanduser("~/swarm")
# --------------------------------------

mavproxy_proc = None
auto_running = False   # <--- NEW FLAG


# -----------------------------------------------------
# MAVProxy Start
# -----------------------------------------------------
def start_mavproxy():
    global mavproxy_proc

    if mavproxy_proc is None:
        try:
            mavproxy_proc = subprocess.Popen(
                [MAVPROXY_CMD, f"--master={MASTER}", "--source-system", "1", "--console"],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            messagebox.showinfo("MAVProxy", "MAVProxy started successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to start MAVProxy:\n{e}")
    else:
        messagebox.showinfo("MAVProxy", "Already running.")


# -----------------------------------------------------
# Send script
# -----------------------------------------------------
def send_script(script_name):
    global mavproxy_proc

    if mavproxy_proc is None:
        messagebox.showwarning("MAVProxy", "Start MAVProxy first!")
        return

    script_path = os.path.join(SCRIPTS_DIR, script_name)

    if not os.path.isfile(script_path):
        messagebox.showerror("Error", f"{script_name} not found!")
        return

    try:
        mavproxy_proc.stdin.write(f"script {script_path}\n")
        mavproxy_proc.stdin.flush()
    except Exception as e:
        messagebox.showerror("Error", f"Failed to send script:\n{e}")


# -----------------------------------------------------
# AUTO MODE (infinite loop)
# -----------------------------------------------------
def run_auto_sequence():
    global auto_running
    global mavproxy_proc

    if mavproxy_proc is None:
        messagebox.showwarning("MAVProxy", "Start MAVProxy first!")
        return

    sequence = ["step1.txt", "step2.txt", "step3.txt", "step4.txt"]

    auto_running = True  # AUTO started

    while auto_running:  # <--- INFINITE LOOP
        for script in sequence:
            if not auto_running:
                print("AUTO stopped!")
                return

            path = os.path.join(SCRIPTS_DIR, script)
            print("AUTO →", script)

            try:
                mavproxy_proc.stdin.write(f"script {path}\n")
                mavproxy_proc.stdin.flush()
            except Exception as e:
                print("Error sending:", script, e)

            time.sleep(3)

    print("AUTO loop ended.")


def run_auto():
    thread = threading.Thread(target=run_auto_sequence)
    thread.daemon = True
    thread.start()
    messagebox.showinfo("AUTO MODE", "Auto sequence running infinitely.")


# -----------------------------------------------------
# STOP AUTO WHEN ALLIGN IS PRESSED
# -----------------------------------------------------
def stop_auto_and_align():
    global auto_running
    auto_running = False   # <---- STOP AUTO LOOP
    send_script("l50_xx.txt")  # run align script
    print("AUTO stopped by ALLIGN button.")


# -----------------------------------------------------
# MAIN WINDOW
# -----------------------------------------------------
root = tk.Tk()
root.title("Drone Swarm Control")
root.geometry("150x290")

btn_start = tk.Button(root, text="START", command=start_mavproxy, width=12, bg="green", fg="white")
btn_start.pack(pady=5)

btn_arm = tk.Button(root, text="ARM", width=12, bg="green", fg="white", command=lambda: send_script("start.txt"))
btn_arm.pack(pady=5)

btn_disarm = tk.Button(root, text="DISARM", width=12, bg="red", fg="white", command=lambda: send_script("disarm.txt"))
btn_disarm.pack(pady=5)

btn_takeoff = tk.Button(root, text="TAKEOFF", width=12, bg="green", fg="white", command=lambda: send_script("takeoff.txt"))
btn_takeoff.pack(pady=5)

btn_align = tk.Button(root, text="ALLIGN", width=12, bg="orange", fg="black", command=stop_auto_and_align)
btn_align.pack(pady=5)

btn_auto = tk.Button(root, text="AUTO", width=12, bg="blue", fg="white", command=run_auto)
btn_auto.pack(pady=5)

btn_quit = tk.Button(root, text="QUIT", width=12, bg="red", fg="white", command=root.destroy)
btn_quit.pack(pady=5)

root.mainloop()

