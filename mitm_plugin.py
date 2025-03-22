from mitmproxy import http
import json
import os

# 定义标志文件路径
FLAG_FILE = "capture_done.flag"  # 用于通知外部程序停止抓包

def response(flow: http.HTTPFlow):
    if "api.fangao.100eks.com/member.miniprogram.auth" in flow.request.url:
        if "application/json" in flow.response.headers.get("content-type", ""):
            try:
                # 解析和修改数据（保持原有逻辑）
                response_data = flow.response.json()
                if "data" in response_data:
                    data = response_data["data"]
                    
                    # 篡改嵌套字段
                    if "last_login_student" in data:
                        data["last_login_student"]["username"] = data["last_login_student"]["username"] + "(已篡改)"
                    
                    # 保存关键数据
                    with open("user.json", "w") as f:
                        json.dump({
                            "mid": data.get("mid"),
                            "token": data.get("token"),
                            "openid": data.get("openid")
                        }, f, indent=4)
                    
                    # 创建停止抓包标志文件
                    with open(FLAG_FILE, "w") as f:
                        f.write("done")
                        print("[+] 抓包完成标志已创建")

                flow.response.text = json.dumps(response_data)
                
            except Exception as e:
                print(f"[-] 错误: {str(e)}")