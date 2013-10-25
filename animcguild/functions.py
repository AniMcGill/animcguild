from random import SystemRandom

def roll(number,sides):
    rand = SystemRandom()
    val = 0
    for x in range (0, number):
        val += rand.randint(1,sides)
    return val
