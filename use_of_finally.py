try:
    f = open("data.txt", "r")
    print(f.read())
except FileNotFoundError as e:
    print("File nahi mili")
    print(e)
finally:
    print("Program khatam")
    