
"""
21.08, nash
    시간 체크용 클래스 작성
"""
import time
from time import (
    process_time,
    perf_counter,
    sleep,
)


class Timer:
    """perf_counter timer
    21.08, nash
    """

    def __init__(self):
        self.pc1 = 0
        self.pc2 = 0
        pass

    def clear(self):
        self.pc1 = self.pc2

    def check(self):
        self.pc1 = self.pc2
        self.pc2 = perf_counter()
        print(f'time delta: {self.pc2 - self.pc1:.6f} s')

    def diff(self):
        self.pc1 = self.pc2
        self.pc2 = perf_counter()
        return self.pc2 - self.pc1

    def delay_sec(self, delay):
        """testing..."""
        start = perf_counter()
        while perf_counter() - start < delay:
            pass
        return perf_counter() - start


def main():
    t1 = Timer()
    print('perf_counter started.')

    t1.clear()
    for i in range(10):
        t1.check()

    print('delay start')
    t1.clear()
    t1.delay_sec(2)
    t1.check()
    print('delay end')


if __name__ == '__main__':
    main()

