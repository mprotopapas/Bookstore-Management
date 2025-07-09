import tkinter as tk
import os
import matplotlib.pyplot as plt
import pandas as pd
from tkinter import simpledialog, messagebox, filedialog
from data_loader import save_data,load_data



# # Function to refresh dataframes (ASK WHY THIS DOESNT WORK?????!?!)
# def refresh_data():
#     global user_df, admin_df, books_df
#     user_df, admin_df, books_df = load_data()

#Draws the admin menu
def admin_menu(admin_username, books_df, admin_df, user_df):
    admin_data = admin_df[admin_df['username'] == admin_username].iloc[0]
    accessible_bookstores = admin_data['bookstores']

    admin_window = tk.Toplevel()
    admin_window.title("Admin Menu")
    tk.Label(admin_window, text=f"Welcome administrator {admin_data['username']}! ", font='Helvetica 15 underline').pack(pady=10, side='top', anchor="w")
    admin_window.geometry("600x400")

    # Function to create a book

    def add_book():
        def submit_add_book():
            global user_df, admin_df, books_df
            user_df, admin_df, books_df = load_data()

            title = title_entry.get()
            author = author_entry.get()
            publisher = publisher_entry.get()
            categories = categories_entry.get().split(',')
            cost = float(cost_entry.get())
            shipping_cost = float(shipping_cost_entry.get())
            availability = bool(int(availability_entry.get()))
            copies = int(copies_entry.get())

            existing_books = books_df[(books_df['title'] == title) & (books_df['author'] == author) & (books_df['publisher'] == publisher)]

            if not existing_books.empty:
                for idx, book in existing_books.iterrows():
                    book_bookstores = book['bookstores'] if isinstance(book['bookstores'], dict) else {}
                    admin_bookstores = set(accessible_bookstores)

                    if admin_bookstores.intersection(book_bookstores.keys()):
                        for bookstore in admin_bookstores:
                            if bookstore in book_bookstores:
                                book_bookstores[bookstore] += copies
                            else:
                                book_bookstores[bookstore] = copies

                        total_copies = sum(book_bookstores.values())
                        books_df.loc[books_df['id'] == book['id'], 'bookstores'] = [book_bookstores]
                        books_df.loc[books_df['id'] == book['id'], 'copies'] = total_copies

                        save_data(user_df, admin_df, books_df)
                        messagebox.showinfo("Success", "Book already exists. Copies added successfully!")
                        add_book_window.destroy()
                        return
                    else:
                        messagebox.showinfo("Info", f"The book is available in the following bookstores: {', '.join(book['bookstores'].keys())}")
                        return

            new_book_data = {
                'id': books_df['id'].max() + 1,
                'title': title,
                'author': author,
                'publisher': publisher,
                'categories': categories,
                'cost': cost,
                'shipping_cost': shipping_cost,
                'availability': availability,
                'bookstores': {store: copies for store in accessible_bookstores},
                'copies': copies
            }

            new_book_df = pd.DataFrame([new_book_data])
            updated_books_df = pd.concat([books_df, new_book_df], ignore_index=True)
            save_data(user_df, admin_df, updated_books_df)
            messagebox.showinfo("Success", "Book added successfully!")
            add_book_window.destroy()

        add_book_window = tk.Toplevel()
        add_book_window.title("Add Book")

        tk.Label(add_book_window, text="Title").pack()
        title_entry = tk.Entry(add_book_window)
        title_entry.pack()

        tk.Label(add_book_window, text="Author").pack()
        author_entry = tk.Entry(add_book_window)
        author_entry.pack()

        tk.Label(add_book_window, text="Publisher").pack()
        publisher_entry = tk.Entry(add_book_window)
        publisher_entry.pack()

        tk.Label(add_book_window, text="Categories (comma-separated)").pack()
        categories_entry = tk.Entry(add_book_window)
        categories_entry.pack()

        tk.Label(add_book_window, text="Cost").pack()
        cost_entry = tk.Entry(add_book_window)
        cost_entry.pack()

        tk.Label(add_book_window, text="Shipping Cost").pack()
        shipping_cost_entry = tk.Entry(add_book_window)
        shipping_cost_entry.pack()

        tk.Label(add_book_window, text="Availability (1 for True, 0 for False)").pack()
        availability_entry = tk.Entry(add_book_window)
        availability_entry.pack()

        tk.Label(add_book_window, text="Copies").pack()
        copies_entry = tk.Entry(add_book_window)
        copies_entry.pack()

        tk.Button(add_book_window, text="Submit", command=submit_add_book).pack()


    def import_csv():
        def add_books_from_csv():
            global user_df, admin_df, books_df
            user_df, admin_df, books_df = load_data()
            csv_file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])

            if not csv_file_path:
                messagebox.showerror("Error", "No file path provided.")
                return

            if not os.path.exists(csv_file_path):
                messagebox.showerror("Error", "File not found.")
                return

            try:
                csv_df = pd.read_csv(csv_file_path)
                required_columns = ['title', 'author', 'categories', 'cost', 'shipping_cost', 'availability', 'copies']
                for col in required_columns:
                    if col not in csv_df.columns:
                        messagebox.showerror("Error", f"CSV file does not contain a '{col}' column.")
                        return

                admin_data = admin_df[admin_df['username'] == admin_username].iloc[0]
                accessible_bookstores = eval(admin_data['bookstores']) if isinstance(admin_data['bookstores'], str) else admin_data['bookstores']

                added_books = []
                updated_books = []

                new_books = []
                for index, row in csv_df.iterrows():
                    title = row['title'].strip()
                    author = row['author'].strip() if pd.notna(row['author']) else ''
                    categories = row['categories'].strip().split(',') if pd.notna(row['categories']) else []
                    cost = row['cost'] if pd.notna(row['cost']) else 0
                    shipping_cost = row['shipping_cost'] if pd.notna(row['shipping_cost']) else 0
                    availability = row['availability'] if pd.notna(row['availability']) else ''
                    copies = int(row['copies']) if pd.notna(row['copies']) else 0

                    existing_books = books_df[(books_df['title'].str.lower() == title.lower()) &
                                            (books_df['author'].str.lower() == author.lower())]

                    if existing_books.empty:
                        new_book = {
                            'id': books_df['id'].max() + 1 if not books_df.empty else 1,
                            'title': title,
                            'author': author,
                            'publisher': '',
                            'categories': categories,
                            'cost': cost,
                            'shipping_cost': shipping_cost,
                            'availability': availability,
                            'copies': copies,
                            'bookstores': {store: copies for store in accessible_bookstores}  # Use accessible_bookstores directly
                        }
                        new_books.append(new_book)
                        added_books.append(title)
                    else:
                        book_updated = False
                        for idx, book in existing_books.iterrows():
                            book_bookstores = eval(book['bookstores']) if isinstance(book['bookstores'], str) else book['bookstores']
                            for store in accessible_bookstores:
                                if store in book_bookstores:
                                    book_bookstores[store] += copies
                                else:
                                    book_bookstores[store] = copies

                            total_copies = sum(book_bookstores.values())
                            books_df.at[idx, 'bookstores'] = book_bookstores
                            books_df.at[idx, 'copies'] = total_copies

                            updated_books.append(title)
                            book_updated = True
                            break

                        if not book_updated:
                            messagebox.showinfo("Info", f"Duplicate book found: {title}. Skipping update.")

                if new_books:
                    new_books_df = pd.DataFrame(new_books)
                    books_df = pd.concat([books_df, new_books_df], ignore_index=True)

                save_data(user_df, admin_df, books_df)

                if added_books:
                    messagebox.showinfo("Success", f"Books added: {', '.join(added_books)}")
                if updated_books:
                    messagebox.showinfo("Success", f"Books updated with additional copies: {', '.join(updated_books)}")

            except Exception as e:
                messagebox.showerror("Error", f"An error occurred while processing the file: {e}")

        def open_add_books_from_csv():
            add_books_from_csv()

        csv_management_window = tk.Toplevel()
        csv_management_window.title("Import Books")
        tk.Button(csv_management_window, text="Import from CSV", command=open_add_books_from_csv).pack(pady=3)
        tk.Button(csv_management_window, text="Exit", command=csv_management_window.destroy).pack(pady=3)
        
        # Function to remove a book from their bookstore only
    def remove_book():
        global user_df, admin_df, books_df
        user_df, admin_df, books_df = load_data()
        book_id = simpledialog.askinteger("Input", "Enter book ID to remove:")
        if book_id is None:
            return

        if book_id in books_df['id'].values:
            book = books_df.loc[books_df['id'] == book_id].iloc[0]
            admin_bookstores = set(accessible_bookstores)
            book_bookstores = book['bookstores'] if isinstance(book['bookstores'], dict) else {}

            if admin_bookstores.intersection(book_bookstores.keys()):
                for store in admin_bookstores:
                    if store in book_bookstores:
                        del book_bookstores[store]

                if not book_bookstores:
                    books_df.drop(books_df[books_df['id'] == book_id].index, inplace=True)
                else:
                    total_copies = sum(book_bookstores.values())
                    books_df.loc[books_df['id'] == book_id, 'bookstores'] = [book_bookstores]
                    books_df.loc[books_df['id'] == book_id, 'copies'] = total_copies

                save_data(user_df, admin_df, books_df)
                messagebox.showinfo("Success", "Book removed successfully!")
            else:
                messagebox.showerror("Error", "You do not have access to remove this book.")
        else:
            messagebox.showerror("Error", "Book ID not found.")

    # Function for the administrator to update the books from THEIR bookstores ONLY
    def update_book():
        global user_df, admin_df, books_df
        user_df, admin_df, books_df = load_data()

        def submit_update_book(book_id):
            global user_df, admin_df, books_df
            user_df, admin_df, books_df = load_data()

            title = title_entry.get()
            author = author_entry.get()
            publisher = publisher_entry.get()
            categories = categories_entry.get().split(',')
            cost = float(cost_entry.get())
            shipping_cost = float(shipping_cost_entry.get())
            availability = bool(int(availability_entry.get()))
            new_copies = int(copies_entry.get())

            # Ensure the list of accessible bookstores is used
            admin_bookstores = accessible_bookstores

            # Find the index of the book_id
            book_index = books_df.index[books_df['id'] == book_id].tolist()[0]

            # Get the bookstores and copies for this book
            book_bookstores = books_df.at[book_index, 'bookstores']
            if isinstance(book_bookstores, str):
                book_bookstores = eval(book_bookstores)
            if not isinstance(book_bookstores, dict):
                book_bookstores = {}

            # Update details for each bookstore the admin has access to
            for store in admin_bookstores:
                if store in book_bookstores:
                    # Update copies for the admin's store
                    book_bookstores[store] = new_copies

            # Update the total copies
            total_copies = sum(book_bookstores.values())

            # Update each column individually, only for accessible bookstores
            books_df.at[book_index, 'title'] = title
            books_df.at[book_index, 'author'] = author
            books_df.at[book_index, 'publisher'] = publisher
            books_df.at[book_index, 'categories'] = categories  # Assign list directly
            books_df.at[book_index, 'cost'] = cost
            books_df.at[book_index, 'shipping_cost'] = shipping_cost
            books_df.at[book_index, 'availability'] = availability
            books_df.at[book_index, 'bookstores'] = book_bookstores  # Update only the relevant bookstores
            books_df.at[book_index, 'copies'] = total_copies

            save_data(user_df, admin_df, books_df)
            messagebox.showinfo("Success", "Book updated successfully!")
            update_book_window.destroy()

        book_id = simpledialog.askinteger("Input", "Enter book ID to update:")
        if book_id is None:
            return

        if book_id in books_df['id'].values:
            book = books_df.loc[books_df['id'] == book_id].iloc[0]

            # Check if admin has access to any of the bookstores associated with the book
            admin_bookstores = set(accessible_bookstores)
            book_bookstores = book['bookstores']
            if isinstance(book_bookstores, str):
                book_bookstores = eval(book_bookstores)
            if not isinstance(book_bookstores, dict):
                book_bookstores = {}

            if admin_bookstores.intersection(book_bookstores.keys()):
                update_book_window = tk.Toplevel()
                update_book_window.title("Update Book")

                tk.Label(update_book_window, text="Title").pack()
                title_entry = tk.Entry(update_book_window)
                title_entry.insert(0, book['title'])
                title_entry.pack()

                tk.Label(update_book_window, text="Author").pack()
                author_entry = tk.Entry(update_book_window)
                author_entry.insert(0, book['author'])
                author_entry.pack()

                tk.Label(update_book_window, text="Publisher").pack()
                publisher_entry = tk.Entry(update_book_window)
                publisher_entry.insert(0, book['publisher'])
                publisher_entry.pack()

                tk.Label(update_book_window, text="Categories (comma-separated)").pack()
                categories_entry = tk.Entry(update_book_window)
                categories_entry.insert(0, ','.join(book['categories']))
                categories_entry.pack()

                tk.Label(update_book_window, text="Cost").pack()
                cost_entry = tk.Entry(update_book_window)
                cost_entry.insert(0, book['cost'])
                cost_entry.pack()

                tk.Label(update_book_window, text="Shipping Cost").pack()
                shipping_cost_entry = tk.Entry(update_book_window)
                shipping_cost_entry.insert(0, book['shipping_cost'])
                shipping_cost_entry.pack()

                tk.Label(update_book_window, text="Availability (1 for True, 0 for False)").pack()
                availability_entry = tk.Entry(update_book_window)
                availability_entry.insert(0, int(book['availability']))
                availability_entry.pack()

                tk.Label(update_book_window, text="Copies for your store").pack()
                copies_entry = tk.Entry(update_book_window)
                store_name = list(admin_bookstores)[0]  # adds the storename
                copies_entry.insert(0, book_bookstores.get(store_name, 0))
                copies_entry.pack()

                tk.Button(update_book_window, text="Submit", command=lambda: submit_update_book(book_id)).pack()
            else:
                messagebox.showerror("Error", "You do not have access to update this book.")
        else:
            messagebox.showerror("Error", "Book ID not found.")


    # Menu for book availability
    def book_availability():
        # checks for book availability
        def check_book_availability():
            book_title = simpledialog.askstring("Input", "Enter book title to check availability:")
            # Set it to none for the cancel button
            if book_title is None:
                return
            
            # Make the title comparison case-insensitive
            matching_books = books_df[books_df['title'].str.lower() == book_title.lower()]
            
            if not matching_books.empty:
                book = matching_books.iloc[0]
                admin_bookstores = set(accessible_bookstores)
                book_bookstores = set(book['bookstores'].keys()) if isinstance(book['bookstores'], dict) else set() #If dictionary, extract the keys and convert them to a set else initiallize empty
                
                if admin_bookstores.intersection(book_bookstores):
                    if book['availability']:
                        messagebox.showinfo("Info", f"{book['title']} with id {book['id']} is available.")
                    else:
                        messagebox.showinfo("Info", f"{book['title']} with id {book['id']} is not available.")
                else:
                    accessible_stores = ", ".join(book['bookstores'].keys())
                    messagebox.showinfo("Info", f"'{book['title']}' is not available in your store. However, it is available at: {accessible_stores}")
            else:
                messagebox.showerror("Error", "Book title not found.")
            # Check if the book exists in a certain store
        def check_book_availability_at_store():
            book_title = simpledialog.askstring("Input", "Enter book title to check availability:")
            if book_title is None:
                return
            bookstore_name = simpledialog.askstring("Input", "Enter bookstore name to check availability:")
            if bookstore_name is None:
                return
            
            # Make the title comparison case-insensitive
            matching_books = books_df[books_df['title'].str.lower() == book_title.lower()] # I could've used this for a lot more things just got bored. Makes both the title and the input lower case to avoid case sensitivity.
            
            if not matching_books.empty:
                book = matching_books.iloc[0]
                book_bookstores = eval(book['bookstores']) if isinstance(book['bookstores'], str) else book['bookstores']
                if not isinstance(book_bookstores, dict):
                    book_bookstores = {}

                if bookstore_name in book_bookstores:
                    if book['availability']:
                        messagebox.showinfo("Info", f"'{book['title']}' with id {book['id']} is available at {bookstore_name}.")
                    else:
                        messagebox.showinfo("Info", f"'{book['title']}' with id {book['id']} is not available at {bookstore_name}.")
                else:
                    messagebox.showinfo("Info", f"'{book['title']}' is not available at {bookstore_name}.")
            else:
                messagebox.showerror("Error", "Book title not found.")
        book_availability_window= tk.Toplevel()
        book_availability_window.title("Book Availability Menu")


        tk.Button(book_availability_window, text="Check Book Availability", command=check_book_availability).pack(pady=3)
        tk.Button(book_availability_window, text="Check Book Availability at certain stores", command=check_book_availability_at_store).pack(pady=3)
        tk.Button(book_availability_window, text="Exit", command=book_availability_window.destroy).pack(pady=3)

    # Calculates the book cost by taking either the id or the total cost if the admin has access to the bookstore
    def calculate_book_costs():
        def calculate_individual_book_cost():
            book_id = simpledialog.askinteger("Input", "Enter book ID to calculate cost:")
            if book_id is None:
                return

            if book_id in books_df['id'].values:
                book = books_df[books_df['id'] == book_id].iloc[0]
                admin_bookstores = set(accessible_bookstores)
                book_bookstores = set(book['bookstores'].keys()) if isinstance(book['bookstores'], dict) else set()
                
                if admin_bookstores.intersection(book_bookstores):
                    total_cost = book['cost'] + book['shipping_cost']
                    messagebox.showinfo("Book Cost", f"Total cost for '{book['title']}': {total_cost}")
                else:
                    messagebox.showerror("Error", "You do not have access to calculate cost for this book.")
            else:
                messagebox.showerror("Error", "Book ID not found.")

        def calculate_total_costs():
            admin_bookstores = set(accessible_bookstores)
            
            # Filter books_df to only include books from accessible bookstores
            def is_accessible(bookstores):
                if isinstance(bookstores, dict):
                    return bool(set(bookstores.keys()).intersection(admin_bookstores))
                return False
            
            accessible_books_df = books_df[books_df['bookstores'].apply(is_accessible)]
            
            total_by_author = accessible_books_df.groupby('author').apply(lambda x: (x['cost'] + x['shipping_cost']).sum()).to_dict()
            total_by_publisher = accessible_books_df.groupby('publisher').apply(lambda x: (x['cost'] + x['shipping_cost']).sum()).to_dict()
            total_cost = (accessible_books_df['cost'] + accessible_books_df['shipping_cost']).sum()

            result = "Total costs by author:\n" + "\n".join([f"{author}: {total}" for author, total in total_by_author.items()])
            result += "\n\nTotal costs by publisher:\n" + "\n".join([f"{publisher}: {total}" for publisher, total in total_by_publisher.items()])
            result += f"\n\nOverall total cost of all accessible books: {total_cost}"

            messagebox.showinfo("Total Costs", result)

        costs_window = tk.Toplevel()
        costs_window.title("Calculate Book Costs")

        tk.Button(costs_window, text="Calculate Individual Book Cost", command=calculate_individual_book_cost).pack(pady=3)
        tk.Button(costs_window, text="Calculate Total Costs", command=calculate_total_costs).pack(pady=3)
        tk.Button(costs_window, text="Exit", command=costs_window.destroy).pack(pady=3)


    # Deletes the user, no matter where, idk if we needed a limit
    def delete_user():
        username = simpledialog.askstring("Input", "Enter username to delete:")
        if username is None:
            return
        if username in user_df['username'].values:
            user_df.drop(user_df[user_df['username'] == username].index, inplace=True)
            save_data(user_df, admin_df, books_df)
            messagebox.showinfo("Success", f"User '{username}' deleted successfully.")
        else:
            messagebox.showerror("Error", f"User '{username}' not found.")
    # Manage reviews menu
    def manage_reviews():
        # Allows admin to remove reviews
        def remove_reviews(books_df, accessible_bookstores):
            global user_df, admin_df
            user_df, admin_df, books_df = load_data()
            
            book_id = simpledialog.askinteger("Input", "Enter the ID of the book you want to manage reviews for:")
            if book_id is None:
                return

            if book_id in books_df['id'].values:
                book = books_df.loc[books_df['id'] == book_id].iloc[0]

                # Parse the bookstores information from the string representation
                book_bookstores = eval(book['bookstores']) if isinstance(book['bookstores'], str) else book['bookstores']
                if not isinstance(book_bookstores, dict):
                    messagebox.showerror("Error", "Bookstore data is not in the correct format.")
                    return
                
                admin_bookstores = set(accessible_bookstores) # make it a set

                if admin_bookstores.intersection(book_bookstores.keys()):
                    book_index = books_df.index[books_df['id'] == book_id].tolist()[0]
                    book_reviews = books_df.at[book_index, 'reviews']
                    book_ratings = books_df.at[book_index, 'ratings']

                    if book_reviews:
                        reviews_list = "\n\n".join([f"User: {review['username']}\nReview: {review['review_text']}" for review in book_reviews])
                        selected_review = simpledialog.askinteger("Input", f"Select review number to delete (1-{len(book_reviews)}):\n\n{reviews_list}")

                        if selected_review is not None and 1 <= selected_review <= len(book_reviews):
                            # Delete the selected review
                            del book_reviews[selected_review - 1]
                            del book_ratings[selected_review - 1]
                            books_df.at[book_index, 'reviews'] = book_reviews
                            books_df.at[book_index, 'ratings'] = book_ratings
                            save_data(user_df, admin_df, books_df)  # Save books_df after deleting review
                            messagebox.showinfo("Success", "Review deleted successfully!")
                        else:
                            messagebox.showerror("Error", "Invalid input.")
                    else:
                        messagebox.showinfo("Reviews", f"No reviews available for Book ID {book_id}.")
                else:
                    messagebox.showerror("Error", "You do not have access to manage reviews for this book.")
            else:
                messagebox.showerror("Error", f"Book with ID {book_id} not found.")

        # allows the administrator to edit reviews, takes in books_df and accessible stores
        def edit_reviews(books_df, accessible_bookstores):
            book_id = simpledialog.askinteger("Input", "Enter the ID of the book to manage reviews for:")
            if book_id is None:
                return

            if book_id in books_df['id'].values:
                book_index = books_df.index[books_df['id'] == book_id].tolist()[0] # Converts the indices of these rows into a list.
                book = books_df.loc[book_index]

                # Parse the bookstores information from the string representation
                book_bookstores = eval(book['bookstores']) if isinstance(book['bookstores'], str) else book['bookstores'] # If string, eval() as an expression to convert to dict, else directly assign the value
                if not isinstance(book_bookstores, dict):
                    messagebox.showerror("Error", "Bookstore data is not in the correct format.")
                    return
                
                admin_bookstores = set(accessible_bookstores)

                if admin_bookstores.intersection(book_bookstores.keys()):
                    edit_review_window = tk.Toplevel()
                    edit_review_window.title("Edit Reviews")

                    tk.Label(edit_review_window, text=f"Reviews for Book ID: {book_id}").pack()

                    if 'reviews' not in book or not book['reviews']:
                        tk.Label(edit_review_window, text="No reviews available for this book.").pack()
                    else:
                        reviews_frame = tk.Frame(edit_review_window)
                        reviews_frame.pack(padx=10, pady=10)

                        review_entries = []

                        for review_index, review in enumerate(book['reviews']): # Returns an iterator to allow traversal through all of the elements in reviews
                            review_label = tk.Label(reviews_frame, text=f"Review {review_index + 1}:")
                            review_label.pack(anchor='w')

                            review_text = tk.Text(reviews_frame, height=4, width=50)
                            review_text.insert(tk.END, review['review_text'])
                            review_text.pack()

                            review_entries.append(review_text)

                        def save_all_changes():
                            for review_index, review_text in enumerate(review_entries):
                                updated_review = {
                                    'username': book['reviews'][review_index]['username'],
                                    'review_text': review_text.get("1.0", tk.END).strip()
                                }
                                books_df.at[book_index, 'reviews'][review_index] = updated_review

                            save_data(user_df, admin_df, books_df)
                            messagebox.showinfo("Success", "Reviews updated successfully!")
                            edit_review_window.destroy()

                        save_button = tk.Button(reviews_frame, text="Save All Changes", command=save_all_changes)
                        save_button.pack(pady=10)

                else:
                    messagebox.showerror("Error", "You do not have access to manage reviews for this book.")
            else:
                messagebox.showerror("Error", f"Book with ID {book_id} not found.")

        # Views the reports (Stolen code from user, modified)
        def view_reviews(books_df):
            book_id = simpledialog.askinteger("Input", "Enter the ID of the book you want to view reviews for:")
            
            if book_id is None:
                return

            # Check if the book ID exists in the DataFrame
            if book_id in books_df['id'].values:
                book_index = books_df.index[books_df['id'] == book_id].tolist()[0]
                book_reviews = books_df.loc[book_index, 'reviews']
                book_ratings = books_df.loc[book_index, 'ratings']
                
                if book_reviews:
                    reviews_list = "\n\n".join(
                        [f"User: {review['username']}\nReview: {review['review_text']}\nRating: {rating}" for review, rating in zip(book_reviews, book_ratings)]
                    )
                    messagebox.showinfo("Reviews", f"Reviews for Book ID '{book_id}':\n\n{reviews_list}")
                else:
                    messagebox.showinfo("Reviews", f"No reviews available for Book ID '{book_id}'.")
            else:
                messagebox.showerror("Error", f"Book with ID '{book_id}' not found.")


        # Function to draw the remove menu
        def open_remove_reviews():
            remove_reviews(books_df, accessible_bookstores)

        # Function to draw the edit menu
        def open_edit_reviews():
            edit_reviews(books_df,accessible_bookstores)

        def open_view_reviews():
            view_reviews(books_df)
        # Initiate TK window
        manage_reviews_window = tk.Toplevel()
        manage_reviews_window.title("Manage Reviews")

        tk.Button(manage_reviews_window, text="Remove Review", command=open_remove_reviews).pack(pady=3)
        tk.Button(manage_reviews_window, text="View Reviews",command=open_view_reviews).pack(pady=3)
        tk.Button(manage_reviews_window, text="Edit Review", command=open_edit_reviews).pack(pady=3)
        tk.Button(manage_reviews_window, text="Exit", command=manage_reviews_window.destroy).pack(pady=3)

    # Generate graphs with matplotlib
    def generate_graphs():
        def plot_graph(title, x_data, y_data, x_label, y_label):
            plt.figure(figsize=(10, 6))
            plt.bar(x_data, y_data)
            plt.title(title)
            plt.xlabel(x_label)
            plt.ylabel(y_label)
            plt.xticks(rotation=45, ha='right')
            plt.tight_layout()
            plt.show()

        def books_per_publisher(include_copies):
            if include_copies:
                data = books_df.groupby('publisher')['copies'].sum()
                title = 'Number of Books per Publisher (Including Copies)'
            else:
                data = books_df['publisher'].value_counts()
                title = 'Number of Books per Publisher (Excluding Copies)'
            plot_graph(title, data.index, data.values, 'Publisher', 'Number of Books')

        def books_per_author(include_copies):
            if include_copies:
                data = books_df.groupby('author')['copies'].sum()
                title = 'Number of Books per Author (Including Copies)'
            else:
                data = books_df['author'].value_counts()
                title = 'Number of Books per Author (Excluding Copies)'
            plot_graph(title, data.index, data.values, 'Author', 'Number of Books')

        def books_per_category():
            categories = books_df['categories'].explode().value_counts()
            plot_graph('Number of Books per Category (Excluding Copies)', categories.index, categories.values, 'Category', 'Number of Books')

        def books_per_store():
            store_counts = {}
            for bookstores in books_df['bookstores']:
                for store in bookstores:
                    if store in store_counts:
                        store_counts[store] += 1
                    else:
                        store_counts[store] = 1
            data = pd.Series(store_counts)
            plot_graph('Number of Books per Store (Including Copies)', data.index, data.values, 'Store', 'Number of Books')

        def distribution_costs():
            costs = books_df['cost'] + books_df['shipping_cost']
            plt.figure(figsize=(10, 6))
            plt.hist(costs, bins=20)
            plt.title('Distribution of Book Costs')
            plt.xlabel('Cost')
            plt.ylabel('Number of Books')
            plt.tight_layout()
            plt.show()

        def users_per_city():
            data = user_df['city'].value_counts()
            plot_graph('Number of Users per City', data.index, data.values, 'City', 'Number of Users')

        graphs_window = tk.Toplevel()
        graphs_window.geometry("400x600")
        graphs_window.title("Generate Graphs")

        tk.Button(graphs_window, text="Books per Publisher (Including Copies)", command=lambda: books_per_publisher(True)).pack(pady=3)
        tk.Button(graphs_window, text="Books per Publisher (Excluding Copies)", command=lambda: books_per_publisher(False)).pack(pady=3)
        tk.Button(graphs_window, text="Books per Author (Including Copies)", command=lambda: books_per_author(True)).pack(pady=3)
        tk.Button(graphs_window, text="Books per Author (Excluding Copies)", command=lambda: books_per_author(False)).pack(pady=3)
        tk.Button(graphs_window, text="Books per Category", command=books_per_category).pack(pady=3)
        tk.Button(graphs_window, text="Books per Store", command=books_per_store).pack(pady=3)
        tk.Button(graphs_window, text="Distribution of Book Costs", command=distribution_costs).pack(pady=3)
        tk.Button(graphs_window, text="Users per City", command=users_per_city).pack(pady=3)
        tk.Button(graphs_window, text="Close Window", command=graphs_window.destroy).pack(pady=3)

    tk.Button(admin_window, text="Add Book", command=add_book).pack(pady=3)
    tk.Button(admin_window, text="Add Books from csv", command=import_csv).pack(pady=3)
    tk.Button(admin_window, text="Remove Book", command=remove_book).pack(pady=3)
    tk.Button(admin_window, text="Update Book", command=update_book).pack(pady=3)
    tk.Button(admin_window, text="Check Book Availability", command=book_availability).pack(pady=3)
    tk.Button(admin_window, text="Calculate Book Costs", command=calculate_book_costs).pack(pady=3)
    tk.Button(admin_window, text="Delete User", command=delete_user).pack(pady=3)
    tk.Button(admin_window, text="Manage Reviews", command=manage_reviews).pack(pady=3)
    tk.Button(admin_window, text="Generate Graphs", command=generate_graphs).pack(pady=3)
    tk.Button(admin_window, text="Logout", command=admin_window.destroy).pack(pady=3)
