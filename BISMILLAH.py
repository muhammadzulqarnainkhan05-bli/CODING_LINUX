money = 1000

while True:
    inp = input("Input:")
    if inp == "help":
        print("-"*30)
        print("--------HELP--------")
        print("\nType:")
        print("1 for takng out money.")
        print("2 for check money.")
        print("-"*30)
    elif inp == "2":
        print("Your current money is: ", money)

    elif inp == "1":
        amount = int(input("Enter amount to withdraw: "))
        if amount <= money:
            money -= amount
            print("Money withdrawn successfully.")
        else:
            print("Insufficient funds.")
    else:
        print("Invalid input. Type 'help' for options.")

    if input("Do you want to continue? (yes/no): ").lower() != "yes":
        break
    else:
        print("Continuing...")
    if input("Do you want to exit? (yes/no): ").lower() == "yes":
        print("Exiting the program.")
        break
    else:
        print("Continuing...")
    if input("Do you want to restart? (yes/no): ").lower() == "yes":
        print("Restarting the program.")
        money = 1000  # Reset money to initial value
    else:
        print("Continuing...")
    if input("Do you want to reset money? (yes/no): ").lower() == "yes":
        money = 1000  # Reset money to initial value
        print("Money has been reset to 1000.")
    else:
        print("Continuing...")
    