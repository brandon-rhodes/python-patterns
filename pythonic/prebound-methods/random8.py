from datetime import datetime

class Random8(object):
    def __init__(self, seed=None):
        if seed is None:
            seed = datetime.now().microsecond % 256
        self.seed = seed

    def random(self):
        self.seed, carry = divmod(self.seed, 2)
        if carry:
            self.seed ^= 0xb8
        return self.seed

    def randrange(self, i):
        return (self.random() - 1) * i // 254

_instance = Random8()

random = _instance.random
randrange = _instance.randrange

nums = set()

for i in range(2550):
    n = _random8.random()
    nums.add(n)

assert len(nums) == 255
assert min(nums) == 1
assert max(nums) == 255
