import time

def brewCoffee():
    print('Start brewCoffee()')
    time.sleep(3)
    print('End brewCoffee')
    return "Coffee Ready"

def toastBagel():
    print("Start toastBagel()")
    time.sleep(2)
    print("End toastBagel")
    return "Bagel toasted"

def main():
    start_time = time.time()

    result_coffee = brewCoffee()
    result_bagel = toastBagel()

    end_time = time.time()
    elapsed_time = end_time - start_time

    print(f"Result of brewCoffee: {result_coffee}")
    print(f"Result of toastBagel: {result_bagel}")
    print(f"Total execution time: {elapsed_time:.2f} seconds")

if __name__ == '__main__':
    main()
