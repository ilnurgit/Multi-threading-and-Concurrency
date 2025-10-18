import threading

list_numbers = [i for i in range(30, 51)]


def even_number(numbers: list[int]) -> None:
    for number in numbers:
        if number % 2 == 0:
            print(f"Number {number} is even")


def odd_number(numbers: list[int]) -> None:
    for number in numbers:
        if not number % 2 == 0:
            print(f"Number {number} is odd")


th1 = threading.Thread(target=even_number, args=(list_numbers,))
th2 = threading.Thread(target=odd_number, args=(list_numbers,))

th1.start()
th2.start()

th1.join()
th2.join()
