import tkinter as tk
from tkinter import messagebox
import pymongo

client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["crudoperation"]
collection = db["mycollection"]

def create_record():
    name = name_entry.get()
    age = age_entry.get()
    data = {"name": name, "age": age}
    try:
        inserted_record = collection.insert_one(data)
        messagebox.showinfo("Success", f"Record with ID {inserted_record.inserted_id} created successfully.")
        clear_inputs()
    except Exception as e:
        messagebox.showerror("Error", f"Error: {str(e)}")

def read_records():
    try:
        records = collection.find()
        record_text = ""
        for record in records:
            record_text += f"Name: {record['name']}, Age: {record['age']}\n"
        result_text.delete(1.0, tk.END)
        result_text.insert(tk.END, record_text)
    except Exception as e:
        messagebox.showerror("Error", f"Error: {str(e)}")

def update_record(existing_name, new_name, new_age):
    query = {"name": existing_name}
    new_data = {"$set": {"name": new_name, "age": new_age}}
    try:
        updated_record = collection.update_one(query, new_data)
        if updated_record.modified_count > 0:
            messagebox.showinfo("Success", "Record updated successfully.")
            clear_inputs()
        else:
            messagebox.showinfo("Info", "No records matched the query.")
    except Exception as e:
        messagebox.showerror("Error", f"Error: {str(e)}")

def delete_record(name_to_delete):
    query = {"name": name_to_delete}
    try:
        deleted_record = collection.delete_one(query)
        if deleted_record.deleted_count > 0:
            messagebox.showinfo("Success", "Record deleted successfully.")
            clear_inputs()
        else:
            messagebox.showinfo("Info", "No records matched the query.")
    except Exception as e:
        messagebox.showerror("Error", f"Error: {str(e)}")

def clear_inputs():
    name_entry.delete(0, tk.END)
    age_entry.delete(0, tk.END)
    existing_name_entry.delete(0, tk.END)
    new_name_entry.delete(0, tk.END)
    new_age_entry.delete(0, tk.END)
    delete_name_entry.delete(0, tk.END)

root = tk.Tk()
root.title("MongoDB CRUD GUI")

name_label = tk.Label(root, text="Name:")
name_entry = tk.Entry(root)
age_label = tk.Label(root, text="Age:")
age_entry = tk.Entry(root)
create_button = tk.Button(root, text="Create", command=create_record)
read_button = tk.Button(root, text="Read", command=read_records)

existing_name_label = tk.Label(root, text="Existing Name:")
existing_name_entry = tk.Entry(root)
update_label = tk.Label(root, text="Update:")
new_name_label = tk.Label(root, text="New Name:")
new_name_entry = tk.Entry(root)
new_age_label = tk.Label(root, text="New Age:")
new_age_entry = tk.Entry(root)
update_button = tk.Button(root, text="Update", command=lambda: update_record(existing_name_entry.get(), new_name_entry.get(), new_age_entry.get()))

delete_label = tk.Label(root, text="Delete:")
delete_name_label = tk.Label(root, text="Name to Delete:")
delete_name_entry = tk.Entry(root)
delete_button = tk.Button(root, text="Delete", command=lambda: delete_record(delete_name_entry.get()))

clear_button = tk.Button(root, text="Clear", command=clear_inputs)
result_text = tk.Text(root, width=40, height=10)

name_label.grid(row=0, column=0)
name_entry.grid(row=0, column=1)
age_label.grid(row=1, column=0)
age_entry.grid(row=1, column=1)
create_button.grid(row=2, column=0)
read_button.grid(row=2, column=1)

existing_name_label.grid(row=3, column=0)
existing_name_entry.grid(row=3, column=1)
update_label.grid(row=4, column=0)
new_name_label.grid(row=5, column=0)
new_name_entry.grid(row=5, column=1)
new_age_label.grid(row=6, column=0)
new_age_entry.grid(row=6, column=1)
update_button.grid(row=7, column=0)

delete_label.grid(row=8, column=0)
delete_name_label.grid(row=9, column=0)
delete_name_entry.grid(row=9, column=1)
delete_button.grid(row=10, column=0)

clear_button.grid(row=11, column=0)
result_text.grid(row=12, column=0, columnspan=3)

root.mainloop()
