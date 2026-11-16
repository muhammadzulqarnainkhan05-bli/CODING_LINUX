# Part 1: 1 se 10 tak numbers, asan kam 
for i in range(1, 11):
    print(i)

print("=" * 30)

# Part 2: user ke number ka pahada, thora mushkil
while True:
    try:
        phada = int(input("Kiss No. ka Phada Chahiye: "))
        times = int(input("Kitny times Chahiye: "))
        for i in range(1, times + 1):
            print(f"{phada} x {i} = {phada * i}")
        break
    except ValueError:
        print("Bhai number do, alphabet nahi.")