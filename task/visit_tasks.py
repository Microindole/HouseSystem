from datetime import datetime, timedelta
from redis import Redis
from models import VisitStatsModel
from exts import db

r = Redis(host='localhost', port=6379, db=0)

def store_daily_visit_stats():
    yesterday = datetime.now() - timedelta(days=1)
    key = 'visits:' + yesterday.strftime('%Y%m%d')  # ✅ 统一 key

    count = r.scard(key)
    print(f"[store_daily_visit_stats] 从 Redis 读取 {key}，独立访问量：{count}")

    stat = VisitStatsModel(
        visit_date=(yesterday + timedelta(hours=8)).date(),  # ✅ 加8小时变北京时间
        unique_visits=count
    )
    db.session.add(stat)
    db.session.commit()

    r.delete(key)