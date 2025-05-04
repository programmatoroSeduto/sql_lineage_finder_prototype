
lines = set()
with open('./sql keywords.txt', 'r') as fil:
    lines = set([ x.strip().upper() for x in fil.readlines()])

print(lines)