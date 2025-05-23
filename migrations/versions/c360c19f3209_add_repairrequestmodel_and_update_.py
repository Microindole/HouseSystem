"""Add RepairRequestModel and update NewsModel for landlord features

Revision ID: c360c19f3209
Revises: 0b04b293096e
Create Date: 2025-05-18 15:13:21.505644

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c360c19f3209'
down_revision = '0b04b293096e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('repair_request',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('house_id', sa.Integer(), nullable=False, comment='关联房屋ID'),
    sa.Column('tenant_username', sa.String(length=100), nullable=False, comment='租客用户名'),
    sa.Column('landlord_username', sa.String(length=100), nullable=False, comment='房东用户名'),
    sa.Column('content', sa.Text(), nullable=False, comment='维修内容描述'),
    sa.Column('request_time', sa.DateTime(), nullable=False, comment='请求发起时间'),
    sa.Column('status', sa.String(length=50), nullable=False, comment='维修请求状态'),
    sa.Column('handler_notes', sa.Text(), nullable=True, comment='房东处理备注'),
    sa.Column('handled_time', sa.DateTime(), nullable=True, comment='房东处理时间'),
    sa.ForeignKeyConstraint(['house_id'], ['house_info.house_id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['landlord_username'], ['login.username'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['tenant_username'], ['login.username'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('appointment', schema=None) as batch_op:
        batch_op.drop_constraint('appointment_ibfk_3', type_='foreignkey')
        batch_op.drop_constraint('appointment_ibfk_2', type_='foreignkey')
        batch_op.drop_constraint('appointment_ibfk_1', type_='foreignkey')
        batch_op.create_foreign_key(None, 'landlord', ['landlord_name'], ['landlord_name'], ondelete='CASCADE')
        batch_op.create_foreign_key(None, 'tenant', ['tenant_name'], ['tenant_name'], ondelete='CASCADE')
        batch_op.create_foreign_key(None, 'house_info', ['house_id'], ['house_id'], ondelete='CASCADE')

    with op.batch_alter_table('complaint', schema=None) as batch_op:
        batch_op.drop_constraint('complaint_ibfk_1', type_='foreignkey')
        batch_op.create_foreign_key(None, 'login', ['handler_username'], ['username'])

    with op.batch_alter_table('house_listing_audit', schema=None) as batch_op:
        batch_op.drop_constraint('house_listing_audit_ibfk_2', type_='foreignkey')
        batch_op.drop_constraint('house_listing_audit_ibfk_1', type_='foreignkey')
        batch_op.create_foreign_key(None, 'landlord', ['landlord_name'], ['landlord_name'])
        batch_op.create_foreign_key(None, 'house_status', ['house_id', 'landlord_name'], ['house_id', 'landlord_name'])

    with op.batch_alter_table('message', schema=None) as batch_op:
        batch_op.drop_constraint('message_ibfk_2', type_='foreignkey')
        batch_op.drop_constraint('message_ibfk_3', type_='foreignkey')
        batch_op.drop_constraint('message_ibfk_1', type_='foreignkey')
        batch_op.create_foreign_key(None, 'login', ['receiver_username'], ['username'])
        batch_op.create_foreign_key(None, 'login', ['sender_username'], ['username'])
        batch_op.create_foreign_key(None, 'private_channel', ['channel_id'], ['channel_id'], ondelete='CASCADE')

    with op.batch_alter_table('news', schema=None) as batch_op:
        batch_op.add_column(sa.Column('landlord_username', sa.String(length=100), nullable=True, comment='新闻发布者(房东)'))
        batch_op.create_foreign_key(None, 'login', ['landlord_username'], ['username'])

    with op.batch_alter_table('private_channel', schema=None) as batch_op:
        batch_op.drop_constraint('private_channel_ibfk_1', type_='foreignkey')
        batch_op.drop_constraint('private_channel_ibfk_2', type_='foreignkey')
        batch_op.drop_constraint('private_channel_ibfk_3', type_='foreignkey')
        batch_op.create_foreign_key(None, 'login', ['landlord_username'], ['username'])
        batch_op.create_foreign_key(None, 'login', ['tenant_username'], ['username'])
        batch_op.create_foreign_key(None, 'house_info', ['house_id'], ['house_id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('private_channel', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_foreign_key('private_channel_ibfk_3', 'house_info', ['house_id'], ['house_id'], onupdate='RESTRICT', ondelete='RESTRICT')
        batch_op.create_foreign_key('private_channel_ibfk_2', 'login', ['tenant_username'], ['username'], onupdate='RESTRICT', ondelete='RESTRICT')
        batch_op.create_foreign_key('private_channel_ibfk_1', 'login', ['landlord_username'], ['username'], onupdate='RESTRICT', ondelete='RESTRICT')

    with op.batch_alter_table('news', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_column('landlord_username')

    with op.batch_alter_table('message', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_foreign_key('message_ibfk_1', 'private_channel', ['channel_id'], ['channel_id'], onupdate='RESTRICT', ondelete='CASCADE')
        batch_op.create_foreign_key('message_ibfk_3', 'login', ['sender_username'], ['username'], onupdate='RESTRICT', ondelete='RESTRICT')
        batch_op.create_foreign_key('message_ibfk_2', 'login', ['receiver_username'], ['username'], onupdate='RESTRICT', ondelete='RESTRICT')

    with op.batch_alter_table('house_listing_audit', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_foreign_key('house_listing_audit_ibfk_1', 'house_status', ['house_id', 'landlord_name'], ['house_id', 'landlord_name'], onupdate='RESTRICT', ondelete='RESTRICT')
        batch_op.create_foreign_key('house_listing_audit_ibfk_2', 'landlord', ['landlord_name'], ['landlord_name'], onupdate='RESTRICT', ondelete='RESTRICT')

    with op.batch_alter_table('complaint', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_foreign_key('complaint_ibfk_1', 'login', ['handler_username'], ['username'], onupdate='RESTRICT', ondelete='RESTRICT')

    with op.batch_alter_table('appointment', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_foreign_key('appointment_ibfk_1', 'tenant', ['tenant_name'], ['tenant_name'], onupdate='RESTRICT', ondelete='CASCADE')
        batch_op.create_foreign_key('appointment_ibfk_2', 'landlord', ['landlord_name'], ['landlord_name'], onupdate='RESTRICT', ondelete='CASCADE')
        batch_op.create_foreign_key('appointment_ibfk_3', 'house_info', ['house_id'], ['house_id'], onupdate='RESTRICT', ondelete='CASCADE')

    op.drop_table('repair_request')
    # ### end Alembic commands ###
