while True:
    try:
        user = int(input("Age:"))
        print("Apki Umar",user," sall hai")
    except ValueError as err:
        print(f"Bhai err ye hai:\n{err}")
    else:
        print("END")