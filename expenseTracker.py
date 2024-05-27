import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
import csv
import os
from tkinter import PhotoImage

# Function to save expense to a CSV file
def save_expense(date, category, description, amount, payment_method):
    file_exists = os.path.isfile('expenses.csv')
    with open('expenses.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(["Date", "Category", "Description", "Amount", "Payment Method"])
        writer.writerow([date, category, description, amount, payment_method])
    messagebox.showinfo("Expense Tracker", "Expense added successfully!")
    display_expenses()  # Update the display after adding an expense


# Function to add expense
def add_expense():
    date = date_entry.get()
    category = category_var.get()  # Retrieve the selected category from the variable
    description = description_entry.get()
    amount = amount_entry.get()
    payment_method = payment_method_var.get()

    if not date or not category or not description or not amount or not payment_method:
        messagebox.showwarning("Input Error", "Please fill all fields.")
        return

    save_expense(date, category, description, amount, payment_method)

    # Clear entry fields
    date_entry.set_date("")
    category_var.set("")  # Reset the category variable
    description_entry.delete(0, tk.END)
    amount_entry.delete(0, tk.END)
    payment_method_var.set("")

# Function to load expenses from the CSV file
def load_expenses():
    if not os.path.isfile('expenses.csv'):
        return []
    with open('expenses.csv', newline='') as file:
        reader = csv.reader(file)
        next(reader, None)  # Skip the header
        return list(reader)

# Function to display expenses with alternating row colors
def display_expenses():
    for row in expense_tree.get_children():
        expense_tree.delete(row)
    expenses = load_expenses()
    for i, expense in enumerate(expenses):
        tag = 'evenrow' if i % 2 == 0 else 'oddrow'
        expense_tree.insert('', 'end', values=expense, tags=(tag,))

# Function to delete selected expense
def delete_expense():
    selected_item = expense_tree.selection()
    if not selected_item:
        messagebox.showwarning("Delete Error", "Please select an expense to delete.")
        return

    item_values = expense_tree.item(selected_item)['values']
    expense_tree.delete(selected_item)
    
    expenses = load_expenses()
    updated_expenses = [expense for expense in expenses if expense != item_values]
    
    with open('expenses.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Date", "Category", "Description", "Amount", "Payment Method"])
        writer.writerows(updated_expenses)
    
    messagebox.showinfo("Expense Tracker", "Expense deleted successfully!")

# Function to clear all expenses
def clear_all_expenses():
    response = messagebox.askyesno("Clear All Expenses", "Are you sure you want to clear all expenses?")
    if response:
        for row in expense_tree.get_children():
            expense_tree.delete(row)
        with open('expenses.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Date", "Category", "Description", "Amount", "Payment Method"])
        messagebox.showinfo("Expense Tracker", "All expenses have been cleared!")

# Create the main window
root = tk.Tk()
root.title("Expense Tracker")
root.configure(background="#f0f0f0")  # Set background color

# Load and resize the icon
calendar_icon = PhotoImage(file="C:/Users/Ayush Shukla/Desktop/MotionCut/week3/calendar_icon.png").subsample(15, 15)

# Create and place labels and entries with icons
tk.Label(root, text="Date:", image=calendar_icon, compound="left", bg="#f0f0f0").grid(row=0, column=0, padx=10, pady=10)

tk.Label(root, text="Category:", bg="#f0f0f0").grid(row=1, column=0, padx=10, pady=10)
tk.Label(root, text="Description:", bg="#f0f0f0").grid(row=2, column=0, padx=10, pady=10)
tk.Label(root, text="Amount:", bg="#f0f0f0").grid(row=3, column=0, padx=10, pady=10)
tk.Label(root, text="Payment Method:", bg="#f0f0f0").grid(row=4, column=0, padx=10, pady=10)

date_entry = DateEntry(root, width=12, background='darkblue', foreground='white', borderwidth=2)
category_var = tk.StringVar(root)
category_dropdown = ttk.Combobox(root, textvariable=category_var, values=["FOOD", "TRAVELING", "RECHARGE", "BILLS", "TO FRIEND", "OTHERS"])
description_entry = tk.Entry(root)
amount_entry = tk.Entry(root)
payment_method_var = tk.StringVar(root)
payment_method_dropdown = ttk.Combobox(root, textvariable=payment_method_var, values=["UPI", "CASH", "CREDIT CARD", "DEBIT CARD"])

date_entry.grid(row=0, column=1, padx=10, pady=10)
category_dropdown.grid(row=1, column=1, padx=10, pady=10)
description_entry.grid(row=2, column=1, padx=10, pady=10)
amount_entry.grid(row=3, column=1, padx=10, pady=10)
payment_method_dropdown.grid(row=4, column=1, padx=10, pady=10)

# Add expense button with custom color
add_button = tk.Button(root, text="Add Expense", command=add_expense, bg="#4CAF50", fg="white")
add_button.grid(row=5, column=0, columnspan=2, pady=20)

# Add a Treeview widget to display expenses
columns = ("Date", "Category", "Description", "Amount", "Payment Method")
expense_tree = ttk.Treeview(root, columns=columns, show='headings')
for col in columns:
    expense_tree.heading(col, text=col)
    expense_tree.column(col, width=100, anchor='center')  # Adjust column width and alignment
expense_tree.grid(row=6, column=0, columnspan=2, padx=10, pady=10)

# Apply colors to rows
expense_tree.tag_configure('evenrow', background='lightgrey')
expense_tree.tag_configure('oddrow', background='white')

# Button to delete selected expense with custom color
delete_button = tk.Button(root, text="Delete Expense", command=delete_expense, bg="#FF5722", fg="white")
delete_button.grid(row=7, column=0, pady=10, sticky='w')

# Button to clear all expenses with custom color
clear_button = tk.Button(root, text="Clear All Expenses", command=clear_all_expenses, bg="#FF5722", fg="white")
clear_button.grid(row=7, column=1, pady=10, sticky='e')

# Initial display of expenses
display_expenses()

# Start the Tkinter event loop
root.mainloop()