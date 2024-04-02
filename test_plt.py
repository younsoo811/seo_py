import psutil
import matplotlib.pyplot as plt
import time

# CPU 사용량 모니터링
def monitor_cpu(interval):
    cpu_percentages = []
    timestamps = []

    while True:
        cpu_percent = psutil.cpu_percent()
        timestamp = time.time()

        cpu_percentages.append(cpu_percent*10)
        timestamps.append(timestamp)

        print(cpu_percent*10)
        plt.plot(timestamps, cpu_percentages)
        plt.xlabel("Time")
        plt.ylabel("CPU Usage (%)")
        plt.title("CPU Usage Monitor")
        plt.grid(True)
        plt.pause(interval)

# 메모리 사용량 모니터링
def monitor_memory(interval):
    memory_percentages = []
    timestamps = []

    while True:
        memory = psutil.virtual_memory()
        used_memory = memory.used / (1024 * 1024) # 메모리 사용량을 MB 단위로 변환
        available_memory = memory.available / (1024 * 1024) # 사용 가능한 메모리 양을 MB 단위로 변환
        timestamp = time.time()

        memory_percentages.append(used_memory)
        timestamps.append(timestamp)

        plt.plot(timestamps, memory_percentages)
        plt.xlabel("Time")
        plt.ylabel("Memory Usage (MB)")
        plt.title("Memory Usage Monitor")
        plt.grid(True)
        plt.pause(interval)

# 디스크 사용량 모니터링
def monitor_disk(interval):
    disk_percentages = []
    timestamps = []

    while True:
        usage = psutil.disk_usage('/')
        used_disk = usage.used / (1024 * 1024 * 1024) # 디스크 사용량을 GB 단위로 변환
        timestamp = time.time()

        disk_percentages.append(used_disk)
        timestamps.append(timestamp)

        plt.plot(timestamps, disk_percentages)
        plt.xlabel("Time")
        plt.ylabel("Disk Usage (GB)")
        plt.title("Disk Usage Monitor")
        plt.grid(True)
        plt.pause(interval)

# 네트워크 사용량 모니터링
def monitor_network(interval):
    sent_data = []
    recv_data = []
    timestamps = []

    while True:
        network = psutil.net_io_counters()
        sent_bytes = network.bytes_sent / (1024 * 1024) # 송신 데이터 양을 MB 단위로 변환
        recv_bytes = network.bytes_recv / (1024 * 1024) # 수신 데이터 양을 MB 단위로 변환
        timestamp = time.time()

        sent_data.append(sent_bytes)
        recv_data.append(recv_bytes)
        timestamps.append(timestamp)

        plt.plot(timestamps, sent_data, label="Sent")
        plt.plot(timestamps, recv_data, label="Received")
        plt.xlabel("Time")
        plt.ylabel("Network Usage (MB)")
        plt.title("Network Usage Monitor")
        plt.legend()
        plt.grid(True)
        plt.pause(interval)

# 사용 예시
if __name__ == "__main__":
    interval = 1 # 업데이트 간격 (초 단위)

    monitor_cpu(interval)
    # monitor_memory(interval)
    # monitor_disk(interval)
    # monitor_network(interval)