from exts import db
from datetime import datetime
from sqlalchemy import UniqueConstraint # 新增导入 UniqueConstraint

class CommentModel(db.Model):
    __tablename__ = 'comment'
    comment_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    house_id = db.Column(db.Integer, nullable=False, comment='房屋的id')
    username = db.Column(db.String(255), nullable=False, comment='留言人名字')
    type = db.Column(db.Integer, nullable=False, comment='留言人类型,1:租客，2:房东')
    desc = db.Column(db.String(255), nullable=False, comment='留言内容')
    at = db.Column(db.Integer, nullable=True, comment='@哪条留言，前端显示为@谁，选填')
    time = db.Column(db.DateTime, nullable=False, comment='留言时间')


class HouseInfoModel(db.Model):
    __tablename__ = 'house_info'
    house_id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment='房屋id，自增的，不用填')
    house_name = db.Column(db.String(255), nullable=False, comment='房屋名称')
    rooms = db.Column(db.String(100), nullable=False, comment='房屋户型，如3室1厅')
    region = db.Column(db.String(100), nullable=False, comment='房屋地区，如北京市海淀区')
    addr = db.Column(db.String(255), nullable=False, comment='具体地址')
    price = db.Column(db.Numeric(10, 2), nullable=False, comment='房屋价格')
    deposit = db.Column(db.Numeric(10, 2), nullable=True, comment='押金')
    situation = db.Column(db.String(255), nullable=True, comment='房屋装修情况')
    highlight = db.Column(db.String(255), nullable=True, comment='亮点（没有可以不填）')
    image = db.Column(db.String(255), nullable=True, comment='房屋图片')


class HouseStatusModel(db.Model):
    __tablename__ = 'house_status'
    house_id = db.Column(db.Integer, db.ForeignKey('house_info.house_id', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True, comment='有一个外键指向house_info表')
    landlord_name = db.Column(db.String(100), primary_key=True)
    status = db.Column(db.Integer, nullable=False, comment='0为空置，1为出租中，2为装修中')
    phone = db.Column(db.String(255), nullable=False, comment='房屋联系方式')
    update_time = db.Column(db.DateTime, nullable=False, comment='房屋发布时间（之后状态有变化都更新一次时间）')


class LandlordModel(db.Model):
    __tablename__ = 'landlord'
    landlord_name = db.Column(db.String(100), primary_key=True, comment='房东用户名')
    phone = db.Column(db.String(255), nullable=False, comment='联系电话，与house_status中的phone一致')
    addr = db.Column(db.String(255), nullable=False, comment='房东住址')


class LoginModel(db.Model):
    __tablename__ = 'login'
    username = db.Column(db.String(100), primary_key=True)
    password = db.Column(db.String(100), nullable=False)
    type = db.Column(db.Integer, nullable=False, comment='0为管理员，1为租客，2为房东')


class PrivateChannelModel(db.Model):
    __tablename__ = 'private_channel'
    channel_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tenant_username = db.Column(db.String(100), db.ForeignKey('login.username'), nullable=False, comment='租客用户名')
    landlord_username = db.Column(db.String(100), db.ForeignKey('login.username'), nullable=False, comment='房东用户名')
    house_id = db.Column(db.Integer, db.ForeignKey('house_info.house_id'), nullable=False, comment='关联的房屋ID')
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, comment='频道创建时间')
    # 添加唯一约束，确保同一租客、房东、房屋只有一个频道
    __table_args__ = (UniqueConstraint('tenant_username', 'landlord_username', 'house_id', name='uq_tenant_landlord_house'),)


class MessageModel(db.Model):
    __tablename__ = 'message'
    message_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    channel_id = db.Column(db.Integer, db.ForeignKey('private_channel.channel_id', ondelete='CASCADE'), nullable=False, comment='所属私信频道的ID')
    sender_username = db.Column(db.String(100), db.ForeignKey('login.username'), nullable=False, comment='发送者用户名')
    receiver_username = db.Column(db.String(100), db.ForeignKey('login.username'), nullable=False, comment='接收者用户名')
    content = db.Column(db.Text, nullable=False, comment='消息内容')
    timestamp = db.Column(db.DateTime, nullable=False, comment='发送时间')
    is_read = db.Column(db.Boolean, nullable=False, default=False, comment='是否已读 (接收者视角)')


class NewsModel(db.Model):
    __tablename__ = 'news'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    time = db.Column(db.DateTime, nullable=False, comment='新闻发布时间，注意新闻只能新增，(尽量)不能修改')
    house_id = db.Column(db.Integer, db.ForeignKey('house_info.house_id', ondelete='RESTRICT', onupdate='RESTRICT'), nullable=False, comment='房屋id，有一个指向house_info的外键')
    title = db.Column(db.String(255), nullable=False, comment='新闻标题（如某某房屋出租了）,一般配对房屋状态变化')
    desc = db.Column(db.String(255), nullable=True, comment='新闻内容')


class OrderModel(db.Model):
    __tablename__ = 'order'
    order_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tenant_name = db.Column(db.String(100), nullable=False, comment='写在用户租赁历史中，用户可对租赁状态进行修改，注意：只能归还')
    house_id = db.Column(db.Integer, nullable=False)
    time = db.Column(db.String(100), nullable=False, comment='租赁时间，按月算，需要前端或者后端计算时间(是否超出日期)')
    status = db.Column(db.Integer, nullable=False, comment='与house_status中的status对应,这里0:归还,1:租赁中\r\n注意：这里修改要影响house_status，那里修改不会影响这里')


class TenantModel(db.Model):
    __tablename__ = 'tenant'
    tenant_name = db.Column(db.String(100), primary_key=True, comment='租客用户名')
    phone = db.Column(db.String(100), nullable=False, comment='联系方式')
    addr = db.Column(db.String(255), nullable=False, comment='用户住址')

    
class AppointmentModel(db.Model):
    __tablename__ = 'appointment'
    appointment_id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment='预约ID')
    house_id = db.Column(db.Integer, db.ForeignKey('house_info.house_id', ondelete='CASCADE'), nullable=False, comment='房屋ID')
    house_name = db.Column(db.String(255), nullable=False, comment='房屋名称')
    tenant_name = db.Column(db.String(100), db.ForeignKey('tenant.tenant_name', ondelete='CASCADE'), nullable=False, comment='租客用户名')
    landlord_name = db.Column(db.String(100), db.ForeignKey('landlord.landlord_name', ondelete='CASCADE'), nullable=False, comment='房东用户名')
    appointment_time = db.Column(db.DateTime, nullable=False, comment='预约时间')
    status = db.Column(db.String(20), nullable=False, default='申请中', comment='预约状态（申请中/已同意/已拒绝）')


class ComplaintModel(db.Model):
    __tablename__ = 'complaint'
    complaint_id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment='投诉/消息ID')
    sender = db.Column(db.String(100), nullable=False, comment='发送人用户名（租客/房东/管理员）')
    receiver = db.Column(db.String(100), nullable=True, comment='接收人用户名（为空表示所有管理员可见）')
    content = db.Column(db.Text, nullable=False, comment='消息/投诉内容')
    time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, comment='发送时间')
    type = db.Column(db.String(20), nullable=False, default='投诉', comment='类型：投诉/反馈')
    status = db.Column(db.String(20), nullable=False, default='待处理', comment='处理状态：待处理/处理中/已解决/已关闭')
    handler_username = db.Column(db.String(100), db.ForeignKey('login.username'), nullable=True, comment='处理人用户名')
    last_updated_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow, comment='最后更新时间')
    update_seen_by_sender = db.Column(db.Boolean, nullable=False, default=False, comment='发送者是否已查看最新状态更新') # 新增字段

    # 可选：与处理记录表建立关系
    # handling_records = db.relationship('ComplaintHandlingRecordModel', backref='complaint', lazy=True)

# 可选：处理记录模型
# class ComplaintHandlingRecordModel(db.Model):
#     __tablename__ = 'complaint_handling_record'
#     record_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     complaint_id = db.Column(db.Integer, db.ForeignKey('complaint.complaint_id'), nullable=False)
#     handler_username = db.Column(db.String(100), db.ForeignKey('login.username'), nullable=False)
#     action_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
#     action_description = db.Column(db.Text, nullable=False, comment='处理动作描述，如：已联系用户，正在调查')
#     new_status = db.Column(db.String(20), nullable=False, comment='处理后的状态')

class EmailUsernameMapModel(db.Model):
    __tablename__ = 'user_email'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(255), nullable=False, index=True, comment='用户邮箱')
    username = db.Column(db.String(100), db.ForeignKey('login.username', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, comment='关联的用户名')

    # 添加唯一约束，确保同一个邮箱和用户名的组合是唯一的
    __table_args__ = (db.UniqueConstraint('email', 'username', name='uq_email_username_map'),)