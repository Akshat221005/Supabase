from supabase import create_client
from dotenv import load_dotenv
import os

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = ""

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
# -------------------------
# LOGIN
# -------------------------
email = input("Enter email: ")
password = input("Enter password: ")

auth = supabase.auth.sign_in_with_password({
    "email": email,
    "password": password
})

user = auth.user
user_id = user.id

print("Login successful")
print("User ID:", user_id)

bucket_name = "user_files"

# -------------------------
# CHECK IF USER FOLDER EXISTS
# -------------------------
files = supabase.storage.from_(bucket_name).list(path=user_id)

if len(files) == 0:
    print("User folder does not exist. It will be created on first upload.")
else:
    print("User folder already exists")
# -------------------------
# FETCH USER RECORDS
# -------------------------
response = supabase.table("users_data") \
    .select("id,name,city") \
    .eq("user_id", user_id) \
    .execute()

rows = response.data

if not rows:
    print("No records found for this user")
    exit()

print("\nYour records:")
for r in rows:
    print(f"ID: {r['id']} | Name: {r['name']} | City: {r['city']}")

# -------------------------
# SELECT RECORD
# -------------------------
record_id = int(input("\nEnter the ID where you want to attach the file: "))

# -------------------------
# FILE UPLOAD
# -------------------------
file_path = input("Enter file path to upload: ")
file_name = os.path.basename(file_path)

storage_path = f"{user_id}/{record_id}/{file_name}"

with open(file_path, "rb") as f:
    supabase.storage.from_(bucket_name).upload(
        storage_path,
        f
    )

print("File uploaded successfully")

# -------------------------
# GET FILE URL
# -------------------------
file_url = supabase.storage.from_(bucket_name).get_public_url(storage_path)

print("File URL:", file_url)

# -------------------------
# UPDATE DATABASE
# -------------------------
supabase.table("users_data") \
    .update({"file_url": file_url}) \
    .eq("id", record_id) \
    .execute()

print("Database updated successfully")
