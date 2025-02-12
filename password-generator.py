import random
import string
import tkinter as tk
from tkinter import messagebox
import pyperclip

# Set to store used passwords
used_passwords = set()

def check_password_strength(password):
    """Checks password strength and returns a rating"""
    score = 0
    if len(password) >= 8:
        score += 1
    if any(char.isdigit() for char in password):
        score += 1
    if any(char.isupper() for char in password):
        score += 1
    if any(char in string.punctuation for char in password):
        score += 1

    if score == 4:
        return "Strong"
    elif score == 3:
        return "Medium"
    else:
        return "Weak"

def generate_password(length=12, complexity="Strong"):
    """Generates a unique random password based on user preferences."""
    if complexity == "Easy":
        characters = string.ascii_lowercase  # Only lowercase letters
    elif complexity == "Medium":
        characters = string.ascii_letters + string.digits  # Letters + Numbers
    else:
        characters = string.ascii_letters + string.digits + string.punctuation  # Full complexity
    
    while True:
        password = ''.join(random.choice(characters) for _ in range(length))
        if password not in used_passwords:
            used_passwords.add(password)
            return password

def save_to_file(password):
    """Saves password to a file"""
    with open("generated_passwords.txt", "a") as file:
        file.write(password + "\n")
    messagebox.showinfo("Saved", "Password saved to 'generated_passwords.txt'.")

def copy_to_clipboard():
    """Copies the generated password to clipboard"""
    password = password_label.cget("text").replace("Generated Password:\n", "")
    if password and password != "Generated Password:":
        pyperclip.copy(password)
        messagebox.showinfo("Copied", "Password copied to clipboard!")
    else:
        messagebox.showerror("Error", "No password to copy!")

def generate_and_display():
    """Generates password and displays it in the GUI"""
    try:
        length = int(length_entry.get())
        if length < 1:
            messagebox.showerror("Error", "Password length must be at least 1.")
            return
    except ValueError:
        messagebox.showerror("Error", "Please enter a valid number.")
        return

    complexity = complexity_var.get()
    password = generate_password(length, complexity)
    strength = check_password_strength(password)

    password_label.config(text=f"Generated Password:\n{password}\nStrength: {strength}")

def save_password():
    """Saves the displayed password to a file"""
    password = password_label.cget("text").replace("Generated Password:\n", "").split("\n")[0]
    if password and password != "Generated Password:":
        save_to_file(password)
    else:
        messagebox.showerror("Error", "No password to save!")

# GUI Setup
root = tk.Tk()
root.title("Password Generator")
root.geometry("400x350")

# UI Elements
tk.Label(root, text="Enter Password Length:").pack()
length_entry = tk.Entry(root)
length_entry.pack()

tk.Label(root, text="Select Complexity Level:").pack()
complexity_var = tk.StringVar(value="Strong")
tk.Radiobutton(root, text="Easy (Only letters)", variable=complexity_var, value="Easy").pack()
tk.Radiobutton(root, text="Medium (Letters + Numbers)", variable=complexity_var, value="Medium").pack()
tk.Radiobutton(root, text="Strong (Letters + Numbers + Special)", variable=complexity_var, value="Strong").pack()

generate_button = tk.Button(root, text="Generate Password", command=generate_and_display)
generate_button.pack(pady=10)

password_label = tk.Label(root, text="Generated Password:\n", font=("Arial", 12))
password_label.pack()

copy_button = tk.Button(root, text="Copy to Clipboard", command=copy_to_clipboard)
copy_button.pack(pady=5)

save_button = tk.Button(root, text="Save Password", command=save_password)
save_button.pack(pady=5)

root.mainloop()
