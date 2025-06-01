from exts import db
from datetime import datetime
from sqlalchemy import UniqueConstraint

"""
本模块定义了应用程序中使用的所有数据库模型 (SQLAlchemy Models)。
每个类代表数据库中的一张表，其实例代表表中的一条记录。

主要模型及其用途如下：

- CommentModel: 存储用户对房屋的评论或留言信息，包括评论人、内容、时间以及可能回复的某条其他评论。
- HouseInfoModel: 存储房屋的基本静态信息，如房屋名称、户型、所在地区、详细地址、价格、押金、装修情况、房屋亮点和相关图片。
- HouseStatusModel: 存储房屋的动态状态信息，如关联的房东、当前状态（例如空置、出租中、装修中）、对外联系电话以及状态的最后更新时间。
- LandlordModel: 存储房东用户的基本信息，包括房东用户名（主键）、联系电话和住址。
- LoginModel: 存储用户的登录认证信息，包括用户名（主键）、加密后的密码以及用户类型（如管理员、租客、房东）。
- PrivateChannelModel: 定义租客和房东之间针对特定房屋建立的私人沟通渠道，记录了参与方和关联房屋。
- MessageModel: 存储在上述私信频道中发送的具体消息内容，包括发送者、接收者、消息文本、时间戳及已读状态。
- NewsModel: 存储与房屋相关的动态或新闻资讯，通常关联到具体的房屋及其房东，记录了新闻的标题、描述和发布时间。
- TenantModel: 存储租客用户的基本信息，包括租客用户名（主键）、联系电话和住址。
- AppointmentModel: 记录租客就特定房源向房东发起的看房预约详情，包含预约时间、涉及的房源、租客、房东以及预约状态。
- ComplaintModel: 存储用户（租客、房东或管理员）提交的投诉或反馈信息，包括发送人、接收人（可选）、内容、类型、处理状态、处理人及时间戳。
- DailyRentRateModel: 用于按天记录和统计平台上房源的出租情况，包括总上架数、已出租数及计算得出的出租率。
- HouseListingAuditModel: 记录房东提交的房源上架申请的审核流程信息，包括关联房源、房东、审核状态、原因及时间戳。
- EmailUsernameMapModel: 建立用户邮箱地址与其系统用户名的映射关系，方便通过邮箱进行关联操作。
- RentalContract: 存储租赁合同的详细信息，关联到特定的私信频道，记录合同双方、起止日期、总金额、支付状态及创建更新时间。
- RepairRequestModel: 记录租客针对特定房屋提交的维修请求，包含请求描述、关联房源、租客、房东、请求时间、处理状态及房东备注等。
"""

class CommentModel(db.Model):
    __tablename__ = 'comment'
    comment_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    house_id = db.Column(db.Integer, db.ForeignKey('house_info.house_id', ondelete='CASCADE'), nullable=False, comment='房屋的id')
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
    landlord_name = db.Column(db.String(100), nullable=False)  # landlord_name 变为普通列
    status = db.Column(db.Integer, nullable=False, comment='0为空置，1为出租中，2为装修中')
    phone = db.Column(db.String(255), nullable=False, comment='房屋联系方式')
    update_time = db.Column(db.DateTime, nullable=False, comment='房屋发布时间（之后状态有变化都更新一次时间）')

    house_info = db.relationship('HouseInfoModel', backref='status')

    __table_args__ = (
        db.UniqueConstraint('house_id', 'landlord_name', name='uq_house_landlord'),  # 添加唯一约束
    )

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
    house_id = db.Column(db.Integer, db.ForeignKey('house_info.house_id', ondelete='CASCADE'), nullable=False, comment='关联的房屋ID')
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
    house_id = db.Column(db.Integer, db.ForeignKey('house_info.house_id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, comment='房屋id，有一个指向house_info的外键')
    title = db.Column(db.String(255), nullable=False, comment='新闻标题（如某某房屋出租了）,一般配对房屋状态变化')
    desc = db.Column(db.String(255), nullable=True, comment='新闻内容')
    landlord_username = db.Column(db.String(100), db.ForeignKey('login.username'), nullable=True, comment='新闻发布者(房东)')

    # Add relationship to HouseInfoModel
    house_info = db.relationship('HouseInfoModel', backref='news_items')

    def __repr__(self):
        return f'<NewsModel {self.id} {self.title}>'


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


class DailyRentRateModel(db.Model):
    __tablename__ = 'daily_rent_rate'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment='自增ID')
    date = db.Column(db.Date, nullable=False, unique=True, comment='统计日期')
    total_count = db.Column(db.Integer, nullable=False, default=0, comment='上架总数（状态为0）')
    rented_count = db.Column(db.Integer, nullable=False, default=0, comment='出租数（状态为1）')
    rent_rate = db.Column(db.Numeric(5, 2), nullable=False, comment='出租率百分比（如 66.67）')

    def __repr__(self):
        return f'<DailyRentRate {self.date} - {self.rent_rate}%>'


class HouseListingAuditModel(db.Model):
    __tablename__ = 'house_listing_audit'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment='审核记录ID')
    house_id = db.Column(db.Integer, nullable=False, comment='房源ID')  # 移除单列的外键引用
    house_name = db.Column(db.String(255), nullable=False, comment='房源名称')
    landlord_name = db.Column(db.String(100), db.ForeignKey('landlord.landlord_name'), nullable=False, comment='房东名字')
    audit_status = db.Column(db.Integer, nullable=False, default=0, comment='审核状态：0-审核中，1-已通过，2-已拒绝')
    reason = db.Column(db.String(255), comment='拒绝理由')
    create_time = db.Column(db.DateTime, server_default=db.func.now(), nullable=False, comment='申请时间')
    update_time = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now(), nullable=False, comment='回复时间')

    # 修改复合外键约束，添加 ondelete='CASCADE'
    __table_args__ = (
        db.ForeignKeyConstraint(
            ['house_id', 'landlord_name'],
            ['house_status.house_id', 'house_status.landlord_name'],
            ondelete='CASCADE'
        ),
    )

class EmailUsernameMapModel(db.Model):
    __tablename__ = 'user_email'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(255), nullable=False, index=True, comment='用户邮箱')
    username = db.Column(db.String(100), db.ForeignKey('login.username', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, comment='关联的用户名')

    # 添加唯一约束，确保同一个邮箱和用户名的组合是唯一的
    __table_args__ = (db.UniqueConstraint('email', 'username', name='uq_email_username_map'),)


class RentalContract(db.Model):
    __tablename__ = 'rental_contract'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    # 更新与聊天频道的关系，添加外键约束
    channel_id = db.Column(db.Integer, db.ForeignKey('private_channel.channel_id', ondelete='CASCADE'), nullable=False, comment='关联的私信频道ID')

    landlord_username = db.Column(db.String(100), nullable=False)
    tenant_username = db.Column(db.String(100), nullable=False)

    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)

    total_amount = db.Column(db.Numeric(10, 2), nullable=False)

    status = db.Column(db.Integer, nullable=False, default=0, comment='0：待支付，1：支付成功，2：取消订单,3：撤销订单')

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # 添加与 PrivateChannelModel 的关系
    channel = db.relationship('PrivateChannelModel', backref=db.backref('contracts', lazy=True))

    def __repr__(self):
        return f'<RentalContract {self.id} - {self.landlord_username} → {self.tenant_username}>'

class RepairRequestModel(db.Model):
    __tablename__ = 'repair_request'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    house_id = db.Column(db.Integer, db.ForeignKey('house_info.house_id', ondelete='CASCADE'), nullable=False, comment='关联房屋ID')
    tenant_username = db.Column(db.String(100), db.ForeignKey('login.username', ondelete='CASCADE'), nullable=False, comment='租客用户名')
    landlord_username = db.Column(db.String(100), db.ForeignKey('login.username', ondelete='CASCADE'), nullable=False, comment='房东用户名')
    content = db.Column(db.Text, nullable=False, comment='维修内容描述')
    request_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, comment='请求发起时间')
    # 状态：请求中 (default), 已同意, 处理中, 已完成, 已拒绝
    status = db.Column(db.String(50), nullable=False, default='请求中', comment='维修请求状态')
    handler_notes = db.Column(db.Text, nullable=True, comment='房东处理备注')
    handled_time = db.Column(db.DateTime, nullable=True, comment='房东处理时间')

    # 关系定义 (backref 名称可以根据您的喜好调整，确保不与现有冲突)
    house = db.relationship('HouseInfoModel', backref=db.backref('repair_requests_info', lazy='dynamic'))
    tenant = db.relationship('LoginModel', foreign_keys=[tenant_username], backref=db.backref('sent_repair_requests_info', lazy='dynamic'))
    landlord = db.relationship('LoginModel', foreign_keys=[landlord_username], backref=db.backref('received_repair_requests_info', lazy='dynamic'))

    def __repr__(self):
        return f'<RepairRequestModel {self.id} by {self.tenant_username} for house {self.house_id}>'

class VisitStatsModel(db.Model):
        __tablename__ = 'visit_stats'

        id = db.Column(db.Integer, primary_key=True)
        visit_date = db.Column(db.Date, nullable=False)
        unique_visits = db.Column(db.Integer, default=0)
        created_at = db.Column(db.DateTime, default=datetime.utcnow)

