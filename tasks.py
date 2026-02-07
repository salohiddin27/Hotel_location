from turtle import *
import math


# Sozlamalar
speed(0)
setup(800, 800)
setposition(-40, -30)
bgcolor("black")
color("aqua")

# Chizish jarayoni
for i in range(160):
    rt(i)
    circle(170, i)
    fd(100)
    right(240)
    fd(i)
    lt(1)


# Ekran sozlamalari
bgcolor("black")
speed(0) # Eng tez tezlik
color("red")
pensize(2)

def heart(n):
    # Yurak shaklining matematik formulasi
    x = 15 * math.sin(n)**3
    y = 12 * math.cos(n) - 5 * \
        math.cos(2*n) - 2 * \
        math.cos(3*n) - \
        math.cos(4*n)
    return x, y

# Bir nechta yuraklarni chizish
for i in range(1, 18):
    penup()
    goto(0, 0) # Markazga qaytish
    pendown()
    for j in range(0, 100):
        x, y = heart(j/15)
        goto(x*i, y*i) # Har bir yurakni i marta kattalashtirish

hideturtle()
done()

hideturtle()
done()