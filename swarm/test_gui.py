import tkinter as tk
from tkinter import messagebox, Toplevel
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
# Send script to MAVProxy
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
# AUTO MODE (run sequence in background thread)
# -----------------------------------------------------
def run_auto_sequence():
    global mavproxy_proc

    if mavproxy_proc is None:
        messagebox.showwarning("MAVProxy", "Start MAVProxy first!")
        return

    sequence = [
        "l5_xx.txt", "l5_yy.txt", "u5_rt.txt", "v5_rt.txt", "v5_lt.txt", "u5_lt.txt",
        "l5_yy.txt", "l5_xx.txt", "u5_dn.txt", "v5_dn.txt", "v5_up.txt", "u5_up.txt",
        "l5_xx.txt", "l5_yy.txt", "p5_luss.txt", "l5_yy.txt", "c5_ross.txt", "l5_yy.txt",
        "l_zz.txt", "u_lt.txt", "v_lt.txt", "u_lt.txt", "l_zz.txt", "u_rt.txt", "v_rt.txt",
        "u_rt.txt", "l_zz.txt", "l5_yy.txt", "l5_xx.txt", "u_up.txt", "v_up.txt",
        "l5_xx.txt", "u_dn.txt", "v_dn.txt", "l5_xx.txt", "x_pluss.txt", "y_pluss.txt",
        "x_pluss.txt", "l5_xx.txt", "disarm.txt"
    ]

    for script in sequence:
        path = os.path.join(SCRIPTS_DIR, script)
        print("AUTO →", script)
        try:
            mavproxy_proc.stdin.write(f"script {path}\n")
            mavproxy_proc.stdin.flush()
        except Exception as e:
            print("Error sending:", script, e)
        time.sleep(5)

    print("AUTO sequence finished.")


def run_auto():
    thread = threading.Thread(target=run_auto_sequence)
    thread.daemon = True
    thread.start()
    messagebox.showinfo("AUTO MODE", "Auto sequence running in background.")


# -----------------------------------------------------
# MANUAL MODE WINDOW (all movement buttons)
# -----------------------------------------------------
def open_manual_window():
    win = Toplevel()
    win.title("Manual Drone Control")
    win.geometry("480x250")

    buttons = [
        ("u_up", "u_up.txt"),  ("v_up", "v_up.txt"),  ("v_dn", "v_dn.txt"),  ("u_dn", "u_dn.txt"),
        ("l_zz", "l_zz.txt"),  ("x_pluss", "x_pluss.txt"), ("y_pluss", "y_pluss.txt"),
        ("u_lt", "u_lt.txt"),  ("v_lt", "v_lt.txt"),  ("v_rt", "v_rt.txt"),  ("u_rt", "u_rt.txt"),
        ("u5_up", "u5_up.txt"), ("v5_up", "v5_up.txt"), ("v5_dn", "v5_dn.txt"), ("u5_dn", "u5_dn.txt"),
        ("l5_xx", "l5_xx.txt"), ("l5_yy", "l5_yy.txt"),
        ("p5_luss", "p5_luss.txt"), ("c5_ross", "c5_ross.txt"),
        ("u5_lt", "u5_lt.txt"), ("v5_lt", "v5_lt.txt"),
        ("v5_rt", "v5_rt.txt"), ("u5_rt", "u5_rt.txt")
    ]

    row = 0
    col = 0

    for text, file in buttons:
        tk.Button(
            win, text=text, command=lambda f=file: send_script(f), width=10
        ).grid(row=row, column=col, padx=5, pady=5)

        col += 1
        if col == 4:
            col = 0
            row += 1


# -----------------------------------------------------
# MAIN WINDOW
# -----------------------------------------------------
root = tk.Tk()
root.title("Drone Swarm Control")
root.geometry("200x300")

btn_start = tk.Button(root, text="START", command=start_mavproxy, width=12, bg="green", fg="white")
btn_start.pack(pady=5)

btn_arm = tk.Button(root, text="ARM", width=12, bg="green", fg="white", command=lambda: send_script("start.txt"))
btn_arm.pack(pady=5)

btn_disarm = tk.Button(root, text="DISARM", width=12, bg="red", fg="white", command=lambda: send_script("disarm.txt"))
btn_disarm.pack(pady=5)

btn_takeoff = tk.Button(root, text="TAKEOFF", width=12, bg="green", fg="white", command=lambda: send_script("takeoff.txt"))
btn_takeoff.pack(pady=5)

btn_auto = tk.Button(root, text="AUTO", width=12, bg="blue", fg="white", command=run_auto)
btn_auto.pack(pady=5)

btn_manual = tk.Button(root, text="MANUAL", width=12, bg="purple", fg="white", command=open_manual_window)
btn_manual.pack(pady=5)

btn_quit = tk.Button(root, text="QUIT", width=12, bg="red", fg="white", command=root.destroy)
btn_quit.pack(pady=5)

root.mainloop()

