from datetime import datetime

_seed = datetime.now().microsecond % 256

def random():
    global _seed
    _seed, carry = divmod(_seed, 2)
    if carry:
        _seed ^= 0xb8
    return _seed

def randrange(i):
    return (random() - 1) * i // 254

nums = set()

for i in range(2550):
    n = random()
    nums.add(n)

assert len(nums) == 255
assert min(nums) == 1
assert max(nums) == 255
