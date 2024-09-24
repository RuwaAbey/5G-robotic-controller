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

    #task approach in routines
    cofee_task = asyncio.create_task(brewCoffee())
    toast_task = asyncio.create_task(toastBagel())

    result_coffee = await cofee_task
    result_bagel = await toast_task

    end_time = time.time()
    elapsed_time = end_time - start_time

    print(f"Result of brewCoffee: {result_coffee}")
    print(f"Result of toastBagel: {result_bagel}")
    print(f"Total execution time: {elapsed_time:.2f} seconds")

if __name__ == '__main__':
    asyncio.run(main())
