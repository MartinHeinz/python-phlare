import os
import resource
import time

# import profiling modules
from pypprof.net_http import start_pprof_server
import mprofile

INSTANCE = os.environ.get("INSTANCE", "default")
CPU_LOAD = int(os.environ.get("CPU_LOAD", "500"))  # Max recursion around 970
MEMORY_LOAD = int(os.environ.get("MEMORY_LOAD", "700"))
LOAD_TYPE = os.environ.get("LOAD_TYPE", "CPU")  # or MEMORY


def create_smallest_list(size):
    return [None] * (size*100)


def create_small_list(size):
    return [None] * (size*500)


def create_big_list(size):
    return [None] * (size*1000)


def memory_intensive(size):
    smallest_list = create_smallest_list(size)
    small_list = create_small_list(size)
    big_list = create_big_list(size)  # You can't see this in flame graph, you would need line profiler for this
    del big_list
    return smallest_list, small_list


def partition(array, begin, end):
    pivot = begin
    for i in range(begin+1, end+1):
        if array[i] <= array[begin]:
            pivot += 1
            array[i], array[pivot] = array[pivot], array[i]
    array[pivot], array[begin] = array[begin], array[pivot]
    return pivot


def quicksort(array, begin=0, end=None):
    if end is None:
        end = len(array) - 1

    def _quicksort(array, begin, end):
        if begin >= end:
            return
        pivot = partition(array, begin, end)
        _quicksort(array, begin, pivot-1)
        _quicksort(array, pivot+1, end)
    return _quicksort(array, begin, end)


def set_max_memory():
    soft, hard = resource.getrlimit(resource.RLIMIT_AS)
    resource.setrlimit(resource.RLIMIT_AS, (500000000, hard))  # 500 MB


if __name__ == "__main__":
    # start memory profiling
    print(f"Starting service instance: {INSTANCE}")
    mprofile.start(sample_rate=128 * 1024)

    # enable pprof http server
    start_pprof_server(host='0.0.0.0', port=8081)

    set_max_memory()

    def load_cpu():
        import random
        random_numbers = random.sample(range(0, CPU_LOAD), CPU_LOAD)
        while True:
            time.sleep(0.5)
            print(f"Computing 'quicksort(...)'...")
            quicksort(random_numbers)

    def load_memory():
        print(f"Computing 'memory_intensive({MEMORY_LOAD})'...")
        allocated = memory_intensive(MEMORY_LOAD)
        while True:
            time.sleep(5)
            print(f"Data was allocated, sleeping...")

    if LOAD_TYPE == "CPU":
        load_cpu()
    elif LOAD_TYPE == "MEMORY":
        load_memory()
    else:
        print("Invalid 'LOAD_TYPE'")
        time.sleep(5)
        exit(1)
