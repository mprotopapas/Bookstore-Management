import tkinter as tk
import os
import pandas as pd
from tkinter import simpledialog, messagebox,filedialog
from collections import defaultdict
from data_loader import save_data,load_data

global user_df, admin_df, books_df
user_df, admin_df, books_df = load_data()

# Draws the user menu
def user_menu(user_username, user_df, books_df):
    user_data = user_df[user_df['username'] == user_username].iloc[0]

    user_window = tk.Toplevel()
    user_window.title("User Menu")
    tk.Label(user_window, text=f"Welcome {user_data['username']}! ", font = 'Helvetica 13 underline',).pack(pady= 10,side='top', anchor="w")
    user_window.geometry("600x700")

    # Imports the damned csv file that the user wants to input
    def import_csv():
        def add_favorites_from_csv():
            csv_file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])


            if not os.path.exists(csv_file_path):
                messagebox.showerror("Error", "File not found.")
                return

            try:
                csv_df = pd.read_csv(csv_file_path)
                if 'title' not in csv_df.columns:
                    messagebox.showerror("Error", "CSV file does not contain a 'title' column.")
                    return

                book_titles_to_add = [title.strip() for title in csv_df['title'].tolist() if title.strip()]
                
                
                added_books = []
                already_favorite_books = []  # Array to keep track of already favorited books
                for title in book_titles_to_add:
                    if title not in user_data['favorites']:
                        user_data['favorites'].append(title)  # Add the title to favorites
                        added_books.append(title)
                    else:
                        already_favorite_books.append(title)

                user_df.loc[user_df['username'] == user_username, 'favorites'] = str(user_data['favorites'])
                save_data(user_df, None, books_df)

                if added_books:
                    messagebox.showinfo("Success", f"Books added to favorites: {', '.join(added_books)}")
                if already_favorite_books:
                    messagebox.showinfo("Info", f"Books already in favorites: {', '.join(already_favorite_books)}")
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred while processing the file: {e}")

        def open_add_favorites_from_csv():
            add_favorites_from_csv()

        csv_management_window= tk.Toplevel()
        csv_management_window.title("Import favorites")
        tk.Button
        tk.Button(csv_management_window, text="Import from csv", command=open_add_favorites_from_csv).pack(pady=3)
        tk.Button(csv_management_window, text="Exit", command=csv_management_window.destroy).pack(pady=3)
    # Function to allow the user to modify their own information
    
    def modify_personal_info():
        def submit_modification():
            global user_df, admin_df, books_df
            user_df, admin_df, books_df = load_data()
            address = address_entry.get() # Get the address from the entry
            city = city_entry.get() # Get the city from the entry
            new_username = username_entry.get() # Get the new username from the entry
            new_password = password_entry.get() # Get the new password from the entry

            if new_username != user_username and new_username in user_df['username'].values:
                messagebox.showerror("Error", "Username already exists. Please choose another one.")
                return

            user_df.loc[user_df['username'] == user_username, 'address'] = address
            user_df.loc[user_df['username'] == user_username, 'city'] = city
            user_df.loc[user_df['username'] == user_username, 'username'] = new_username
            user_df.loc[user_df['username'] == user_username, 'password'] = new_password
            
            save_data(user_df, None, books_df)
            
            messagebox.showinfo("Success", "Information updated successfully!")
            modify_info_window.destroy()
            if new_username != user_username or new_password != user_data['password']:
                user_window.destroy()

        modify_info_window = tk.Toplevel()
        modify_info_window.title("Modify Personal Information")

        tk.Label(modify_info_window, text="Address").pack()
        address_entry = tk.Entry(modify_info_window)
        address_entry.insert(0, user_data['address'])
        address_entry.pack()

        tk.Label(modify_info_window, text="City").pack()
        city_entry = tk.Entry(modify_info_window)
        city_entry.insert(0, user_data['city'])
        city_entry.pack()

        tk.Label(modify_info_window, text="New Username").pack()
        username_entry = tk.Entry(modify_info_window)
        username_entry.insert(0, user_username)
        username_entry.pack()

        tk.Label(modify_info_window, text="New Password").pack()
        password_entry = tk.Entry(modify_info_window)
        password_entry.insert(0, user_data['password'])
        password_entry.pack()

        tk.Button(modify_info_window, text="Submit", command=submit_modification).pack()

    def favorite_actions():
        # Allows the user to add a book to his favourite
        def add_to_favorites():
            book_titles_input = simpledialog.askstring("Input", "Enter book titles to add to favorites (comma-separated):")

            if book_titles_input is None:
                return
            if book_titles_input:
                book_titles_to_add = [title.strip() for title in book_titles_input.split(",") if title.strip()]
                
                added_books = []
                already_favorite_books = []

                for title in book_titles_to_add:
                    if title not in user_data['favorites']:
                        user_data['favorites'].append(title)
                        added_books.append(title)
                    else:
                        already_favorite_books.append(title)

                user_df.loc[user_df['username'] == user_username, 'favorites'] = str(user_data['favorites'])
                save_data(user_df, None, None) 

                if added_books:
                    messagebox.showinfo("Success", f"Books added to favorites: {', '.join(added_books)}")
                if already_favorite_books:
                    messagebox.showinfo("Info", f"Books already in favorites: {', '.join(already_favorite_books)}")
            else:
                messagebox.showerror("Error", "No book titles provided.")

        # Allows the user to remove the book from their favorites
        def remove_from_favorites():
            book_titles_input = simpledialog.askstring("Input", "Enter book titles to remove from favorites (comma-separated):")

            if book_titles_input is None:
                return
            if book_titles_input:
                book_titles_to_remove = [title.strip() for title in book_titles_input.split(",") if title.strip()]

                removed_books = []
                not_in_favorites_books = []
                
                # Check each title in user's favorites
                for title in book_titles_to_remove:
                    if title in user_data['favorites']:
                        user_data['favorites'].remove(title)
                        removed_books.append(title)
                    else:
                        not_in_favorites_books.append(title)

                user_df.loc[user_df['username'] == user_username, 'favorites'] = str(user_data['favorites'])
                save_data(user_df, None, None)  # Only user_df needs to be saved

                if removed_books:
                    messagebox.showinfo("Success", f"Books removed from favorites: {', '.join(removed_books)}")
                if not_in_favorites_books:
                    messagebox.showinfo("Info", f"Books not found in favorites: {', '.join(not_in_favorites_books)}")
            else:
                messagebox.showerror("Error", "No book titles provided.")

        def view_favorites():
            if not user_data['favorites']:
                messagebox.showinfo("Favorites", "You have no favorite books.")
                return

            # Directly uses the favorite books from user_data
            favorites_list = "\n\n".join(user_data['favorites'])
            messagebox.showinfo("Favorite Books", f"Your favorite books:\n\n{favorites_list}")

        # Allows the user to check for availability of liked titles
        def check_favorites_availability_price():
            favorite_books = books_df[books_df['title'].isin(user_data['favorites'])]
            if favorite_books.empty:
                messagebox.showinfo("Favorites Availability and Price", "No favorite books available.")
                return

            book_titles_input = simpledialog.askstring("Input", "Enter book titles to check (comma-separated) or leave empty to check all favorites:")
            if book_titles_input:
                book_titles_to_check = [title.strip().lower() for title in book_titles_input.split(",") if title.strip()]
                books_to_check = favorite_books[favorite_books['title'].str.lower().isin(book_titles_to_check)]
            else:
                books_to_check = favorite_books

            if books_to_check.empty: # If no books are found in the df, rip
                messagebox.showinfo("Error", "No matching favorite books found.")
                return

            available_books = []
            unavailable_books = []
            for idx, book in books_to_check.iterrows():
                if book['availability']:
                    available_books.append((book['title'], book['author'], book['cost'] + book['shipping_cost'], book['bookstores']))
                else:
                    unavailable_books.append(book['title'], book['author'])
            # If books are available
            if available_books:
                availability_info = "\n".join([f"{title} by {author}: ${price} available at {bookstores}" for title, author, price, bookstores in available_books]) # Show them to the user
                messagebox.showinfo("Available Favorite Books", availability_info)
            else:
                messagebox.showinfo("Available Favorite Books", "No favorite books available.")

            if unavailable_books:
                unavailable_info = "\n".join(unavailable_books)
                messagebox.showinfo("Unavailable Favorite Books", f"The following books are currently unavailable:\n{unavailable_info}") # Same thing here but for unavailable
        favorites_window = tk.Toplevel()
        favorites_window.title("Favorites actions")

        tk.Button(favorites_window,text="Import favorites from csv",command=import_csv).pack(pady=3)
        tk.Button(favorites_window, text="Add to Favorites", command=add_to_favorites).pack(pady=3)
        tk.Button(favorites_window,text="View Favorites",command=view_favorites).pack(pady=3)
        tk.Button(favorites_window, text="Remove from Favorites", command=remove_from_favorites).pack(pady=3)
        tk.Button(favorites_window, text="Check Availability and Price of Favorites", command=check_favorites_availability_price).pack(pady=3)
        tk.Button(favorites_window,text="Exit",command=favorites_window.destroy).pack(pady=3)

    def user_wallet():
        # Allows the user to check their balance
        def check_balance():
            messagebox.showinfo("Balance", f"Your current balance is: ${user_data['balance']}")
        # Allows the user to add store credit
        def add_balance():
            amount = simpledialog.askfloat("Input", "Enter amount to add to balance:")
            if amount is None:
                return
            if  amount > 0:
                user_data['balance'] += amount
                user_df.loc[user_df['username'] == user_username, 'balance'] = user_data['balance']
                save_data(user_df, None, books_df)
                messagebox.showinfo("Success", f"Added ${amount} to your balance!")
            else:
                messagebox.showerror("Error", "Invalid amount.")
        # Allows the user to redeem store credit to his wallet (Of course this wouldn't be possible in an actual application)
        def remove_balance():
            amount = simpledialog.askfloat("Input", "Enter amount to withdraw to wallet:")
            if amount is None:
                return
            if  amount <= user_data['balance']: # Checks if the amount the user wants to withdraw is feasible
                user_data['balance'] -= amount
                user_df.loc[user_df['username'] == user_username, 'balance'] = user_data['balance']
                save_data(user_df, None, books_df)
                messagebox.showinfo("Success", f"Withdrew ${amount} to your wallet!")
            else:
                messagebox.showerror("Error", "Insufficient Funds.")
        user_wallet_window=tk.Toplevel()
        user_wallet_window.title("Wallet")

        tk.Button(user_wallet_window, text="Check Balance", command=check_balance).pack(pady=3)
        tk.Button(user_wallet_window, text="Add Balance", command=add_balance).pack(pady=3)
        tk.Button(user_wallet_window, text="Withdraw balance", command=remove_balance).pack(pady=3)
        tk.Button(user_wallet_window,text="Exit",command=user_wallet_window.destroy).pack(pady=3)
    # Allows the user to see all available books
    def view_available_books():
        available_books = books_df[books_df['availability']]
        if not available_books.empty:
            book_list = "\n".join([f"ID: {row['id']}, Title: {row['title']}, Author: {row['author']}, Cost: ${row['cost']}, Shipping: ${row['shipping_cost']}, Bookstore: {row['bookstores']}" for idx, row in available_books.iterrows()])
            messagebox.showinfo("Available Books", book_list)
        else:
            messagebox.showinfo("Available Books", "No books are currently available.")
    # Allows the user to manage their active orders (Should i even put completed orders? Idk)
    def manage_orders():
        def view_orders():
            if user_data['orders']:
                order_details = []
                for order in user_data['orders']:
                    order_id = order['order_id']
                    bookstore_name = order['bookstore']
                    book = books_df[books_df['id'] == order_id].iloc[0]
                    total_cost = book['cost'] + book['shipping_cost']
                    order_details.append(f"ID: {book['id']}, Title: {book['title']}, Bookstore: {bookstore_name}, Total Cost: ${total_cost}")

                order_info = "\n".join(order_details)
                messagebox.showinfo("Active Orders", order_info)
            else:
                messagebox.showinfo("Active Orders", "You have no active orders.")

        # Function to cancel orders
        def cancel_order():
            global books_df, user_df
            user_df, admin_df, books_df = load_data()  # Reload data to ensure the latest updates

            order_ids_input = simpledialog.askstring("Input", "Enter order IDs to cancel (comma-separated):")
            if order_ids_input:
                order_ids = [int(order_id.strip()) for order_id in order_ids_input.split(",") if order_id.strip().isdigit()]
                not_found_orders = []

                for order_id in order_ids:
                    order = next((o for o in user_data['orders'] if o['order_id'] == order_id), None)
                    if order:
                        user_data['orders'].remove(order)
                        bookstore_name = order['bookstore']
                        book = books_df[books_df['id'] == order_id].iloc[0]
                        book_bookstores = book['bookstores']

                        if bookstore_name in book_bookstores:
                            book_bookstores[bookstore_name] += 1  # Add the returned copy
                            total_copies = sum(book_bookstores.values())

                            if book_bookstores[bookstore_name] > 0:
                                books_df.loc[books_df['id'] == order_id, 'availability'] = True

                            books_df.loc[books_df['id'] == order_id, 'bookstores'] = [book_bookstores]
                            books_df.loc[books_df['id'] == order_id, 'copies'] = total_copies

                            user_data['balance'] += book['cost'] + book['shipping_cost']

                            user_df.loc[user_df['username'] == user_username, 'orders'] = str(user_data['orders'])
                            user_df.loc[user_df['username'] == user_username, 'balance'] = user_data['balance']
                            save_data(user_df, None, books_df)
                        else:
                            messagebox.showerror("Error", f"The bookstore '{bookstore_name}' is incorrect or not found in the book's records.")
                            return
                    else:
                        not_found_orders.append(order_id)

                if not_found_orders:
                    messagebox.showerror("Error", f"Order IDs not found: {', '.join(map(str, not_found_orders))}")
                else:
                    messagebox.showinfo("Success", "Cancelled orders successfully!")

        manage_orders_window = tk.Toplevel()
        manage_orders_window.title("Manage Orders")

        tk.Button(manage_orders_window, text="View Orders", command=view_orders).pack(pady=3)
        tk.Button(manage_orders_window, text="Cancel Order", command=cancel_order).pack(pady=3)
        tk.Button(manage_orders_window, text="Exit", command=manage_orders_window.destroy).pack(pady=3)


    def get_book_suggestions():
        global user_df, admin_df, books_df
        user_df, admin_df, books_df = load_data()
        favorite_categories = []

        # Ensure user_data and books_df are not empty
        if not user_data.get('favorites') or books_df.empty:
            messagebox.showinfo("Book Suggestions", "No favorites or books available.")
            return

        # Find book IDs and categories based on the favorite titles
        valid_favorite_books = books_df[books_df['title'].isin(user_data['favorites'])]

        # Extract order IDs from user_data['orders']
        ordered_book_ids = [order['order_id'] for order in user_data['orders']]
        valid_ordered_books = books_df[books_df['id'].isin(ordered_book_ids)]

        if valid_favorite_books.empty and valid_ordered_books.empty:
            messagebox.showinfo("Book Suggestions", "No valid favorite or ordered books found.")
            return

        # Collect categories from favorite books
        for idx, book in valid_favorite_books.iterrows():
            favorite_categories.extend(book['categories'])

        # Collect categories from ordered books
        for idx, book in valid_ordered_books.iterrows():
            favorite_categories.extend(book['categories'])

        # Count occurrences of each category
        category_count = defaultdict(int)
        for category in favorite_categories:
            category_count[category] += 1

        suggested_books = []
        suggested_book_ids = set()  # To keep track of already suggested book IDs

        # Suggest books based on the most frequent categories
        for category, count in sorted(category_count.items(), key=lambda item: item[1], reverse=True):
            category_books = books_df[
                books_df['categories'].apply(lambda x: category in x) & 
                ~books_df['title'].isin(user_data['favorites']) &
                ~books_df['id'].isin(ordered_book_ids)  # Filter out ordered books
            ]
            for book in category_books.to_dict('records'):
                if book['id'] not in suggested_book_ids:
                    suggested_books.append(book)
                    suggested_book_ids.add(book['id'])
                    if len(suggested_books) >= 10:
                        break
            if len(suggested_books) >= 10:
                break

        # Display suggestions or a no suggestions message
        if suggested_books:
            suggestions = "\n".join([f"{book['title']} by {book['author']}" for book in suggested_books])
            messagebox.showinfo("Book Suggestions", suggestions)
        else:
            messagebox.showinfo("Book Suggestions", "No suggestions available.")


    def order_book():
        global books_df  # Ensure books_df is modifiable from the outer scope
        book_titles_input = simpledialog.askstring("Input", "Enter book titles to order (comma-separated):")
        
        if book_titles_input:
            book_titles = [title.strip() for title in book_titles_input.split(",") if title.strip()]  # Split and clean titles
            
            total_cost = 0
            unavailable_books = []
            insufficient_balance = False
            books_to_order = []

            for title in book_titles:
                if title in books_df['title'].values:
                    book = books_df.loc[books_df['title'].str.lower() == title.lower()].iloc[0]
                    
                    if book['availability']:
                        total_cost += book['cost'] + book['shipping_cost']
                        books_to_order.append(book)
                    else:
                        unavailable_books.append(title)
                else:
                    messagebox.showerror("Error", f"Book '{title}' not found.")
                    return

            if total_cost > user_data['balance']:
                insufficient_balance = True

            if unavailable_books:
                messagebox.showerror("Error", f"Books not available: {', '.join(unavailable_books)}")
            elif insufficient_balance:
                messagebox.showerror("Error", "Insufficient balance.")
            else:
                for book in books_to_order:
                    if book['copies'] > 0:
                        user_data['balance'] -= book['cost'] + book['shipping_cost']

                        # Prompt user for the bookstore they are ordering from
                        bookstore_name = simpledialog.askstring("Input", f"Enter the bookstore name for the book '{book['title']}':")
                        if bookstore_name and bookstore_name in book['bookstores']:
                            user_data['orders'].append({'order_id': book['id'], 'bookstore': bookstore_name})
                            book['bookstores'][bookstore_name] -= 1

                            # Update the total copies and availability
                            total_copies = sum(book['bookstores'].values())
                            books_df.loc[books_df['id'] == book['id'], 'copies'] = total_copies
                            books_df.loc[books_df['id'] == book['id'], 'bookstores'] = [book['bookstores']]

                            if total_copies == 0:
                                books_df.loc[books_df['id'] == book['id'], 'availability'] = False
                        else:
                            messagebox.showerror("Error", f"The bookstore '{bookstore_name}' is incorrect or not found in the book's records.")
                            return

                # Save updated dataframes
                user_df.loc[user_df['username'] == user_username, 'orders'] = str(user_data['orders'])
                user_df.loc[user_df['username'] == user_username, 'balance'] = user_data['balance']
                save_data(user_df, None, books_df)
                messagebox.showinfo("Success", "Ordered books successfully!")


    def reviews_panel():
        # Allows the user to write a review
        def write_review(books_df, user_df, user_username):
            # Get user data
            user_data = user_df.loc[user_df['username'] == user_username].iloc[0]

            # Assuming 'orders' is stored as a list of dictionaries directly
            user_orders = user_data['orders']
            
            if isinstance(user_orders, str):
                user_orders = eval(user_orders)

            # Check if user_orders is a list
            if not isinstance(user_orders, list):
                messagebox.showerror("Error", "User orders data is not in the correct format.")
                return

            # Get the book title from user input
            book_title = simpledialog.askstring("Input", "Enter the title of the book you want to review:")
            if book_title is None or not book_title.strip():
                return

            # Check if the book title exists in the DataFrame
            if book_title in books_df['title'].values:
                # Find the book index and its ID
                book_index = books_df.index[books_df['title'] == book_title][0]
                book_id = books_df.loc[book_index, 'id']
                
                # Check if the user has ordered the book
                book_ordered = any(order['order_id'] == book_id for order in user_orders)
                
                if book_ordered:
                    # Check if the user has already written a review for this book
                    existing_reviews = books_df.at[book_index, 'reviews']
                    if existing_reviews is not None:
                        for review in existing_reviews:
                            if review['username'] == user_username:
                                messagebox.showerror("Error", "You have already written a review for this book.")
                                return

                    # Prompt the user for rating (mandatory)
                    rating = simpledialog.askinteger("Input", "Give a rating (1-5) for the book:")
                    if rating is None or rating < 1 or rating > 5:
                        messagebox.showerror("Error", "Invalid rating. Please enter a number between 1 and 5.")
                        return

                    # Prompt the user for review text (optional)
                    review_text = simpledialog.askstring("Input", "Write your review (optional):")

                    # Construct the review object with username and optional review text
                    new_review = {
                        'username': user_username,
                        'review_text': review_text if review_text else ""  # Save review_text as empty string if not provided
                    }

                    # Update the reviews column for the selected book
                    if books_df.at[book_index, 'reviews'] is None:
                        books_df.at[book_index, 'reviews'] = []

                    books_df.at[book_index, 'reviews'].append(new_review)

                    # Update the ratings column with the new rating
                    if books_df.at[book_index, 'ratings'] is None:
                        books_df.at[book_index, 'ratings'] = []

                    books_df.at[book_index, 'ratings'].append(rating)

                    # Save the updated DataFrame to CSV file
                    save_data(user_df, None, books_df)
                    messagebox.showinfo("Success", "Review added successfully!")
                else:
                    messagebox.showerror("Error", f"You have not ordered '{book_title}' by {books_df.at[book_index, 'author']}. Therefore, you cannot write a review.")
            else:
                messagebox.showerror("Error", f"Book with title '{book_title}' not found.")
        def view_reviews(books_df):
            book_title = simpledialog.askstring("Input", "Enter the title of the book you want to view reviews for:")
            
            if book_title is None or not book_title.strip():
                return

            # Check if the book title exists in the DataFrame
            if book_title in books_df['title'].values:
                book_index = books_df.index[books_df['title'] == book_title][0]
                book_reviews = books_df.loc[book_index, 'reviews']
                book_ratings = books_df.loc[book_index, 'ratings']
                
                if book_reviews:
                    reviews_list = "\n\n".join(
                        [f"User: {review['username']}\nReview: {review['review_text']}\nRating: {rating}" for review, rating in zip(book_reviews, book_ratings)]
                    )
                    messagebox.showinfo("Reviews", f"Reviews for Book '{book_title}':\n\n{reviews_list}")
                else:
                    messagebox.showinfo("Reviews", f"No reviews available for Book '{book_title}'.")
            else:
                messagebox.showerror("Error", f"Book with title '{book_title}' not found.")
        def open_write_review():
            write_review(books_df,user_df, user_username)

        def open_view_reviews():
            view_reviews(books_df)
        reviews_panel_window = tk.Toplevel()
        reviews_panel_window.title("Reviews menu")

        tk.Button(reviews_panel_window, text="Leave a Review", command=open_write_review).pack(pady=3)
        tk.Button(reviews_panel_window, text="View Reviews", command=open_view_reviews).pack(pady=3)
        tk.Button(reviews_panel_window, text="Exit", command=reviews_panel_window.destroy).pack(pady=3)

    tk.Button(user_window, text="Modify Personal Information", command=modify_personal_info).pack(pady=3)
    tk.Button(user_window,text="Favorites Actions",command=favorite_actions).pack(pady=3)
    tk.Button(user_window, text="Wallet", command=user_wallet).pack(pady=3)
    tk.Button(user_window, text="View Available Books", command=view_available_books).pack(pady=3)
    tk.Button(user_window, text="Order Book", command=order_book).pack(pady=3)
    tk.Button(user_window, text="Manage Orders", command=manage_orders).pack(pady=3)
    tk.Button(user_window, text="Reviews", command=reviews_panel).pack(pady=3)
    tk.Button(user_window, text="Get Book Suggestions", command=get_book_suggestions).pack(pady=3)
    tk.Button(user_window, text="Logout", command=user_window.destroy).pack(pady=3)