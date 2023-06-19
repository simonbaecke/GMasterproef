import math

def round_up(n, decimals=0):
    multiplier = 10 ** decimals
    return math.ceil(n * multiplier) / multiplier

locald = {"B2":20,"B1":10, "A20": 300}
globalsd = globals()


b="R4 = min(10000,round_up((B2-B1)*50,-3))"

exec(b,globalsd,locald)


print(eval("[B2-B1,A20]",locald))
