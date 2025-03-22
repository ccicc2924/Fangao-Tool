import pygetwindow as gw
import time
import subprocess
import os

# 配置参数
MITM_CMD = "mitmdump -q -s mitm_plugin.py"  # 静默模式运行
FLAG_FILE = "capture_done.flag"  # 与插件中的标志文件一致

def manage_proxy():
    mitm_process = None
    
    try:
        # 启动 mitmproxy
        mitm_process = subprocess.Popen(
            MITM_CMD.split(),
            stdout=subprocess.DEVNULL,  # 丢弃输出
            stderr=subprocess.DEVNULL
        )
        print("[*] mitmproxy 已启动 (PID: %d)" % mitm_process.pid)
        
        # 等待抓包完成标志
        while True:
            if os.path.exists(FLAG_FILE):
                print("[+] 检测到抓包完成标志")
                os.remove(FLAG_FILE)  # 清理标志
                break
            time.sleep(1)
            
    finally:
        # 终止 mitmproxy
        if mitm_process and mitm_process.poll() is None:
            mitm_process.terminate()
            print("[*] mitmproxy 已终止")

def check_window():
    while True:
        windows = gw.getWindowsWithTitle('凡高云校园')
        if windows:
            print("[*] 检测到目标窗口，关闭中...")
            windows[0].close()
            manage_proxy()  # 启动代理管理流程
            break
        else:
            print("[*] 等待目标窗口出现...")
            time.sleep(2)

if __name__ == "__main__":
    check_window()