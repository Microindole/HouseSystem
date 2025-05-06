from exts import db
from models import CommentModel, HouseStatusModel
from datetime import datetime, timedelta
from flask import Flask

app = Flask(__name__)
app.config.from_object('config')  # 根据你的配置文件路径调整

db.init_app(app)

with app.app_context():
    house_status_list = HouseStatusModel.query.all()
    comments = []
    NUM_COMMENTS_PER_HOUSE = 10  # 每个房源生成10条留言

    for hs in house_status_list:
        for i in range(NUM_COMMENTS_PER_HOUSE):
            comments.append(CommentModel(
                house_id=hs.house_id,
                username=f'租客{i+1}',
                type=1,
                desc=f'这是第{i+1}条留言，房东{hs.landlord_name}你好！',
                at=None,
                time=datetime.now() - timedelta(days=i)
            ))
    db.session.add_all(comments)
    db.session.commit()
    print("每个房源已添加多条留言")