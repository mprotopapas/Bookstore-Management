import tkinter as tk
from tkinter import messagebox
from data_loader import save_data,load_data

# Validates the username by checking if it's included in admin or user df
def validate_username(username, user_df, admin_df):
    return username in user_df['username'].values or username in admin_df['username'].values

# Same deal as above, checks if the password matches
def validate_password(username, password, user_df, admin_df):
    if username in user_df['username'].values:
        return user_df[user_df['username'] == username]['password'].values[0] == password
    elif username in admin_df['username'].values:
        return admin_df[admin_df['username'] == username]['password'].values[0] == password
    return False

# Draws the registration menu
def register_user(user_df, admin_df, books_df):

    # submits the new user data
    def submit_registration():
        username = username_entry.get()
        password = password_entry.get()
        address = address_entry.get()
        city = city_entry.get()
        
        # checks if the username already exists
        if username in user_df['username'].values:
            messagebox.showerror("Error", "Username already exists.")
            return
        # checks if the password is longer than 8 chars and if it contains special chars
        if len(password) < 8 or not any(char in '!@#$%^&*()-_=+[]{};:,.<>?/\\|' for char in password):
            messagebox.showerror("Error", "Password must be at least 8 characters long and contain a special character.")
            return
        
        new_user = {
            'id': user_df['id'].max() + 1,
            'username': username,
            'password': password,
            'address': address,
            'city': city,
            'orders': [],
            'favorites': [],
            'balance': 0.0
        }
        
        user_df.loc[len(user_df)] = new_user
        save_data(user_df, admin_df, books_df)
        messagebox.showinfo("Success", "User registered successfully!")
        registration_window.destroy()
    
    registration_window = tk.Toplevel()
    registration_window.title("Register")
    registration_window.geometry("200x210")

    tk.Label(registration_window, text="Username").pack()
    username_entry = tk.Entry(registration_window)
    username_entry.pack()

    tk.Label(registration_window, text="Password").pack()
    password_entry = tk.Entry(registration_window, show='*')
    password_entry.pack()

    tk.Label(registration_window, text="Address").pack()
    address_entry = tk.Entry(registration_window)
    address_entry.pack()

    tk.Label(registration_window, text="City").pack()
    city_entry = tk.Entry(registration_window)
    city_entry.pack()

    tk.Button(registration_window, text="Submit", command=submit_registration).pack()
# draws the login menu
def login_system(user_df, admin_df, books_df, save_data, admin_menu, user_menu):


    # Checks the entry data and guides the user/admin to the correct menu
    def submit_login():
        global user_df, admin_df, books_df
        user_df, admin_df, books_df = load_data()
        username = username_entry.get()
        password = password_entry.get()
        
        if validate_username(username, user_df, admin_df) and validate_password(username, password, user_df, admin_df):
            messagebox.showinfo("Success", "Login successful!")
            login_window.destroy()
            if username in admin_df['username'].values:
                admin_menu(username, books_df, admin_df, user_df)
            else:
                user_menu(username, user_df, books_df)
        else:
            global attempts
            attempts += 1
            if attempts >= 3:
                messagebox.showerror("Error", "Too many wrong attempts.")
                exit()
            else:
                messagebox.showerror("Error", f"Incorrect credentials. {3 - attempts} attempts left.")
    
    global attempts 
    attempts = 0
    login_window = tk.Toplevel()
    login_window.title("Login")

    tk.Label(login_window, text="Username").pack()
    username_entry = tk.Entry(login_window)
    username_entry.pack()

    tk.Label(login_window, text="Password").pack()
    password_entry = tk.Entry(login_window, show='*')
    password_entry.pack()

    tk.Button(login_window, text="Submit", command=submit_login).pack()