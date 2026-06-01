import os
import time
import tarfile
import yaml
from cryptography.fernet import Fernet
import requests

def load_config(config_path="config.yaml"):
    with open(config_path, 'r', encoding='utf-8') as file:
        return yaml.safe_load(file)

def compress_folder(source_dir, output_filename):
    print(f"📦 正在压缩文件夹: {source_dir}")
    with tarfile.open(output_filename, "w:gz") as tar:
        tar.add(source_dir, arcname=os.path.basename(source_dir))
    return output_filename

def encrypt_file(file_path, key):
    print(f"🔒 正在加密文件: {file_path}")
    fernet = Fernet(key)
    with open(file_path, 'rb') as file:
        original = file.read()
    encrypted = fernet.encrypt(original)
    
    enc_file_path = f"{file_path}.enc"
    with open(enc_file_path, 'wb') as encrypted_file:
        encrypted_file.write(encrypted)
    os.remove(file_path) # 删除未加密的原始压缩包
    return enc_file_path

def send_notification(api_key, message):
    print(f"📢 发送通知: {message}")
    # 这里的 URL 可以替换为 Server酱、PushDeer 或 Telegram Bot 的真实 API
    # 模拟发送请求: requests.post(f"https://api.example.com/notify?key={api_key}", data={"msg": message})
    pass

def main():
    config = load_config()
    source_dir = config['source_dir']
    backup_dir = config['backup_dir']
    api_key = config['notifications']['api_key']
    
    # 1. 准备环境
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)
        
    # 生成备份文件名 (带时间戳)
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    archive_name = os.path.join(backup_dir, f"backup_{timestamp}.tar.gz")
    
    try:
        # 2. 压缩
        compress_folder(source_dir, archive_name)
        
        # 3. 加密 (需要 32-byte 的 base64 编码密钥)
        # 可以通过 python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())" 生成
        enc_key = config['crypto']['secret_key'].encode()
        final_file = encrypt_file(archive_name, enc_key)
        
        # 4. 通知
        send_notification(api_key, f"✅ 备份成功！文件已保存为: {final_file}")
        print("🚀 备份全流程执行完毕！")
        
    except Exception as e:
        error_msg = f"❌ 备份失败: {str(e)}"
        print(error_msg)
        send_notification(api_key, error_msg)

if __name__ == "__main__":
    main()