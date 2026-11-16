# while True:
#     try:

#         list1 = []
#         for i in range(1,4):
#             a= int(input(f"Input number({i}):"))
#             list1.append(a)

#         print("="*8+" ALL SUM "+"="*8)
#         print(sum(list1))
#         print("="*8+" Maximum No."+"="*8)
#         print(max(list1))
#         print("="*8+" Minimum No."+"="*8)
#         print(min(list1))
#         print("="*20)
#         print("="*8+" Average "+"="*8)
#         print(f"Average of the list is: {(sum(list1))/len(list1)}")
#         print("_"*20)
#     except ValueError:
#         print("Value shi do bhai!")



# -------By HELP OF Ai-------------------#

while True:
    list1 = []
    for i in range(1, 6):
        while True:
            try:
                a = int(input(f"Input number({i}): "))
                list1.append(a)
                break
            except ValueError:
                print("Value shi do bhai!")

    print("="*8 + " ALL SUM " + "="*8)
    print(sum(list1))
    print("="*8 + " Maximum No. " + "="*8)
    print(max(list1))
    print("="*8 + " Minimum No. " + "="*8)
    print(min(list1))
    print("="*8 + " Average " + "="*8)
    print(sum(list1) / len(list1))
    print("="*8 + " Sorted " + "="*8)
    print(sorted(list1))
    print("_"*20)

    again = input("Dobara chalana hai? (y/n): ")
    if again != "y":
        break