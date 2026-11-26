# Mode,Naam,Kaam kya karta hai?,Agar file pehle se na ho?
# 'r',Read,Sirf parhne ke liye (Default mode).,FileNotFoundError deta hai.
# 'w',Write,Naya likhne ke liye (purana sab delete kar deta hai).,Nayi file bana deta hai.
# 'a',Append,Purane data ke aakhir mein naya data jorne ke liye.,Nayi file bana deta hai.
# 'x',Exclusive,Sirf tab nayi file banata hai jab wo pehle se maujood na ho.,Nayi file bana deta hai (maujood ho to Error).
# 'r+',Read + Write,Parhne aur likhne dono ke liye (cursor shuru mein hota hai).,FileNotFoundError deta hai.
# 'rb' / 'wb',Binary,"Text ke ilawa Images, PDFs, Videos, ya Pickle objects ke liye.","'rb' error deta hai, 'wb' nayi banata hai."


"""
================================================================================
THE ULTIMATE PYTHON FILE HANDLING MASTERCLASS (Beginner to Advanced / PhD Level)
================================================================================
Is aik file mein Python File Handling ke tamam concepts cover kiye gaye hain:
1. File Modes (r, w, a, x, r+, b)
2. Writing & Appending Data
3. Reading Data (read, readline, readlines, loops)
4. File Pointer Control (seek & tell)
5. Context Managers ('with' statement - Best Practice)
6. Exception Handling (Errors se bachna)
7. Working with Structured Data (CSV & JSON)
8. Binary Files (Images/Raw Bytes & Pickle)
9. OS & Pathlib Module (Folders, Rename, Delete, File Info)
================================================================================
"""

import os
import csv
import json
import pickle
from pathlib import Path

print("🚀 PYTHON FILE HANDLING MASTERCLASS SHURU HO RAHI HAI...\n")

# ==============================================================================
# LEVEL 1: BASIC FILE WRITING (Purana Method vs Modern 'with' Method)
# ==============================================================================
print("--- LEVEL 1: Writing Files ---")

# Method A: Traditional way (Ismein file.close() karna zaroori hota hai)
file = open("basic_notes.txt", "w", encoding="utf-8")  # 'w' purana data mita kar naya likhta hai
file.write("Line 1: Assalam-o-Alaikum! Ye Python File Handling ki pehli file hai.\n")
file.write("Line 2: 'w' mode hamesha nayi file banata hai ya purani ko overwrite karta hai.\n")
file.close()  # Agar close na karein to memory leak ya data loss ho sakta hai

# Method B: Modern & Best Practice ('with' statement / Context Manager)
# Ismein file khud-ba-khud close ho jati hai, chahe error hi kyun na aa jaye.
with open("notes.txt", "w", encoding="utf-8") as f:
    f.write("1. Python seekhna bohat aasan hai.\n")
    f.write("2. File handling se hum data permanent save kar sakte hain.\n")
    
    # writelines() aik list ke tamam items ko file mein likhta hai
    extra_lines = [
        "3. Yeh teesri line hai.\n",
        "4. Yeh chauthi line hai.\n"
    ]
    f.writelines(extra_lines)

print("✅ 'notes.txt' aur 'basic_notes.txt' successfully create ho gayin.\n")


# ==============================================================================
# LEVEL 2: APPENDING DATA (Purana data bachate hue naya data add karna)
# ==============================================================================
print("--- LEVEL 2: Appending Data ('a' mode) ---")

with open("notes.txt", "a", encoding="utf-8") as f:
    f.write("5. Yeh line 'a' (append) mode se end mein add ki gayi hai.\n")

print("✅ 'notes.txt' mein naya data append ho gaya.\n")


# ==============================================================================
# LEVEL 3: READING DATA (Mukhtalif tareeqon se file parhna)
# ==============================================================================
print("--- LEVEL 3: Reading Files ('r' mode) ---")

with open("notes.txt", "r", encoding="utf-8") as f:
    # 1. Poori file aik sath parhna (Choti files ke liye best)
    poora_content = f.read()
    print("[Poori File Ka Content]:\n" + poora_content)

with open("notes.txt", "r", encoding="utf-8") as f:
    # 2. Line by Line parhna (Bari files ke liye memory-efficient tareeqa)
    print("[Line-by-Line Reading]:")
    for line_number, line in enumerate(f, start=1):
        print(f"  Line {line_number} -> {line.strip()}")  # .strip() extra \n hatata hai

with open("notes.txt", "r", encoding="utf-8") as f:
    # 3. Tamam lines ko Python List mein convert karna
    lines_list = f.readlines()
    print(f"\n[List Format]: Total {len(lines_list)} lines hain. Pehli line: {lines_list[0].strip()}\n")


# ==============================================================================
# LEVEL 4: FILE POINTER CONTROL (tell() aur seek()) - Intermediate/Advanced
# ==============================================================================
print("--- LEVEL 4: Cursor Control (seek & tell) ---")

with open("notes.txt", "r", encoding="utf-8") as f:
    print("Shuru mein cursor position:", f.tell())  # 0
    
    pehle_10_chars = f.read(10)  # Sirf 10 characters parhega
    print("Pehle 10 characters:", pehle_10_chars)
    print("Ab cursor position:", f.tell())  # 10
    
    f.seek(0)  # Cursor ko wapas 0 (shuru) par le jana
    print("seek(0) ke baad cursor position:", f.tell())
    print("Dobara pehli line:", f.readline().strip(), "\n")


# ==============================================================================
# LEVEL 5: EXCLUSIVE CREATION ('x') & EXCEPTION HANDLING
# ==============================================================================
print("--- LEVEL 5: Error Handling & 'x' Mode ---")

# 'x' mode sirf tab file banata hai jab wo pehle se maujood na ho
try:
    with open("notes.txt", "x", encoding="utf-8") as f:
        f.write("Test")
except FileExistsError:
    print("⚠️ Error Caught: 'notes.txt' pehle se maujood hai, 'x' mode ne overwrite hone se bacha liya!")

# Agar koi aisi file parhne ki koshish karein jo exist nahi karti:
try:
    with open("ghayab_file.txt", "r") as f:
        print(f.read())
except FileNotFoundError:
    print("⚠️ Error Caught: 'ghayab_file.txt' nahi mili! Program crash hone se bach gaya.\n")


# ==============================================================================
# LEVEL 6: STRUCTURED DATA - CSV FILES (Excel jaisa tabular data)
# ==============================================================================
print("--- LEVEL 6: CSV File Handling ---")

students_data = [
    ["Roll_No", "Name", "Marks", "Grade"],
    [101, "Ali", 92, "A+"],
    [102, "Sara", 85, "A"],
    [103, "Zain", 74, "B"]
]

# CSV Write karna (newline='' lagana zaroori hai taake blank rows na aayein)
with open("students.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerows(students_data)

# CSV Read karna (DictReader se column ke naam se data milta hai - Advanced)
with open("students.csv", "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    print("[CSV Records]:")
    for row in reader:
        print(f"  ID: {row['Roll_No']} | Name: {row['Name']} | Marks: {row['Marks']}")
print()


# ==============================================================================
# LEVEL 7: STRUCTURED DATA - JSON FILES (APIs aur Web Apps ka data)
# ==============================================================================
print("--- LEVEL 7: JSON File Handling ---")

system_config = {
    "app_name": "ZKB Master System",
    "version": 2.5,
    "active": True,
    "skills": ["Python", "Linux", "Cybersecurity", "Data Science"],
    "specs": {"ram": "8GB", "os": "Linux Mint"}
}

# Python Dictionary ko JSON file mein save karna
with open("config.json", "w", encoding="utf-8") as f:
    json.dump(system_config, f, indent=4)  # indent=4 se file khoobsurat format hoti hai

# JSON file ko wapas Python Dictionary mein parhna
with open("config.json", "r", encoding="utf-8") as f:
    loaded_data = json.load(f)
    print(f"[JSON Loaded]: App = {loaded_data['app_name']}, OS = {loaded_data['specs']['os']}\n")


# ==============================================================================
# LEVEL 8: BINARY FILES & PICKLE (PhD / Research / ML Model Saving Level)
# ==============================================================================
print("--- LEVEL 8: Binary Files & Object Serialization (Pickle) ---")

# 1. Raw Binary Write & Read ('wb' aur 'rb' - Images, Audio, ya custom bytes ke liye)
raw_bytes = bytes([65, 66, 67, 68, 10])  # ASCII for ABCD\n
with open("raw_data.bin", "wb") as f:
    f.write(raw_bytes)

with open("raw_data.bin", "rb") as f:
    print("[Raw Binary Data]:", f.read())

# 2. Pickle: Kisi bhi complex Python object (List, Dict, ML Model, Class) ko binary mein save karna
complex_research_data = {"matrix": [[1, 0], [0, 1]], "accuracy": 99.87}
with open("model_checkpoint.pkl", "wb") as f:
    pickle.dump(complex_research_data, f)

with open("model_checkpoint.pkl", "rb") as f:
    restored_object = pickle.load(f)
    print("[Unpickled Object]:", restored_object, "\n")


# ==============================================================================
# LEVEL 9: MODERN FILE SYSTEM MANAGEMENT (pathlib & os module)
# ==============================================================================
print("--- LEVEL 9: File & Folder Management (pathlib) ---")

# Aik naya folder banana
demo_folder = Path("My_Practice_Folder")
demo_folder.mkdir(exist_ok=True)  # Agar pehle se ho to error nahi dega

# File ka size aur details check karna
note_path = Path("notes.txt")
if note_path.exists():
    print(f"File Name: {note_path.name}")
    print(f"File Extension: {note_path.suffix}")
    print(f"File Size: {note_path.stat().st_size} bytes")
    print(f"Absolute Path: {note_path.resolve()}")

# File ko move/rename karna
moved_path = demo_folder / "moved_basic_notes.txt"
if Path("basic_notes.txt").exists():
    Path("basic_notes.txt").replace(moved_path)
    print(f"✅ 'basic_notes.txt' ko '{moved_path}' mein move kar diya gaya.")

# ==============================================================================
# LEVEL 10: CLEANUP (Optional - Testing ke baad kachra saaf karna)
# ==============================================================================
print("\n--- LEVEL 10: Cleanup ---")
# Agar aap chahte hain ke run hone ke baad files delete na hon, to neeche wali lines comment kar dein.
files_to_clean = ["notes.txt", "students.csv", "config.json", "raw_data.bin", "model_checkpoint.pkl"]

for file_name in files_to_clean:
    p = Path(file_name)
    if p.exists():
        p.unlink()  # File delete karne ka modern tareeqa

# Folder ke andar wali file aur phir folder delete karna
if moved_path.exists():
    moved_path.unlink()
if demo_folder.exists():
    demo_folder.rmdir()  # Khali folder delete karta hai

print("🧹 Tamam temporary practice files clean kar di gayin! Masterclass Complete!")