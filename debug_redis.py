from redis import Redis
from datetime import datetime, timedelta

r = Redis(host='localhost', port=6379, db=0)

today = datetime.now().strftime('%Y%m%d')
key = f'visits:{today}'   # 👈 注意这里改为 'visits:20250531'

print(f"[Key] {key}")
ip_list = r.smembers(key)
print("IP 列表：", ip_list)
print("唯一 IP 数量：", len(ip_list))