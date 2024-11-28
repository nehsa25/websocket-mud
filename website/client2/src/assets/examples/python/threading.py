import asyncio
from concurrent.futures import ThreadPoolExecutor
from itertools import starmap
import os
import time
import jsonpickle
import random
from xml.dom import minidom
import unicodedata
import re
from multiprocessing import Pool, Process
import numpy

class ThreadingExamples:

    class ThreadingExamplesType:
        method = ""
        timing = 0.0

        def __init__(self, method, timing):
            a = ArtGenerator()
            self.method = method
            self.timing = timing
            # self.shape = a.generate_svg(1 + int(float(timing)))
            
            #   # Write SVG content to a file (optional)
            # cleaned_filename = a.clean_filename_windows(f"{method}_random_shapes.svg")
            # with open(cleaned_filename, "w") as f:
            #     f.write(self.shape)
                
        def to_json(self):
            return jsonpickle.encode(self)

    number_iterations = 0

    def __init__(self, number_iterations=10):
        self.number_iterations = number_iterations

    # sync
    def sleep_sync_example(self, sleep):
        for i in range(self.number_iterations):
            time.sleep(sleep)
            
    # sync find max element   
    def maxe_sync_example(self, items):
        for i in range(self.number_iterations):
            self.find_max_element(items)

    # thread - executor.submit
    def sleep_thread_example(self, sleep=.1):
        time.sleep(sleep)

    def sleep_async_threading_submit_example(self, sleep):
        with ThreadPoolExecutor() as executor:
            executor.submit(self.sleep_thread_example, range(self.number_iterations), [sleep])
            
    # thread - find max
    def maxe_thread_example(self, items):
        self.find_max_element(items)

    def maxe_async_threading_submit_example(self, sleep):
        with ThreadPoolExecutor() as executor:
            executor.submit(self.maxe_thread_example, range(self.number_iterations), [sleep])

    def sleep_async_threading_map_example(self, sleep):
        if sleep == .1:
            with ThreadPoolExecutor() as executor:
                executor.map(self.sleep_thread_example, range(self.number_iterations))
              
    # multiprocess  
    def sleep_process_example(self, sleep=.1):
        time.sleep(sleep)
        
    def sleep_multiprocess_example(self, s, num_processes=4):    
        data_list = [(s,), (s,), (s,), (s,)] 
        with Pool(processes=num_processes):  # Adjust the number of processes as needed
            results = starmap(self.sleep_process_example, data_list)

    # asyncio sleep
    async def sleep_asyncio_example(self, sleep):
        await asyncio.sleep(sleep)

    async def sleep_asyncio_thread_example(self, sleep):
        tasks = []
        for i in range(self.number_iterations):
            tasks.append(asyncio.create_task(self.sleep_asyncio_example(sleep)))
        await asyncio.gather(*tasks)
        
    # asyncio find max element
    async def maxe_asyncio_example(self, items):
        await self.async_find_max_element(items)

    async def maxe_asyncio_thread_example(self, items):
        tasks = []
        for i in range(self.number_iterations):
            tasks.append(asyncio.create_task(self.maxe_asyncio_example(items)))
        await asyncio.gather(*tasks)

    def find_max_element(self, items):
        max_value = items[0]  
        for element in items:
            if element is None or element > max_value:
                max_value = element
        return max_value
    
    async def async_find_max_element(self, items):
        max_value = items[0]  
        for element in items:
            if element > max_value:
                max_value = element
        return max_value


# sync example:
# ITERATIONS = [1]
# SLEEPS = [.1]

ITERATIONS = [1,2, 10, 50, 100]
TESTS = [(.1, 1000), (.1, 10000), (.1, 100000), (.1, 1000000), (.1, 10000000), (.1, 100000000)]
timings = []

start_test = time.perf_counter()


# threading submit sleep
for i in ITERATIONS:
    for s in TESTS:
        t = ThreadingExamples(i)
        seconds = s[0]
        items = numpy.empty(s[1], dtype=object)
        
        # sync sleep
        start = time.perf_counter()
        t.sleep_sync_example(seconds)
        stop = time.perf_counter()
        timings.append(
            ThreadingExamples.ThreadingExamplesType(f"Sync [Sleep], iterations: {i}, sleep: {seconds}", f"{stop - start:.5f}")
        )
        
        # sync find max
        start = time.perf_counter()
        t.maxe_sync_example(items)
        stop = time.perf_counter()
        timings.append(
            ThreadingExamples.ThreadingExamplesType(f"Sync  [O(n) Linear], iterations: {i}, number of items: {len(items)}", f"{stop - start:.5f}")
        )
        
        # threading submit sleep
        start = time.perf_counter()
        t.sleep_async_threading_submit_example(s)
        stop = time.perf_counter()
        timings.append(
            ThreadingExamples.ThreadingExamplesType(f"Threading [Sleep], iterations: {i}, sleep: {seconds}", f"{stop - start:.5f}")
        )
        
        # threading submit find max
        start = time.perf_counter()
        t.maxe_async_threading_submit_example(items)
        stop = time.perf_counter()
        timings.append(
            ThreadingExamples.ThreadingExamplesType(f"Threading  [O(n) Linear], iterations: {i}, number of items: {len(items)}", f"{stop - start:.5f}")
        )

        # # threading map sleep
        # start = time.perf_counter()
        # t.sleep_async_threading_map_example(s)
        # stop = time.perf_counter()
        # timings.append(
        #     ThreadingExamples.ThreadingExamplesType(f"Threading (map), iterations: {i}, sleep: {seconds}", f"{stop - start:.5f}")
        # )
        
        # multiprocess example
        start = time.perf_counter()
        num_processes = 4
        t.sleep_multiprocess_example(s, num_processes)
        stop = time.perf_counter()
        timings.append(
            ThreadingExamples.ThreadingExamplesType(f"Multi-process [Sleep], iterations: {i}, sleep: {seconds}", f"{stop - start:.5f}")
        )     
        
        # multiprocess example big O complexity is O(n)
        start = time.perf_counter()
        num_processes = 4
        items = [s * 1000]
        t.sleep_multiprocess_example(items, num_processes)
        stop = time.perf_counter()
        timings.append(
            ThreadingExamples.ThreadingExamplesType(f"Multi-process [O(n) Linear], iterations: {i}, number of items: {len(items)}", f"{stop - start:.5f}")
        )   

        # asyncio example sleep
        loop = asyncio.new_event_loop()
        start = time.perf_counter()
        loop.run_until_complete(t.sleep_asyncio_thread_example(seconds))
        stop = time.perf_counter()
        timings.append(
            ThreadingExamples.ThreadingExamplesType(f"asyncio [Sleep], iterations: {i}, sleep: {seconds}", f"{stop - start:.5f}")
        )
        
        # asyncio example find max
        loop = asyncio.new_event_loop()
        start = time.perf_counter()
        loop.run_until_complete(t.maxe_asyncio_thread_example(items))
        stop = time.perf_counter()
        timings.append(
            ThreadingExamples.ThreadingExamplesType(f"asyncio [O(n) Linear], iterations: {i}, sleep: {seconds}", f"{stop - start:.5f}")
        )
        

end_test = time.perf_counter()
print(f"{end_test - start_test:.5f} seconds")

results = sorted(timings, key=lambda x: x.timing)
print(f"Results from threading examples, quickest first:")
for result in results:
    print(f"{result.method} took {result.timing} seconds")

    with open("art.html", "w") as fj:   
        fj.write(f"<html><body>")
        
        for f in os.listdir('.'):
            if f.endswith('.svg'):
                fj.write(f"<img src='{f}'></body></html>")
        fj.write(f"</body></html>")
            

# # string formatting
# super_long_number = 12345678923423.4234234230
# print(f"super_long_number: {super_long_number}")

# # percision formatting
# print(f"super_long_number with .2f: {super_long_number:,.2f}")

# # percision formatting
# print(f"super_long_number with .2f: {super_long_number:,.2f}")
# # no decimal formatting
# super_long_number = 12345678923423.4234234230
# print(f".0f Number: {super_long_number:.0f}")


# super_long_number = 12345678923423.4234234230
# print(f".2 Number: {super_long_number:.2}")
# super_long_number = 12345678923423.4234234230
# print(f".2e Number: {super_long_number:.2e}")


# class GameOfThronesDragons(Enum):
#     DROGON = 1
#     RHAEGAL = 2
#     VISERION = 3


# print(
#     f"Who's a cute little dragon? Yes, {GameOfThronesDragons.DROGON.name} is a cute little dragon!"
# )


# class Monsters(Enum):
#     SKELETON = 1
#     ZOMBIE = 2


# print(f"A rotting {random.choice(list(Monsters)).name.lower()} is to your left?")
