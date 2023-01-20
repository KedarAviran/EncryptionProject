import random

possibleValues = set(range(65, 123))
possibleValues.remove(91)
possibleValues.remove(92)
possibleValues.remove(93)
possibleValues.remove(94)
possibleValues.remove(95)
possibleValues.remove(96)
key = ''
for i in possibleValues.copy():
    rnd = 65
    while not (rnd in possibleValues) or (91 <= rnd <= 96):
        rnd = random.randrange(65, 123)
    key = key + chr(i) + ' ' + chr(rnd) + '\n'
    possibleValues.remove(rnd)

with open('key.txt', 'w') as key_file:
    key_file.write(key)
