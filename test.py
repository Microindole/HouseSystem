from models import db, HouseInfoModel, HouseStatusModel, LandlordModel, RentalContract
from datetime import datetime
from app import app  # 确保 app 是你的 Flask 实例

with app.app_context():
    # 1. 修正 house_status.status 字段不规范（如 4 改为 0/1/2）
    for hs in HouseStatusModel.query.all():
        if hs.status not in (0, 1, 2):
            hs.status = 0  # 默认改为空置
            hs.update_time = datetime.now()
    db.session.commit()

    # 2. 检查 house_status 的 landlord_name 是否都在 landlord 表
    landlord_names = {l.landlord_name for l in LandlordModel.query.all()}
    for hs in HouseStatusModel.query.all():
        if hs.landlord_name not in landlord_names:
            # 修正为已存在的 landlord
            hs.landlord_name = 'landlord'  # 假设有 landlord 这个用户
    db.session.commit()

    # 3. 修正 rental_contract.status 字段不规范（只允许0,1,2）
    for contract in RentalContract.query.all():
        if contract.status not in (0, 1, 2):
            contract.status = 2  # 默认改为已取消
    db.session.commit()

    # 4. 新增房源（house_info 和 house_status），满足唯一约束
    # 选择 landlord3 作为房东，图片用 static/images/t2.jpg
    new_house = HouseInfoModel(
        house_name='朝阳区精装一居室',
        rooms='1室1厅',
        region='北京市朝阳区',
        addr='朝阳公园南路',
        price=8500.00,
        deposit=17000.00,
        situation='精装修',
        highlight='公园旁，生活便利',
        image='static/images/t2.jpg'
    )
    db.session.add(new_house)
    db.session.commit()  # 提交后才能拿到 house_id

    new_status = HouseStatusModel(
        house_id=new_house.house_id,
        landlord_name='landlord',
        status=0,  # 空置
        phone='13800138004',
        update_time=datetime.now()
    )
    db.session.add(new_status)
    db.session.commit()

    print(f"已修正所有不规范数据并新增房源 house_id={new_house.house_id}")