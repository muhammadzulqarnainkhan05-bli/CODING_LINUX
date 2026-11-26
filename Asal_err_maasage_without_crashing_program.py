# yaha program ni ruky ga or bas err dikha ker agly chaly ga
# try:
#     x = int(input("N:"))
# except ValueError as e:
#     print("Masla:", e)
#-----------yahan ab program ruky ga or crash ho ga ---------
# x = int("ab")
# print(x)


# difference:
try:
    x = int("ab")
except ValueError as e:
    print("Masla:", e)

print("Program aage chal raha hai")