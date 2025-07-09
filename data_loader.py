import pandas as pd
import ast


user_df = None
admin_df = None
books_df = None

def load_data():
    # Set global to allow global modification
    global user_df, admin_df, books_df
    user_df = pd.read_csv('Desktop/Pythonexercise/users.csv')
    admin_df = pd.read_csv('Desktop/Pythonexercise/admins.csv')
    books_df = pd.read_csv('Desktop/Pythonexercise/books.csv')

    # Attempts to evaluate all the incoming data  and returns it accordingly. 
    def safe_literal_eval(val):
        try:
            return ast.literal_eval(val) if not pd.isna(val) else []
        # if an exception if found such as a value error or a syntax error, return the value using comma to split it if it's a string, otherwise return an empty list.
        except (ValueError, SyntaxError):
            if isinstance(val, str):
                return val.split(',')
            return []
    #  match and load the data to the according frames.
    if 'orders' in user_df.columns:
        user_df['orders'] = user_df['orders'].apply(safe_literal_eval)
    else:
        user_df['orders'] = []

    if 'favorites' in user_df.columns:
        user_df['favorites'] = user_df['favorites'].apply(safe_literal_eval)
    else:
        user_df['favorites'] = []

    if 'bookstores' in admin_df.columns:
        admin_df['bookstores'] = admin_df['bookstores'].apply(safe_literal_eval)
    else:
        admin_df['bookstores'] = []

    if 'categories' in books_df.columns:
        books_df['categories'] = books_df['categories'].apply(safe_literal_eval)
    else:
        books_df['categories'] = []

    if 'bookstores' in books_df.columns:
        books_df['bookstores'] = books_df['bookstores'].apply(safe_literal_eval)
    else:
        books_df['bookstores'] = []
    
    if 'reviews' in books_df.columns:
        books_df['reviews'] = books_df['reviews'].apply(safe_literal_eval)
    else:
        books_df['reviews'] = []
    if 'ratings' in books_df.columns:
        books_df['ratings'] = books_df['ratings'].apply(safe_literal_eval)
    else:
        books_df['ratings']=[]

    return user_df, admin_df, books_df

def save_data(user_df, admin_df=None, books_df=None, new_user_data=None, new_book_data=None):
    # If new user data is located, add it
    if new_user_data is not None:
        user_df = user_df.append(new_user_data, ignore_index=True)
    user_df.to_csv('Desktop/Pythonexercise/users.csv', index=False)
    # if admin data is not none, add it
    if admin_df is not None:
        admin_df.to_csv('Desktop/Pythonexercise/admins.csv', index=False)
        # if book data is not none, add it
    if books_df is not None:
        if new_book_data is not None:
            books_df = books_df.append(new_book_data, ignore_index=True)
        books_df.to_csv('Desktop/Pythonexercise/books.csv', index=False)

    # load the new data (failsafe)
    load_data()