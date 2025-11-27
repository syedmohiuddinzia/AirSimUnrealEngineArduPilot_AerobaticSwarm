import tkinter as tk
from tkinter import messagebox
import subprocess
import os

# Paths (change if different)
MAVPROXY_CMD = "mavproxy.py"
MASTER = "udp:127.0.0.1:14550"
SCRIPTS_DIR = os.path.expanduser("~/swarm")  # where your txt files are

# Global MAVProxy process
mavproxy_proc = None

def start_mavproxy():
    global mavproxy_proc
    if mavproxy_proc is None:
        try:
            # Start MAVProxy with console
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
        messagebox.showinfo("MAVProxy", "MAVProxy is already running.")

def send_script(script_name):
    global mavproxy_proc
    if mavproxy_proc is None:
        messagebox.showwarning("MAVProxy", "Start MAVProxy first!")
        return
    
    script_path = os.path.join(SCRIPTS_DIR, script_name)
    if not os.path.isfile(script_path):
        messagebox.showerror("Error", f"Script {script_name} not found!")
        return
    
    # Send the command to MAVProxy via stdin
    try:
        mavproxy_proc.stdin.write(f"script {script_path}\n")
        mavproxy_proc.stdin.flush()
    except Exception as e:
        messagebox.showerror("Error", f"Failed to send script:\n{e}")

# --- Tkinter UI ---
root = tk.Tk()
root.title("Drone Swarm Control")
root.geometry("355x370")  # wider to fit 3 columns

# Column 1 
btn_start = tk.Button(root, text="START", command=start_mavproxy, width=10, bg="green", fg="white") 
btn_start.grid(row=0, column=0, padx=5, pady=5) 

btn_u_up = tk.Button(root, text="u_up", command=lambda: send_script("u_up.txt"), width=10) 
btn_u_up.grid(row=1, column=0, padx=5, pady=5) 

btn_v_up = tk.Button(root, text="v_up", command=lambda: send_script("v_up.txt"), width=10) 
btn_v_up.grid(row=2, column=0, padx=5, pady=5) 

btn_v_dn = tk.Button(root, text="v_dn", command=lambda: send_script("v_dn.txt"), width=10) 
btn_v_dn.grid(row=3, column=0, padx=5, pady=5) 

btn_u_dn = tk.Button(root, text="u_dn", command=lambda: send_script("u_dn.txt"), width=10) 
btn_u_dn.grid(row=4, column=0, padx=5, pady=5)

# Column 2
btn_start_script = tk.Button(root, text="ARM", command=lambda: send_script("start.txt"), width=10, bg="green", fg="white") 
btn_start_script.grid(row=0, column=1, padx=5, pady=5)

# Quit button
btn_quit = tk.Button(root, text="QUIT", command=root.destroy, width=10, bg="red", fg="white")
btn_quit.grid(row=1, column=1, padx=5, pady=5)

btn_l_zz = tk.Button(root, text="l_zz", command=lambda: send_script("l_zz.txt"), width=10 , bg="yellow") 
btn_l_zz.grid(row=2, column=1, padx=5, pady=5)

btn_plus = tk.Button(root, text="x_pluss", command=lambda: send_script("x_pluss.txt"), width=10) 
btn_plus.grid(row=3, column=1, padx=5, pady=5) 

btn_cross = tk.Button(root, text="y_pluss", command=lambda: send_script("y_pluss.txt"), width=10) 
btn_cross.grid(row=4, column=1, padx=5, pady=5) 

# Column 3
btn_takeoff = tk.Button(root, text="TAKEOFF", command=lambda: send_script("takeoff.txt"), width=10, bg="green", fg="white")
btn_takeoff.grid(row=0, column=2, padx=5, pady=5)

btn_u_lt = tk.Button(root, text="u_lt", command=lambda: send_script("u_lt.txt"), width=10) 
btn_u_lt.grid(row=1, column=2, padx=5, pady=5) 

btn_v_lt = tk.Button(root, text="v_lt", command=lambda: send_script("v_lt.txt"), width=10) 
btn_v_lt.grid(row=2, column=2, padx=5, pady=5) 

btn_v_rt = tk.Button(root, text="v_rt", command=lambda: send_script("v_rt.txt"), width=10) 
btn_v_rt.grid(row=3, column=2, padx=5, pady=5) 

btn_u_rt = tk.Button(root, text="u_rt", command=lambda: send_script("u_rt.txt"), width=10) 
btn_u_rt.grid(row=4, column=2, padx=5, pady=5)

# Column 1
btn_u5_up = tk.Button(root, text="u5_up", command=lambda: send_script("u5_up.txt"), width=10)
btn_u5_up.grid(row=5, column=0, padx=5, pady=5)

btn_v5_up = tk.Button(root, text="v5_up", command=lambda: send_script("v5_up.txt"), width=10)
btn_v5_up.grid(row=6, column=0, padx=5, pady=5)

btn_v5_dn = tk.Button(root, text="v5_dn", command=lambda: send_script("v5_dn.txt"), width=10)
btn_v5_dn.grid(row=7, column=0, padx=5, pady=5)

btn_u5_dn = tk.Button(root, text="u5_dn", command=lambda: send_script("u5_dn.txt"), width=10)
btn_u5_dn.grid(row=8, column=0, padx=5, pady=5)

# Column 2
btn_l5_xx = tk.Button(root, text="l5_xx", command=lambda: send_script("l5_xx.txt"), width=10, bg="yellow")
btn_l5_xx.grid(row=5, column=1, padx=5, pady=5)

btn_l5_yy = tk.Button(root, text="l5_yy", command=lambda: send_script("l5_yy.txt"), width=10, bg="yellow")
btn_l5_yy.grid(row=6, column=1, padx=5, pady=5)

btn_p5_luss = tk.Button(root, text="p5_luss", command=lambda: send_script("p5_luss.txt"), width=10)
btn_p5_luss.grid(row=7, column=1, padx=5, pady=5)

btn_c5_ross = tk.Button(root, text="c5_ross", command=lambda: send_script("c5_ross.txt"), width=10)
btn_c5_ross.grid(row=8, column=1, padx=5, pady=5)


# Column 3
btn_u5_lt = tk.Button(root, text="u5_lt", command=lambda: send_script("u5_lt.txt"), width=10)
btn_u5_lt.grid(row=5, column=2, padx=5, pady=5)

btn_v5_lt = tk.Button(root, text="v5_lt", command=lambda: send_script("v5_lt.txt"), width=10)
btn_v5_lt.grid(row=6, column=2, padx=5, pady=5)

btn_v5_rt = tk.Button(root, text="v5_rt", command=lambda: send_script("v5_rt.txt"), width=10)
btn_v5_rt.grid(row=7, column=2, padx=5, pady=5)

btn_u5_rt = tk.Button(root, text="u5_rt", command=lambda: send_script("u5_rt.txt"), width=10)
btn_u5_rt.grid(row=8, column=2, padx=5, pady=5)

root.mainloop()



