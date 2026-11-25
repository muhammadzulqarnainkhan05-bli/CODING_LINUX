contacts = {"Ali":311223344984,
            "Hammad":11332948402,
            "Dasnish":843243436273
            }
import os
os.makedirs("wrifi", exist_ok=True)

with open("wrifi/contacts.txt", "a") as file:
    for name,number in contacts.items():
        file.write(f"{name},{number}\n")


contacts1={}
with open("wrifi/contacts.txt","r") as file1:
    for line in file1:
        line=line.strip()
    if line:
        name,number=line.split(",")
        contacts1[name]=number
        