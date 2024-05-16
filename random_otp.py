import random        
a1 = random.randint(0,9)
a2 = random.randint(0,9)
ac = list('abcdefghijklmnopqrstuvxyz')
a3 = random.choice(ac)
AC = list('ABCDEFGHJKLMNOPQRSTUVXYZ')
a4 = random.choice(AC)
sc = list('!@#$%^&*_')
a5 = random.choice(sc)

a6 = random.choice(ac)
a7 = random.choice(AC)
a8 = random.randint(0,9)
otp = [a1,a2,a3,a4,a5,a6,a7,a8]
print(otp)
random.shuffle(otp)
otp = "".join(map(str, otp))
print(otp)