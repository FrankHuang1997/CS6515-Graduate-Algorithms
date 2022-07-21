import GA_ProjectUtils as util
from findX import findXinA
from random import randint

def test(seed=None, size=None, value_override=None):
    findX = util.findX()

    if seed is None:
        seed = randint(1, 9999999999)

    if size is None:
        x = findX.start(seed, 10, 100000)
        size = findX._findX__n
    else:
        x = findX.start(seed, size, size)

    if value_override is not None:
        x = value_override

    try:
        correct_index = findX._findX__A.index(x)
    except ValueError:
        correct_index = None

    print(f'Seed: {seed}, Size: {size}, Index: {correct_index}, X: {x}')

    index, _ = findXinA(x, findX)

    assert index == correct_index, f"Incorrect index reported: {index} != {correct_index}"

test(seed=42, size=32, value_override=-1)
test(seed=42, size=32, value_override=20)
test(seed=42, size=32, value_override=65)

for i in range(16):
    test(size=i + 1)

for i in range(1000):
    test(seed=i + 1)

for _ in range(1000):
    test()