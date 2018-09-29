from datetime import datetime

class Random8(object):
    def __init__(self):
        self.set_seed(datetime.now().microsecond % 255 + 1)

    def set_seed(self, value):
        self.seed = value

    def random(self):
        self.seed, carry = divmod(self.seed, 2)
        if carry:
            self.seed ^= 0xb8
        return self.seed

_instance = Random8()

random = _instance.random
set_seed = _instance.set_seed

nums = set()

for i in range(2550):
    n = _instance.random()
    nums.add(n)

assert len(nums) == 255
assert min(nums) == 1
assert max(nums) == 255
