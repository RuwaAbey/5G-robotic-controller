import asyncio
import time

async def brewCoffee():
    print('Start brewCoffee()')
    #use awai with awaitable commands
    await asyncio.sleep(3)
    print('End brewCoffee')
    return "Coffee Ready"

async def toastBagel():
    print("Start toastBagel()")
    await asyncio.sleep(2)
    print("End toastBagel")
    return "Bagel toasted"

async def main():
    start_time = time.time()

    #batch approach in routines
    batch = asyncio.gather(brewCoffee(), toastBagel())
    result_coffee, result_bagel =  await batch

    end_time = time.time()
    elapsed_time = end_time - start_time

    print(f"Result of brewCoffee: {result_coffee}")
    print(f"Result of toastBagel: {result_bagel}")
    print(f"Total execution time: {elapsed_time:.2f} seconds")

if __name__ == '__main__':
    asyncio.run(main())
