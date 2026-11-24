# def pahada(a=2, b=10):  # a = pahada, b = kitni dafa
#     for i in range(1, b + 1):
#         print(f"{a} x {i} = {a * i}")



# pahada(5, 5)

# def average(b=[2,4,8,13,5,11]):
#     lenofb = len(b)
#     sumofallinb = sum(b)
#     averageofatmostb=sumofallinb/lenofb
#     print(f"The Average of your list or give numbers is {averageofatmostb}")


# average()
def average(b=[2, 4, 8, 13, 5, 11]):
    return sum(b) / len(b)

print(average())                   # 7.166666666666667
print(average([10, 20, 30]))       # 20.0

x = average([10, 20, 30])
print(f"Double average: {x * 2}")  # 40.0
