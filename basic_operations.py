from supabase import create_client
from dotenv import load_dotenv
import os

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

current_user_id = None


# ---------------- LOGIN ---------------- #

def login():
    global current_user_id

    email = input("Enter email: ")
    password = input("Enter password: ")

    try:
        response = supabase.auth.sign_in_with_password({
            "email": email,
            "password": password
        })

        if response.user:
            current_user_id = response.user.id
            print(f"\nLogin successful! Welcome {email}\n")
            return True

    except Exception as e:
        print("Authentication failed:", e)

    return False


# ---------------- INSERT ---------------- #

def insert_data():
    name = input("Enter name: ")
    age = int(input("Enter age: "))
    city = input("Enter city: ")

    response = supabase.table("users_data").insert({
        "user_id": current_user_id,
        "name": name,
        "age": age,
        "city": city
    }).execute()

    print("Inserted:", response.data)


# ---------------- READ ---------------- #

def read_data():

    response = supabase.table("users_data") \
        .select("*") \
        .eq("user_id", current_user_id) \
        .execute()

    print("\nYour Data\n")

    for row in response.data:
        print(row)


# ---------------- UPDATE ---------------- #

def update_data():

    record_id = int(input("Enter record id to update: "))

    print("\nWhat do you want to update?")
    column = input("Enter column name (name / age / city): ")

    new_value = input(f"Enter new value for {column}: ")

    # convert age to integer if needed
    if column == "age":
        new_value = int(new_value)

    response = supabase.table("users_data") \
        .update({column: new_value}) \
        .eq("id", record_id) \
        .eq("user_id", current_user_id) \
        .execute()

    print("Updated:", response.data)


# ---------------- DELETE ---------------- #

def delete_data():

    record_id = int(input("Enter record id to delete: "))

    response = supabase.table("users_data") \
        .delete() \
        .eq("id", record_id) \
        .eq("user_id", current_user_id) \
        .execute()

    print("Deleted:", response.data)


# ---------------- MAIN MENU ---------------- #

def menu():

    while True:

        print("\nChoose Operation")
        print("1 Insert")
        print("2 Read")
        print("3 Update")
        print("4 Delete")
        print("5 Exit")

        choice = input("Enter choice: ")

        if choice == "1":
            insert_data()

        elif choice == "2":
            read_data()

        elif choice == "3":
            update_data()

        elif choice == "4":
            delete_data()

        elif choice == "5":
            print("Exiting...")
            break

        else:
            print("Invalid option")


# ---------------- RUN PROGRAM ---------------- #

if login():
    menu()
else:
    print("Access denied")