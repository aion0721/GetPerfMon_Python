import csv
from datetime import datetime
import time
import os
import argparse

def get_cpu_usage():
    """
    CPU使用率を計算します。
    /proc/statからCPU時間を読み取り、アイドル時間と総CPU時間を基に使用率を計算します。
    """
    with open('/proc/stat', 'r') as f:
        lines = f.readlines()
    cpu_times = list(map(int, lines[0].split()[1:]))
    idle_time = cpu_times[3]
    total_time = sum(cpu_times)
    return idle_time, total_time

def get_memory_usage():
    """
    使用中のメモリ量をMB単位で計算します。
    /proc/meminfoからメモリ情報を読み取り、使用中のメモリ量を計算します。
    """
    with open('/proc/meminfo', 'r') as f:
        lines = f.readlines()
    mem_info = {line.split(':')[0]: line.split(':')[1].strip() for line in lines}
    total_memory = int(mem_info['MemTotal'].split()[0])
    free_memory = int(mem_info['MemFree'].split()[0])
    used_memory = total_memory - free_memory
    used_memory_mb = used_memory / 1024
    return used_memory_mb

def log_data(output_file, sleep_time):
    """
    日付、CPU温度、メモリ使用量、CPU使用率をCSVファイルに記録します。
    出力ファイルが存在しない場合は、ヘッダーを先に書き込みます。
    """
    # ファイルが既に存在するかチェック
    file_exists = os.path.isfile(output_file) and os.path.getsize(output_file) > 0
    headers = ['Date', 'CPU Temperature', 'Memory Usage', 'CPU Usage (%)']
    
    # 現在の日付と時間を取得
    now = datetime.now()
    formatted_date = now.strftime('%Y-%m-%d %H:%M:%S')

    # CPU温度を読み取る
    with open('/sys/class/thermal/thermal_zone0/temp') as f:
        cpu_temp = f.read().strip()

    # メモリ使用量を取得
    memory_usage = get_memory_usage()

    # CPU使用率を計算
    idle_time_prev, total_time_prev = get_cpu_usage()
    time.sleep(1)  # 1秒間隔で再度CPU情報を取得するために待機
    idle_time_next, total_time_next = get_cpu_usage()
    cpu_usage = (1 - ((idle_time_next - idle_time_prev) / (total_time_next - total_time_prev))) * 100

    # データをCSVファイルに追加
    with open(output_file, "a", newline='') as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(headers)  # ヘッダーを先に書き込む
        writer.writerow([formatted_date, cpu_temp, memory_usage, cpu_usage])

if __name__ == "__main__":
    # argparseを使用してコマンドライン引数を処理
    parser = argparse.ArgumentParser(description="Log system stats to a CSV file.")
    parser.add_argument("--output", help="Output CSV file path", default="./data.csv")
    parser.add_argument("--sleep", help="Sleep time between logs in seconds", type=int, default=30)
    args = parser.parse_args()

    # 指定されたスリープ時間で無限ループ内でデータ記録関数を実行
    while True:
        log_data(args.output, args.sleep)
        time.sleep(args.sleep - 1)  # 次の記録まで指定された時間待機。ただし、CPU時間のときに1秒待ってるので1秒削る
