import csv
from datetime import datetime
import time
import os

def get_cpu_usage():
    # CPU情報を読み取る
    with open('/proc/stat', 'r') as f:
        lines = f.readlines()
    cpu_times = list(map(int, lines[0].split()[1:]))
    idle_time = cpu_times[3]
    total_time = sum(cpu_times)
    return idle_time, total_time

def get_memory_usage():
    with open('/proc/meminfo', 'r') as f:
        lines = f.readlines()
    mem_info = {line.split(':')[0]: line.split(':')[1].strip() for line in lines}
    total_memory = int(mem_info['MemTotal'].split()[0])
    free_memory = int(mem_info['MemFree'].split()[0])
    used_memory = total_memory - free_memory
    used_memory_mb = used_memory / 1024
    return used_memory_mb

def log_data():
    # ファイルが新規の場合はヘッダーを追加
    file_exists = os.path.isfile("./data.csv") and os.path.getsize("./data.csv") > 0
    headers = ['Date', 'CPU Temperature', 'Memory Usage', 'CPU Usage (%)']
    
    # 現在の日付と時間を取得
    now = datetime.now()
    formatted_date = now.strftime('%Y-%m-%d %H:%M:%S')

    # CPU温度を読み取る
    with open('/sys/class/thermal/thermal_zone0/temp') as f:
        cpu_temp = f.read().strip()

    # メモリ使用量を取得
    memory_usage = get_memory_usage()

    # CPU使用率を取得
    idle_time_prev, total_time_prev = get_cpu_usage()
    time.sleep(1)  # 1秒待機
    idle_time_next, total_time_next = get_cpu_usage()
    cpu_usage = (1 - ((idle_time_next - idle_time_prev) / (total_time_next - total_time_prev))) * 100

    # データをCSVファイルに追加
    with open("./data.csv", "a", newline='') as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(headers)  # 初回のみヘッダーを書き込む
        writer.writerow([formatted_date, cpu_temp, memory_usage, cpu_usage])

# 無限ループで3秒ごとにデータを記録
while True:
    log_data()
    time.sleep(3)