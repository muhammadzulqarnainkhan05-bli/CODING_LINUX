prices = {"chawal": 300, "cheeni": 150, "chai": 500, "doodh": 200}
bill = []      # kharidi hui cheezein yahan jama hongi
total = 0

while True:
    print(f"Available items: {list(prices.keys())}")
    print("=" * 30)
    khareed = input("Kya lena hai? (khatam karna ho to likho: bas): ")
    if khareed == "bas":
        break

    if khareed in prices:
        try:
            miqdar = int(input("Kitni miqdar: "))
        except ValueError:
            print("Number likho bhai!")
            continue
        raqam = prices[khareed] * miqdar
        bill.append((khareed, miqdar, raqam))
        total = total + raqam
    else:
        print("Ye mojood nahi hai!")

# ---- Bill print karna ----
print("=" * 30)
print("BILL")
for naam, miqdar, raqam in bill:
    print(f"{naam} x {miqdar} = {raqam}")

# ---- Discount wala hissa ----
discount = 0
if total > 1000:
    discount = total * 0.10

pay = total - discount

print("-" * 30)
print(f"Total = {total}")
print(f"Discount = {discount}")
print(f"Pay karo = {pay}")