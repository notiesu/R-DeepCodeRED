import aiohttp
import asyncio
import urllib.parse
from concurrent.futures import ProcessPoolExecutor

def cpu_bound_task(data):
    # Placeholder for CPU-intensive processing
    return data

async def fetch_data(session, url, headers):
    async with session.get(url, headers=headers) as response:
        data = await response.json()  # Assuming the response is JSON
        return data

async def process_data(executor, data):
    loop = asyncio.get_running_loop()
    processed_data = await loop.run_in_executor(executor, cpu_bound_task, data)
    return processed_data

async def fetch_and_process(session, executor, url, headers):
    # Fetch data
    fetched_data = await fetch_data(session, url, headers)
    # Process the fetched data using multiprocessing for CPU-bound tasks
    processed_data = await process_data(executor, fetched_data)
    return processed_data

async def main():
    token = '1T49dq5TgTgaXPhlJqZLbSAlrG7c'
    headers = {'Authorization': 'Bearer ' + token}

    example_query = {
        "destinationLocationCode": "SYD",
        "originLocationCode": "BKK",
        "departureDate": "2024-10-16",
        "returnDate": "2024-10-18",
        "adults": "1"
    }

    base_url = "https://test.api.amadeus.com/v2/shopping/flight-offers"
    query_string = urllib.parse.urlencode(example_query)
    url = f"{base_url}?{query_string}"

    urls = [url] * 10  # Adjust the number as necessary

    executor = ProcessPoolExecutor()

    async with aiohttp.ClientSession() as session:
        results = []
        for url in urls:
            result = await fetch_and_process(session, executor, url, headers)
            results.append(result)
            await asyncio.sleep(1)  # Sleep for 1 second between each API call

        # Print or further process the results
        for result in results:
            print(result)

if __name__ == "__main__":
    asyncio.run(main())
