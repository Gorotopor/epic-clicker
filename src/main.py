import threading
import time
import tkinter as tk
from PIL import Image, ImageTk
import os
from tkinter import messagebox
from pathlib import Path
import sys

if sys.platform == "win32":
    import ctypes
    myappid = "org.gorotopor.epicclicker"
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)


window = tk.Tk()
window.title("epic clicker")
curr_folder = Path(__file__).resolve().parent.parent
icon_path = curr_folder / "ecimages" / "cookieface.png"
icon = tk.PhotoImage(file=icon_path)
window.iconphoto(True, icon)
cps = cookies = 0
cursor_count = cursor_upgrades = cursor_available_upgrades =  0
grandma_count  = grandma_upgrades =  grandma_available_upgrades = 0
rj45_count = rj45_upgrades = rj45_available_upgrades = 0
rapper_count = rapper_upgrades = rapper_available_upgrades = 0
cookies_on_click = 1
flag = flag1 = None
lock = threading.Lock()
user_save_file = curr_folder / "ecstats.txt"
stats = {"cursor_count": "0",
         "cps": "0",
         "cookies": "0",
         "grandma_count": "0",
         "cursor_upgrades": "0",
         "grandma_upgrades": "0",
         "rj45_count": "0",
         "rj45_upgrades": "0",
         "rapper_count": "0",
         "rapper_upgrades": "0"}
if not os.path.exists(user_save_file):
    with open(user_save_file, "w") as file:
        for i, j in stats.items():
            file.write(i + ":" + j + "\n")
else:
    loaded_stats = {}
    with open(user_save_file, 'r') as file:
        for line in file:
            key, value = line.strip().split(":")
            loaded_stats[key] = value
    for key in loaded_stats:
        globals()[key] = (float(loaded_stats[key]))


def second():
    global cookies
    global cookies_shown
    global cps
    while True:
        with lock:
            cookies += round(cps/10, 2)
            cookies_shown.set(round(cookies, 1))
            window.update_idletasks()
            cookies_displayed.set(f"Cookies: {cookies_shown.get()}")
            stats.update({"Cursors: ": str(cursor_count),
                          "\nCookies per second: ": str(cps)})
            cps_shown.set(str(round(cps, 1)))
            cps_shown_variable.set(f"Cookies per second: {cps_shown.get()}")
        time.sleep(0.1)


right_frame = tk.Frame(window)
right_frame.pack(side="right", anchor="n", padx=10, pady=10)
middle_frame = tk.Frame(window)
middle_frame.pack(side="right", anchor="n", padx=200, pady=10)
word_upgrades = tk.Label(window, text="Upgrades", font=("Courier", 40))
word_upgrades.place(x=500, y=430)
class Building:
    def __init__(self, name, base_cost, rate, source, count, text, distance, icon, color, bought_upgrades,
                 available_upgrades):
        self.upgrade_reqs = [10, 25, 50, 75, 100, 150, 200, 300]
        self.bought_upgrades = bought_upgrades
        self.name = name
        self.base_rate = rate
        self.rate = rate
        self.available_upgrades = available_upgrades
        for i in range(int(self.bought_upgrades)):
            self.upgrade_reqs.pop(0)
        self.count = count
        self.base_cost = base_cost
        if self.count == 0:
            self.cost = base_cost
        else:
            exponent = pow(1.15, self.count)
            self.cost = round(self.base_cost*exponent, 1)
        self.source = ImageTk.PhotoImage(Image.open(source))
        self.buy_button = tk.Button(right_frame, command = self.buy, image=self.source,
                                 relief="groove", borderwidth=3)
        self.buy_button.pack()
        self.price_text = tk.StringVar()
        self.price_text.set(self.name + " price: " + str(self.cost))
        self.full_price = tk.Label(right_frame, textvariable=self.price_text, bg="gray")
        self.full_price.pack()
        self.count_text = tk.StringVar()
        self.count_text.set(self.name + " count: " + str(int(self.count)))
        self.full_count = tk.Label(middle_frame, textvariable=self.count_text, bg="cyan", borderwidth=5,
                                        relief="sunken", font=("Gothic", 16, "bold"))
        self.full_count.pack()
        self.text = text
        self.desc_window = None
        self.buy_button.bind("<Enter>", self.show_desc)
        self.buy_button.bind("<Leave>", self.hide_desc)
        self.distance = distance
        self.icon = icon
        base_icon = Image.open(icon).convert("RGBA")
        overlay = Image.new("RGBA", base_icon.size, color)
        upg_icon = Image.alpha_composite(base_icon, overlay)
        self.pi_icon = ImageTk.PhotoImage(upg_icon)
        self.upg_button = tk.Button(window, command=self.buy_upg, image=self.pi_icon)
        self.upg_button.bind("<Enter>", self.show_upg_desc)
        self.upg_button.bind("<Leave>", self.hide_upg_desc)
        if self.count >= self.upgrade_reqs[0]:
            self.upg_button.place(x=500 + self.distance, y=500)


    def buy(self):
        global cookies, cps
        if cookies < self.cost:
            show_necnot()
        else:
            cookies -= self.cost
            self.count += 1
            if self.count == 10:
                self.upg_button.place(x=500 + self.distance, y=500)
            self.cost = round(self.cost * 1.15, 1)
            cps += round(self.rate, 1)
            self.price_text.set(self.name + " price: " + str(self.cost))
            self.count_text.set(self.name + " count: " + str(int(self.count)))
            if self.upgrade_reqs:
                if self.count >= self.upgrade_reqs[0]:
                    self.available_upgrades += 1
                    self.upg_button.place(x=500 + self.distance, y=500)
                    self.upgrade_reqs.pop(0)


    def buy_upg(self):
        global cps, cookies
        if cookies < self.base_cost * (self.bought_upgrades+2) * 20**self.bought_upgrades:
            show_necnot()
        else:
            self.available_upgrades -= 1
            self.bought_upgrades += 1
            cookies -= self.base_cost * (self.bought_upgrades+1) * 20**(self.bought_upgrades-1)
            cps -= round(self.rate * self.count, 1)
            self.rate *= 5
            cps += round(self.rate * self.count, 1)
            self.hide_upg_desc()
            self.show_upg_desc()
            if self.available_upgrades == 0:
                self.upg_button.place_forget()


    def show_desc(self, event=None):  # idk if you can remove the event=None  no you cannot
        if self.desc_window:
            return
        x = self.buy_button.winfo_rootx() + 30
        y = self.buy_button.winfo_rooty() + self.buy_button.winfo_height() + 5
        self.desc_window = dwindow = tk.Toplevel(self.buy_button)
        dwindow.wm_overrideredirect(True)
        dwindow.wm_geometry(f"+{x}+{y}")
        desc_label = tk.Label(dwindow, text="Cps: " + str(self.base_rate * pow(2, self.bought_upgrades)), bg="lime")
        desc_label.pack(ipadx=5, ipady=2)


    def hide_desc(self, event=None):
        dwindow = self.desc_window
        if dwindow:
            dwindow.destroy()
        self.desc_window = None


    def show_upg_desc(self, event=None):  # idk if you can remove the event=None  no you cannot
        if self.desc_window:
            return
        x = self.upg_button.winfo_rootx() + 30
        y = self.upg_button.winfo_rooty() + self.upg_button.winfo_height() + 5
        self.desc_window = dwindow = tk.Toplevel(self.upg_button)
        dwindow.wm_overrideredirect(True)
        dwindow.wm_geometry(f"+{x}+{y}")
        upg_cost = self.base_cost * (self.bought_upgrades+2) * 20**self.bought_upgrades
        desc_label = tk.Label(dwindow, bg="lime", text="Cost: " + str(upg_cost)+f"\n Quintuples {self.name} production")
        desc_label.pack(ipadx=5, ipady=2)


    def hide_upg_desc(self, event=None):
        dwindow = self.desc_window
        if dwindow:
            dwindow.destroy()
        self.desc_window = None


Cursor = Building("Cursor", 15, 0.1,
                  curr_folder / "ecimages" / "cursor.png", count=cursor_count,
                  text="Cps: ", distance=0, icon=curr_folder / "ecimages" / "cursor_upg.png",
                  color=(255, 0, 0, 100), bought_upgrades=cursor_upgrades,
                  available_upgrades=cursor_available_upgrades)
Grandma = Building("Grandma", 100, 10,
                  curr_folder / "ecimages" / "grandma.png", count=grandma_count,
                  text="Cps: ", distance=100, icon=curr_folder / "ecimages" / "grandma_upg.png",
                  color=(0, 255, 0, 100), bought_upgrades=grandma_upgrades,
                  available_upgrades=grandma_available_upgrades)
rj45 = Building("rj45", 1500, 12000,
                  curr_folder / "ecimages" / "rj45.png", count=rj45_count,
                  text="Cps: ", distance=200, icon = curr_folder / "ecimages" / "rj45_upg.png",
                  color = (0, 0, 255, 100), bought_upgrades=rj45_upgrades,
                  available_upgrades=rj45_available_upgrades)
rapper = Building("rodeo rapper", 300000, 50000000,
                  curr_folder / "ecimages" / "rapper.png", count=rapper_count,
                  text="Cps: ",distance=300, icon = curr_folder / "ecimages" / "rapper_upg.png",
                  color = (255, 255, 0, 100), bought_upgrades=rapper_upgrades,
                  available_upgrades=rapper_available_upgrades)

window.geometry("1920x1080")
cookie = Image.open(curr_folder / "ecimages" / "cokie.png").convert("RGBA")
tkcookie = ImageTk.PhotoImage(cookie)


def on_click(event):
    global cookies, cookie_display
    x, y = event.x, event.y
    if 0 <= x < cookie.width and 0 <= y < cookie.height:
        r, g, b, a = cookie.getpixel((x, y))
        if a == 0:
            pass
        else:
            cookies += cookies_on_click
            cookies_shown.set(str(round(cookies, 1)))


clickable = tk.Button(window, image=tkcookie, relief="flat", borderwidth=0, compound="left")
clickable.place(x=60, y=200)
clickable.bind("<Button-1>", on_click)
cookies_shown = tk.StringVar(value=str(cookies))
cookies_displayed = tk.StringVar()
cookies_displayed.set("Cookies: 0")
cps_shown = tk.StringVar(value=str(cps))
cps_shown_variable = tk.StringVar()
cps_shown_variable.set("Cps: 0")
cookie_display = tk.Label(window, textvariable=cookies_displayed, bg="red", font=("Hellvetica", 15, "bold"))
cookie_display.place(x=500, y=0)
cps_display = tk.Label(window, textvariable=cps_shown_variable, bg="yellow", font=("Arial", 13, "bold"))
cps_display.place(x=500, y=50)


def custom_exit(title, question):
    popup = tk.Toplevel()
    popup.title(title)
    popup.geometry("0x60")
    tk.Label(popup, text=question).pack()
    answer = {"value": False}


    def yes():
        answer["value"] = True
        popup.destroy()


    def no():
        answer["value"] = False
        popup.destroy()


    tk.Button(popup, command=yes, text="Yes").pack(side="left")
    tk.Button(popup, command=no, text="No").pack(side="right")
    popup.update_idletasks()
    screen_width = popup.winfo_screenwidth()
    screen_height = popup.winfo_screenheight()
    window_width = popup.winfo_width()
    window_height = popup.winfo_height()
    x = (screen_width // 2) - (window_width // 2)
    y = (screen_height // 2) - (window_height // 2)
    popup.geometry(f"+{x}+{y}")
    popup.transient(window)
    popup.grab_set()
    window.wait_window(popup)

    return answer["value"]


def on_closing():
    response = custom_exit("Confirm", "Do you want to exit?")
    if response:
        saving_response = messagebox.askyesnocancel(title="Saving", message="Do you want to save?", icon="question")
        if saving_response:
            newstats = {"cursor_count": Cursor.count,
                        "cps": round(cps, 1),
                        "cookies": round(cookies, 1),
                        "grandma_count": Grandma.count,
                        "cursor_upgrades": Cursor.bought_upgrades,
                        "grandma_upgrades": Grandma.bought_upgrades,
                        "cursor_available_upgrades": Cursor.available_upgrades,
                        "grandma_available_upgrades": Grandma.available_upgrades,
                        "rj45_count": rj45.count,
                        "rj45_upgrades": rj45.bought_upgrades,
                        "rj45_available_upgrades": rj45.available_upgrades,
                        "rapper_count": rapper.count,
                        "rapper_upgrades": rapper.bought_upgrades,
                        "rapper_available_upgrades": rapper.available_upgrades}

            with open(user_save_file, "w") as file:
                for i, j in newstats.items():
                    file.write(i + ":" + str(j) + "\n")
            window.quit()
        elif saving_response is None:
            return
        else:
            window.quit()


def show_tut():
    global flag1
    tutorial.place(x=150, y=320)
    flag1 = window.after(5000, forget_tut)


def forget_tut():
    global flag1
    tutorial.place_forget()
    flag1 = None


def show_necnot():
    global flag
    nec_not.place(x=400, y=100)
    if flag:
        window.after_cancel(flag)
    flag = window.after(5000, forget_necnot)


def forget_necnot():
    global flag
    nec_not.place_forget()
    flag = None


def delete_save():
    delete_response = messagebox.askyesno(title="Deleting", message="Do you want to delete your save?", icon="question")
    if delete_response:
        os.remove(user_save_file)
        messagebox.showwarning(title="File deleted", message="Save deleted.")
        window.destroy()
    else:
        return


tutorial = tk.Button(window, text="tutorial", font=("Arial", 40), command=show_tut)
tutorial.place(x=100, y=0)
delete = tk.Button(window, text="delete save", font=("Arial", 10), command=delete_save)
delete.place(x=0, y=0)
nec_not = tk.Label(window, text="You don't have enough cookies!", font=("Times New Roman", 20, "bold"))
window.protocol("WM_DELETE_WINDOW", on_closing)
s1 = threading.Thread(target=second, daemon=True)
s1.start()
window.mainloop()
