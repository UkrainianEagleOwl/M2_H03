import time
import multiprocessing

def get_factors(num):
    factors = []
    for i in range(1, num + 1):
        if num % i == 0:
            factors.append(i)
    return factors
    
def simple_factorize(*number):
    result = []
    for num in number:
        factors = get_factors(num)
        result.append(factors)

    return result

def parallel_factorize(*number):
    num_cores = multiprocessing.cpu_count()
    with multiprocessing.Pool(num_cores) as pool:
        results = pool.map(get_factors, number)
    return results

if __name__ == '__main__':
    multiprocessing.freeze_support()
    start_time_simple = time.time()
    a, b, c, d  = simple_factorize(128, 255, 99999, 10651060)
    end_time_simple = time.time()

    start_time = time.time()
    a, b, c, d  = parallel_factorize(128, 255, 99999, 10651060)
    end_time = time.time()


    assert a == [1, 2, 4, 8, 16, 32, 64, 128]
    assert b == [1, 3, 5, 15, 17, 51, 85, 255]
    assert c == [1, 3, 9, 41, 123, 271, 369, 813, 2439, 11111, 33333, 99999]
    assert d == [1, 2, 4, 5, 7, 10, 14, 20, 28, 35, 70, 140, 76079, 152158, 304316, 380395, 532553, 760790, 1065106, 1521580, 2130212, 2662765, 5325530, 10651060]

    print("Execution time with one process:", end_time_simple - start_time_simple, "seconds")
    print("Execution time with multiprocess:", end_time- start_time, "seconds")