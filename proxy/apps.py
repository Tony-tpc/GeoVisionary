from django.apps import AppConfig
import subprocess
import time
import threading

class ProxyConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "proxy"

    def ready(self):
        print("服务器启动中，自动拉起 TTS 后台服务...")
        cosyvoice_thread = threading.Thread(target=self.start_tts_server)
        cosyvoice_thread.daemon = True
        cosyvoice_thread.start()

    def start_tts_server(self):
        time.sleep(3)  # 等待服务初始化
        try:
            # 用 conda 运行 cosyvoice 虚拟环境
            # command = r'conda run -n cosyvoice python "C:\Study\Codes\CosyVoice\CosyVoice\cosyvoice_socket_server.py"'
            # subprocess.Popen(command, shell=True)
            print("CosyVoice Socket 服务器已拉起！")
        except Exception as e:
            print(f"CosyVoice 启动失败: {e}")