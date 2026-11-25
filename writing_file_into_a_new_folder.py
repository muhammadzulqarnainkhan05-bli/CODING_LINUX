import os

os.makedirs("written_files", exist_ok=True)

inp = input("Kia karna hai:\n1. Write in file\n2. Show file text\nWrite 1/2: ").strip()

if inp == "1":
    filename = input("File ka name kia ho: ")
    likhawat = input("Write: ")
    with open(f"written_files/{filename}.txt", "w") as f:
        f.write(likhawat)
    print("Save ho gaya")

elif inp == "2":
    filepath = input("File ka path batao: ")
    try:
        with open(filepath, "r") as f:
            print("File mein likha hai:\n", f.read())
    except FileNotFoundError:
        print("Yeh file nahi mili")

else:
    print("Bhai sahi likho, 1 ya 2")