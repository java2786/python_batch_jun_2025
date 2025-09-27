
from threading import Thread
import time


class CountingThread(Thread):
    ct = "CT"
    def run(self):
        for i in range(1,1000):
            print(f"{self.ct} is running: {i}")
            
            
class AlphabetThread(Thread):
    ct = "AT"
    alphbets = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    def run(self):
        for j in range(1,27):
            for i in range(26):
                print(f"{self.ct} is running: {j}:{self.alphbets[i]}")
                time.sleep(1/100)
            
            
t1 = CountingThread()
t2 = AlphabetThread()


# t1.run()

# t2.run()
t2.start()

t1.start()
