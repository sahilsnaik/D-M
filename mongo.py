import pymongo
import re

client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["crudoperation"]
collection = db["mycollection"]

def create_record(data):
    try:
        inserted_record = collection.insert_one(data)
        return f"Record with ID {inserted_record.inserted_id} created successfully."
    except Exception as e:
        return f"Error: {str(e)}"

def read_records(query={}):
    try:
        records = collection.find(query)
        return list(records)
    except Exception as e:
        return f"Error: {str(e)}"

def update_record(name_to_update, new_data):
    try:
        regex_query = re.compile(fr"^{name_to_update.strip()}", re.IGNORECASE)
        updated_record = collection.update_one({"name": regex_query}, {"$set": new_data})
        if updated_record.modified_count > 0:
            return f"Record updated successfully."
        else:
            return "No records matched the query."
    except Exception as e:
        return f"Error: {str(e)}"

def delete_record(name_to_delete):
    try:
        regex_query = re.compile(fr"^{name_to_delete.strip()}", re.IGNORECASE)
        deleted_record = collection.delete_one({"name": regex_query})
        if deleted_record.deleted_count > 0:
            return f"Record deleted successfully."
        else:
            return "No records matched the query."
    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == "__main__":
    while True:
        print("Select an operation:")
        print("1. Create")
        print("2. Read")
        print("3. Update")
        print("4. Delete")
        print("5. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            name = input("Enter name: ")
            age = int(input("Enter age: "))
            data = {"name": name, "age": age}
            result = create_record(data)
            print(result)

        elif choice == "2":
            query = {}
            records = read_records(query)
            for record in records:
                print(f"Name: {record['name']}, Age: {record['age']}")

        elif choice == "3":
            name_to_update = input("Enter name to update: ")
            new_name = input("Enter new name: ")
            new_age = int(input("Enter new age: "))
            new_data = {"name": new_name, "age": new_age}
            result = update_record(name_to_update, new_data)
            print(result)

        elif choice == "4":
            name_to_delete = input("Enter name to delete: ")
            result = delete_record(name_to_delete)
            print(result)

        elif choice == "5":
            break

        else:
            print("Invalid choice. Please try again.")
