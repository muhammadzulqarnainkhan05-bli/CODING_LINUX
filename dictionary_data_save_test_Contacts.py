# Contacts = {}

# for i in range(1,4):
#     keyfrContacts=input(f"Key {i} :")
#     valfrContacts=input(f"Value {i}:")
#     Contacts[keyfrContacts]=valfrContacts

# print(Contacts)



contacts = {}

# 3 contacts lena
for i in range(1, 4):
    naam = input(f"Naam {i}: ")
    number = input(f"Number {i}: ")
    contacts[naam] = number

print("="*20)
print("Saved contacts:", contacts)
print("="*20)

# Search karna
search = input("Kis ka number chahiye? ")

if search in contacts:
    print(f"{search} ka number hai: {contacts[search]}")
else:
    print("Yeh contact nahi hai")