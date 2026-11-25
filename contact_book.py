import os

# ---------- Folder aur file ka raasta ----------
os.makedirs("wrifi", exist_ok=True)
CONTACTS_PATH = "wrifi/contacts.txt"
STORY_PATH = "wrifi/story.txt"


# ---------- Contact Book ke functions ----------
def load_contacts():
    contacts = {}
    try:
        with open(CONTACTS_PATH, "r") as f:
            for line in f:
                line = line.strip()
                if line:
                    naam, number = line.split(",")
                    contacts[naam] = number
    except FileNotFoundError:
        pass
    return contacts


def save_contacts(contacts):
    with open(CONTACTS_PATH, "w") as f:
        for naam, number in contacts.items():
            f.write(f"{naam},{number}\n")


def contact_book():
    contacts = load_contacts()
    while True:
        print("\n--- CONTACT BOOK ---")
        print("1. Add  2. Dekho  3. Search  4. Delete  5. Wapis")
        choice = input("Chunein: ").strip()

        if choice == "1":
            naam = input("Name: ").strip().title()
            number = input("Number: ").strip()
            contacts[naam] = number
            save_contacts(contacts)
            print("Save ho gaya")

        elif choice == "2":
            if not contacts:
                print("Koi contact nahi")
            for naam, number in contacts.items():
                print(f"{naam}: {number}")

        elif choice == "3":
            naam = input("Kis ka number chahiye? ").strip().title()
            if naam in contacts:
                print(f"{naam}: {contacts[naam]}")
            else:
                print("Yeh contact nahi hai")

        elif choice == "4":
            naam = input("Kis ko delete karna hai? ").strip().title()
            if naam in contacts:
                del contacts[naam]
                save_contacts(contacts)
                print("Delete ho gaya")
            else:
                print("Yeh contact nahi hai")

        elif choice == "5":
            break

        else:
            print("1 se 5 ke beech likho")


# ---------- Story Counter ----------
def story_counter():
    try:
        with open(STORY_PATH, "r") as f:
            text = f.read()
    except FileNotFoundError:
        print(f"{STORY_PATH} nahi mili. Pehle yeh file banayein.")
        return

    words = text.split()
    if not words:
        print("File khali hai")
        return

    longest = words[0]
    for w in words:
        if len(w) > len(longest):
            longest = w

    print("=" * 30)
    print("Characters:", len(text))
    print("Words:", len(words))
    print("Lines:", len(text.splitlines()))
    print("Sab se lamba word:", longest)
    print("=" * 30)


# ---------- Story likhna ----------
def write_story():
    line = input("Story ki line likho: ")
    with open(STORY_PATH, "a") as f:
        f.write(line + "\n")
    print("Add ho gayi")


# ---------- Main menu ----------
while True:
    print("\n===== MAIN MENU =====")
    print("1. Contact Book")
    print("2. Story likho")
    print("3. Story Counter")
    print("4. Exit")
    choice = input("Chunein: ").strip()

    if choice == "1":
        contact_book()
    elif choice == "2":
        write_story()
    elif choice == "3":
        story_counter()
    elif choice == "4":
        print("Khuda hafiz")
        break
    else:
        print("1 se 4 ke beech likho")