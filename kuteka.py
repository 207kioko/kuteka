import streamlit as st
import tkinter as tk
import time
import random
from threading import Thread

# Setup window
root = tk.Tk()
root.title("A Little Something For You ❤️")
root.geometry("600x500")
root.config(bg="misty rose")

message_label = tk.Label(root, text="", font=("Georgia", 16), bg="misty rose", fg="dark red", justify="center")
message_label.pack(pady=20)

poem_label = tk.Label(root, text="", font=("Times New Roman", 14, "italic"), bg="misty rose", fg="purple", justify="center")
poem_label.pack(pady=10)

canvas = tk.Canvas(root, width=600, height=250, bg="misty rose", highlightthickness=0)
canvas.pack()

# Typing effect
def type_message(label, msg, delay=0.05):
    label.config(text="")
    for i in range(len(msg) + 1):
        label.config(text=msg[:i])
        time.sleep(delay)

# Floating hearts animation
def floating_hearts():
    heart_colors = ["red", "deep pink", "hot pink", "magenta"]
    hearts = []
    for _ in range(20):
        x = random.randint(50, 550)
        y = random.randint(50, 200)
        heart = canvas.create_text(x, y, text="❤️", font=("Arial", 20), fill=random.choice(heart_colors))
        hearts.append(heart)
    for _ in range(40):
        for h in hearts:
            canvas.move(h, 0, -1)
        root.update()
        time.sleep(0.05)

# Yes/No button actions
def say_yes():
    btn_yes.place_forget()
    btn_no.place_forget()
    poem_label.config(text="")
    message_label.config(fg="green")
    Thread(target=type_message, args=(message_label, "YES!!! 💍 You've made me the happiest human ever 💖💖💖",)).start()
    floating_hearts()

def say_no():
    btn_yes.place_forget()
    btn_no.place_forget()
    poem_label.config(text="")
    message_label.config(fg="gray")
    Thread(target=type_message, args=(message_label, "Aww... That's okay. Still sending love & smiles your way 💔😊",)).start()

# Buttons
btn_yes = tk.Button(root, text="Yes 💘", font=("Helvetica", 14, "bold"), bg="lightgreen", command=say_yes)
btn_no = tk.Button(root, text="No 💔", font=("Helvetica", 14, "bold"), bg="lightcoral", command=say_no)

# The romantic sequence
def love_story():
    Thread(target=type_message, args=(message_label, "Hey you... 🌸\nThere's something I've been wanting to tell you.",)).start()
    time.sleep(4)
    Thread(target=type_message, args=(message_label, "Every time I see you, my heart skips a beat. 💓")).start()
    time.sleep(4)
    Thread(target=type_message, args=(message_label, "You light up my world in ways I can't explain... ✨")).start()
    time.sleep(4)
    Thread(target=type_message, args=(poem_label, "\nRoses are red,\nViolets are blue,\nLife is sweeter,\nWhenever I'm with you 🌹")).start()
    time.sleep(5)
    Thread(target=type_message, args=(message_label, "\nSo here's my little question... 😊",)).start()
    time.sleep(4)
    Thread(target=type_message, args=(message_label, "Will you be my girlfriend? 💖",)).start()
    time.sleep(3)
    btn_yes.place(x=180, y=420)
    btn_no.place(x=330, y=420)

# Start the love story after window loads
root.after(1000, lambda: Thread(target=love_story).start())

root.mainloop()
