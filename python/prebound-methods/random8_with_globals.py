from datetime import datetime

_seed = datetime.now().microsecond % 255 + 1

def set_seed(value):
    global _seed
    _seed = value

def random():
    global _seed
    _seed, carry = divmod(_seed, 2)
    if carry:
        _seed ^= 0xb8
    return _seed

nums = set()

for i in range(2550):
    n = random()
    nums.add(n)

assert len(nums) == 255
assert min(nums) == 1
assert max(nums) == 255

set_seed(1)
