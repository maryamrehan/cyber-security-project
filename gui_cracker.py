import tkinter as tk
from tkinter import messagebox
import itertools
import string
import time
import threading

# Dictionary Attack Function
def dictionary_attack(target_password, update_status):
    start_time = time.time()
    attempts = 0

    try:
        with open("wordlist.txt", "r") as file:
            for line in file:
                word = line.strip()
                attempts += 1
                update_status(f"Trying: {word} (Attempt {attempts})")
                time.sleep(0.01)

                if word == target_password:
                    end_time = time.time()
                    messagebox.showinfo("Success", f"Password cracked!\nPassword: {word}\nAttempts: {attempts}\nTime: {end_time - start_time:.2f}s")
                    return
    except FileNotFoundError:
        messagebox.showerror("Error", "wordlist.txt not found.")
        return

    messagebox.showwarning("Failed", "Password not found in dictionary.")

# Brute Force Function
def brute_force_attack(target_password, max_length, update_status):
    chars = string.ascii_letters + string.digits + "!@#$%&*"
    attempts = 0
    start_time = time.time()

    for length in range(1, max_length + 1):
        for guess in itertools.product(chars, repeat=length):
            guess_password = ''.join(guess)
            attempts += 1
            update_status(f"Trying: {guess_password} (Attempt {attempts})")

            if guess_password == target_password:
                end_time = time.time()
                messagebox.showinfo("Success", f"Password cracked!\nPassword: {guess_password}\nAttempts: {attempts}\nTime: {end_time - start_time:.2f}s")
                return

    messagebox.showwarning("Failed", "Could not crack the password.")

# Start Attack in a new thread
def start_attack():
    password = entry_password.get()
    method = attack_method.get()
    max_length = entry_maxlen.get()

    if not password:
        messagebox.showerror("Error", "Please enter a password.")
        return

    if method == "brute":
        try:
            max_len = int(max_length)
        except ValueError:
            messagebox.showerror("Error", "Enter valid number for max length.")
            return

        threading.Thread(target=brute_force_attack, args=(password, max_len, update_status)).start()

    elif method == "dictionary":
        threading.Thread(target=dictionary_attack, args=(password, update_status)).start()
    else:
        messagebox.showerror("Error", "Choose an attack method.")

# Status update function
def update_status(message):
    label_status.config(text=message)
    root.update_idletasks()

# GUI Setup
root = tk.Tk()
root.title("🧠 Brute Force Password Cracker (GUI Tool)")
root.geometry("450x300")
root.resizable(False, False)

tk.Label(root, text="🔐 Enter Password to Crack:", font=("Arial", 12)).pack(pady=5)
entry_password = tk.Entry(root, show="*", font=("Arial", 12), width=30)
entry_password.pack()

tk.Label(root, text="🧰 Choose Attack Method:", font=("Arial", 12)).pack(pady=10)
attack_method = tk.StringVar()

tk.Radiobutton(root, text="Dictionary Attack", variable=attack_method, value="dictionary", font=("Arial", 11)).pack()
tk.Radiobutton(root, text="Brute Force Attack", variable=attack_method, value="brute", font=("Arial", 11)).pack()

tk.Label(root, text="⏳ Max Length (for brute-force):", font=("Arial", 12)).pack(pady=5)
entry_maxlen = tk.Entry(root, font=("Arial", 12))
entry_maxlen.pack()

tk.Button(root, text="🚀 Start Cracking", font=("Arial", 12, "bold"), command=start_attack, bg="green", fg="white").pack(pady=15)

label_status = tk.Label(root, text="🟢 Status: Waiting...", font=("Arial", 11))
label_status.pack()

root.mainloop()
