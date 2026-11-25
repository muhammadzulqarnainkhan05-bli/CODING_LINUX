import os

# ---------- Folder banana (na ho to) ----------
os.makedirs("written_files", exist_ok=True)


# ---------- Functions ----------
def file_path(naam):
    """Naam se poora raasta banata hai: written_files/naam.txt"""
    return f"written_files/{naam}.txt"


def write_file(naam, text):
    """"w": purana sab mita kar naya likhta hai"""
    with open(file_path(naam), "w") as f:
        f.write(text + "\n")


def append_file(naam, text):
    """"a": purane ke neeche jorta hai"""
    with open(file_path(naam), "a") as f:
        f.write(text + "\n")


def read_file(naam):
    """"r": parhta hai, file na ho to None wapis"""
    try:
        with open(file_path(naam), "r") as f:
            return f.read()
    except FileNotFoundError:
        return None


def show_lines(naam):
    """Line number ke saath dikhata hai"""
    try:
        with open(file_path(naam), "r") as f:
            n = 1
            for line in f:
                print(f"{n}: {line.strip()}")
                n += 1
    except FileNotFoundError:
        print("Yeh file nahi mili")


def list_files():
    """written_files ki sari files ke naam"""
    files = os.listdir("written_files")
    if not files:
        print("Abhi koi file nahi")
    for f in files:
        print("-", f.replace(".txt", ""))


def delete_file(naam):
    try:
        os.remove(file_path(naam))
        print("Delete ho gayi")
    except FileNotFoundError:
        print("Yeh file nahi mili")


# ---------- Menu ----------
while True:
    print("\n" + "=" * 30)
    print("1. Nayi file likho   (w: purana mit jayega)")
    print("2. File mein add karo (a: purana bacha rahega)")
    print("3. File parho")
    print("4. Line number ke saath dekho")
    print("5. Sari files ki list")
    print("6. File delete karo")
    print("7. Exit")
    choice = input("Chunein: ").strip()

    if choice == "1":
        naam = input("File ka naam: ").strip()
        text = input("Likho: ")
        write_file(naam, text)
        print("Save ho gaya")

    elif choice == "2":
        naam = input("File ka naam: ").strip()
        text = input("Add karo: ")
        append_file(naam, text)
        print("Add ho gaya")

    elif choice == "3":
        naam = input("File ka naam: ").strip()
        data = read_file(naam)
        if data is None:
            print("Yeh file nahi mili")
        else:
            print("File mein likha hai:\n" + data)

    elif choice == "4":
        naam = input("File ka naam: ").strip()
        show_lines(naam)

    elif choice == "5":
        list_files()

    elif choice == "6":
        naam = input("File ka naam: ").strip()
        delete_file(naam)

    elif choice == "7":
        print("Khuda hafiz")
        break

    else:
        print("Ghalat option, 1 se 7 likho")