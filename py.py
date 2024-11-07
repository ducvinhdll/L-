import aiohttp
import asyncio
import time

async def send_request(url):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    print(f"Request sent to {url} with status: {response.status}")
                else:
                    print(f"Request to {url} failed with status: {response.status}")
    except aiohttp.ClientError as e:
        print(f"Error sending request to {url}: {e}")

async def start_requests(url, request_count):
    start_time = time.time()

    # Create a list of tasks (coroutines) to send requests concurrently
    tasks = [send_request(url) for _ in range(request_count)]
    
    # Run all tasks concurrently
    await asyncio.gather(*tasks)
    
    end_time = time.time()
    print(f"Finished! Total requests sent: {request_count}")
    print(f"Time taken: {end_time - start_time} seconds")

if __name__ == "__main__":
    url = input("Enter URL: ")
    request_count = 2000000  # Number of requests you want to send (2M)

    if not url:
        print("Please provide a valid URL.")
    else:
        print(f"Starting {request_count} requests...")
        asyncio.run(start_requests(url, request_count))