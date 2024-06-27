import tkinter as tk
from tkinter import messagebox, simpledialog
from tkinter import ttk
import pymysql

# Соединение с базой данных
connection = pymysql.connect(
    host='localhost',
    user='root',
    password='A02032178a',
    database='test'
)

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Database Application")

        self.tree = ttk.Treeview(root, columns=("id", "fname", "lname", "title", "first", "price", "time"), show="headings")
        self.tree.heading("id", text="ID")
        self.tree.heading("fname", text="First Name")
        self.tree.heading("lname", text="Last Name")
        self.tree.heading("title", text="Title")
        self.tree.heading("first", text="First")
        self.tree.heading("price", text="Price")
        self.tree.heading("time", text="Time")
        self.tree.pack(fill=tk.BOTH, expand=True)

        self.refresh_button = tk.Button(root, text="Refresh", command=self.load_data)
        self.refresh_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.add_button = tk.Button(root, text="Add", command=self.add_record)
        self.add_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.update_button = tk.Button(root, text="Update", command=self.update_record)
        self.update_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.delete_button = tk.Button(root, text="Delete", command=self.delete_record)
        self.delete_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.load_data()

    def load_data(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM user")
            for row in cursor.fetchall():
                self.tree.insert("", tk.END, values=row)

    def add_record(self):
        new_window = tk.Toplevel(self.root)
        new_window.title("Add Record")

        labels = ["First Name", "Last Name", "Title", "First", "Price", "Time"]
        entries = {}

        for i, label in enumerate(labels):
            tk.Label(new_window, text=label).grid(row=i, column=0, padx=10, pady=5)
            entry = tk.Entry(new_window)
            entry.grid(row=i, column=1, padx=10, pady=5)
            entries[label] = entry

        def save():
            fname = entries["First Name"].get()
            lname = entries["Last Name"].get()
            title = entries["Title"].get()
            first = entries["First"].get()
            price = entries["Price"].get()
            time = entries["Time"].get()

            with connection.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO user (fname, lname, title, first, price, time) VALUES (%s, %s, %s, %s, %s, %s)",
                    (fname, lname, title, first, price, time)
                )
            connection.commit()
            self.load_data()
            new_window.destroy()

        tk.Button(new_window, text="Save", command=save).grid(row=len(labels), column=0, columnspan=2, pady=10)

    def update_record(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Select item", "Please select an item to update")
            return

        item = self.tree.item(selected_item)["values"]
        id = item[0]

        new_window = tk.Toplevel(self.root)
        new_window.title("Update Record")

        labels = ["First Name", "Last Name", "Title", "First", "Price", "Time"]
        entries = {}

        for i, (label, value) in enumerate(zip(labels, item[1:])):
            tk.Label(new_window, text=label).grid(row=i, column=0, padx=10, pady=5)
            entry = tk.Entry(new_window)
            entry.grid(row=i, column=1, padx=10, pady=5)
            entry.insert(0, value)
            entries[label] = entry

        def save():
            fname = entries["First Name"].get()
            lname = entries["Last Name"].get()
            title = entries["Title"].get()
            first = entries["First"].get()
            price = entries["Price"].get()
            time = entries["Time"].get()

            with connection.cursor() as cursor:
                cursor.execute(
                    "UPDATE user SET fname=%s, lname=%s, title=%s, first=%s, price=%s, time=%s WHERE id=%s",
                    (fname, lname, title, first, price, time, id)
                )
            connection.commit()
            self.load_data()
            new_window.destroy()

        tk.Button(new_window, text="Save", command=save).grid(row=len(labels), column=0, columnspan=2, pady=10)

    def delete_record(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Select item", "Please select an item to delete")
            return

        item = self.tree.item(selected_item)["values"]
        id = item[0]

        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM user WHERE id=%s", (id,))
        connection.commit()
        self.load_data()

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
