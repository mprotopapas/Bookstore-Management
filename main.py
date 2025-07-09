import tkinter as tk
from data_loader import load_data, save_data
from authentication import register_user, login_system
from admin_actions import admin_menu
from user_actions import user_menu

def main():
    global user_df, admin_df, books_df
    user_df, admin_df, books_df = load_data()

    mprogram = tk.Tk() # set mprogram as tk
    mprogram.title("Bookstore Management System")

    tk.Label(mprogram, text="Welcome to the Bookstore Management System").pack()

    def open_login():
        login_system(user_df, admin_df, books_df, save_data, admin_menu, user_menu)

    def open_registration():
        register_user(user_df, admin_df, books_df)

    tk.Button(mprogram, text="Login", command=open_login).pack()
    tk.Button(mprogram, text="Register", command=open_registration).pack()
    tk.Button(mprogram, text="Exit", command=mprogram.destroy).pack()

    mprogram.mainloop() #set it as mainloop  so the program doesn't end

# call main 
main()
