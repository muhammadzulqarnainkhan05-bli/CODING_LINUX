email = input("Give Email:")
if email=="":
    email="abc@gmail.com"

if "@" in email and ".com" in email:
    print("MAIL shi hai")
else:
    print("gmail shhi nhi hai")