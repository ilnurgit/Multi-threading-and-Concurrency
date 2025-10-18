import threading


def factorial(n: int) -> int:
    result = 1
    if n == 0 or n == 1:
        return 1
    for i in range(1, n + 1):
        result *= i
    return result


def calculate_factorial(n):
    print(f"\nCalculating factorial of {n} in thread {threading.current_thread().name}")
    result = factorial(n)
    print(f"Factorial of {n} is {result} in thread {threading.current_thread().name}")


n = 12

thread1 = threading.Thread(target=calculate_factorial, args=(n,))
thread2 = threading.Thread(target=calculate_factorial, args=(n,))

thread1.start()
thread2.start()

thread1.join()
thread2.join()
