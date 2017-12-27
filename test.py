import _thread, _threading_local, threading
import time


# Define a function for the thread
def print_time(threadName, delay):
    count = 0
    while count < 5:
        time.sleep(delay)
        count += 1
        print("%s: %s" % (threadName, time.ctime(time.time())))



_return_thread_1 = None
_return_thread_2 = None
# Create two threads as follows
_thread_1 = threading.Thread(target=print_time, args=("Thread-1", 2, _return_thread_1))
_thread_2 = threading.Thread(target=print_time, args=("Thread-2", 4, _return_thread_2))

_thread_1.start()
_thread_2.start()

print(_return_thread_1, _return_thread_2)

_thread_1.join()
_thread_2.join()
print(_return_thread_1, _return_thread_2)
print("Exit")
