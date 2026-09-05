import tkinter as tk 
from tkinter import font
import re

ALLOWED_RE = re.compile(r'^[0-9\.\+\-\*\/\%\(\) ]*$')

def safe_eval(expr):
    expr = expr.strip()
    if not expr:
        return ''
    if not ALLOWED_RE.match(expr):
        raise ValueError("Ekspresi mengandung karakter tidak diperbolehkan.")
   
    return eval(expr)

root = tk.Tk()
root.title("Floating Calculator")
root.geometry("360x500+200+200") 
root.overrideredirect(True)        
root.attributes("-topmost", True) 
root.attributes("-alpha", 0.95)     

# Warna & font
BG = "#000000"
FG = "#FFFFFF"
ACC = "#000dff"
btn_font = ("Helvetica", 14, "bold")
display_font = ("Consolas", 20)

# ----- Header (drag + close) -----
header = tk.Frame(root, bg=BG, relief="flat")
header.pack(fill="x")

title = tk.Label(header, text="  Calculator", bg=BG, fg=FG, anchor="w", font=("Helvetica", 10))
title.pack(side="left", padx=6, pady=6)

def on_close():
    root.destroy()

close_btn = tk.Button(header, text="✕", command=on_close, bg=BG, fg=FG, bd=0, activebackground="#d20000")
close_btn.pack(side="right", padx=6)

# Dragging behavior
def start_move(event):
    root.x_offset = event.x
    root.y_offset = event.y

def do_move(event):
    x = root.winfo_pointerx() - root.x_offset
    y = root.winfo_pointery() - root.y_offset
    root.geometry(f"+{x}+{y}")

header.bind("<Button-1>", start_move)
header.bind("<B1-Motion>", do_move)
title.bind("<Button-1>", start_move)
title.bind("<B1-Motion>", do_move)

# ----- Display -----
display_var = tk.StringVar()
display = tk.Entry(root, textvariable=display_var, font=display_font, bd=0, justify="right", bg="#1e2126", fg=FG, insertbackground=FG)
display.pack(fill="x", padx=9, pady=(5,8), ipady=10)

# Meng-handle input keyboard (Enter = hitung, Esc = clear)
def on_key(event):
    if event.keysym == "Return":
        hitung()
    elif event.keysym == "Escape":
        clear_all()

root.bind_all("<Key>", on_key)

# ----- Button grid -----
btns = [
    ['1', '2', '3',], 
    ['4', '5', '6',],
    ['7', '8', '9',],
    ['0', '+', '-',],
    ['*', '/', '%',],
    ['(', ')', '=',],    
]

frame = tk.Frame(root, bg=BG)
frame.pack(padx=8, pady=6)

def press(val):
    if val == 'C':
        clear_all()
    elif val == '=':
        hitung()
    else:
        # tambahkan ke display
        display_var.set(display_var.get() + val)

def clear_all():
    display_var.set("")

def hitung():
    expr = display_var.get()
    try: 
        result = safe_eval(expr)
        display_var.set(str(result))
    except Exception as e:
        display_var.set("Error")
        # Hapus pesan Error setelah 1 detik
        root.after(1000, lambda: display_var.set(""))

# Buat tombol
for r, row in enumerate(btns):
    for c, ch in enumerate(row):
        if ch == '=':
            b = tk.Button(frame, text=ch, width=6, height=2, font=btn_font, command=lambda v=ch: press(v),
                          bg=ACC, fg="black", bd=0, activebackground="#49a1ff")
        elif ch == 'C':
            b = tk.Button(frame, text=ch, width=6, height=2, font=btn_font, command=lambda v=ch: press(v),
                          bg="#ea2828", fg="white", bd=0, activebackground="#ff4c4c")
        else:
            b = tk.Button(frame, text=ch, width=6, height=2, font=btn_font, command=lambda v=ch: press(v),
                          bg="#ff0000", fg=FG, bd=0, activebackground="#FEFEFE")
        b.grid(row=r, column=c, padx=4, pady=4)

# ----- Optional: klik kanan -> minimize / restore -----
menu = tk.Menu(root, tearoff=0)
def minimize():
    root.withdraw()
def restore(event=None):
    root.deiconify()

menu.add_command(label="Minimize", command=minimize)
menu.add_command(label="Close", command=on_close)

def show_menu(event):
    menu.tk_popup(event.x_root, event.y_root)

root.bind("<Button-3>", show_menu)  # klik kanan buka menu
# restore dengan double-click header  
header.bind("<Double-Button-1>", lambda e: restore())

# Jalankan
root.mainloop()
