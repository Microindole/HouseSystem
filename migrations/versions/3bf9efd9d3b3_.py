"""empty message

Revision ID: 3bf9efd9d3b3
Revises: 3df32edfa07b
Create Date: 2025-05-31 15:15:37.601029

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3bf9efd9d3b3'
down_revision = '3df32edfa07b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('appointment', schema=None) as batch_op:
        batch_op.drop_constraint('appointment_ibfk_3', type_='foreignkey')
        batch_op.drop_constraint('appointment_ibfk_1', type_='foreignkey')
        batch_op.drop_constraint('appointment_ibfk_2', type_='foreignkey')
        batch_op.create_foreign_key(None, 'landlord', ['landlord_name'], ['landlord_name'], ondelete='CASCADE')
        batch_op.create_foreign_key(None, 'house_info', ['house_id'], ['house_id'], ondelete='CASCADE')
        batch_op.create_foreign_key(None, 'tenant', ['tenant_name'], ['tenant_name'], ondelete='CASCADE')

    with op.batch_alter_table('comment', schema=None) as batch_op:
        batch_op.drop_constraint('comment_ibfk_1', type_='foreignkey')
        batch_op.create_foreign_key(None, 'house_info', ['house_id'], ['house_id'], ondelete='CASCADE')

    with op.batch_alter_table('complaint', schema=None) as batch_op:
        batch_op.drop_constraint('complaint_ibfk_1', type_='foreignkey')
        batch_op.create_foreign_key(None, 'login', ['handler_username'], ['username'])

    with op.batch_alter_table('house_listing_audit', schema=None) as batch_op:
        batch_op.drop_constraint('house_listing_audit_ibfk_2', type_='foreignkey')
        batch_op.drop_constraint('house_listing_audit_ibfk_1', type_='foreignkey')
        batch_op.create_foreign_key(None, 'landlord', ['landlord_name'], ['landlord_name'])
        batch_op.create_foreign_key(None, 'house_status', ['house_id', 'landlord_name'], ['house_id', 'landlord_name'], ondelete='CASCADE')

    with op.batch_alter_table('message', schema=None) as batch_op:
        batch_op.drop_constraint('message_ibfk_2', type_='foreignkey')
        batch_op.drop_constraint('message_ibfk_1', type_='foreignkey')
        batch_op.drop_constraint('message_ibfk_3', type_='foreignkey')
        batch_op.create_foreign_key(None, 'login', ['receiver_username'], ['username'])
        batch_op.create_foreign_key(None, 'private_channel', ['channel_id'], ['channel_id'], ondelete='CASCADE')
        batch_op.create_foreign_key(None, 'login', ['sender_username'], ['username'])

    with op.batch_alter_table('news', schema=None) as batch_op:
        batch_op.drop_constraint('news_ibfk_2', type_='foreignkey')
        batch_op.create_foreign_key(None, 'login', ['landlord_username'], ['username'])

    with op.batch_alter_table('private_channel', schema=None) as batch_op:
        batch_op.drop_constraint('private_channel_ibfk_3', type_='foreignkey')
        batch_op.drop_constraint('private_channel_ibfk_2', type_='foreignkey')
        batch_op.drop_constraint('private_channel_ibfk_1', type_='foreignkey')
        batch_op.create_foreign_key(None, 'login', ['tenant_username'], ['username'])
        batch_op.create_foreign_key(None, 'login', ['landlord_username'], ['username'])
        batch_op.create_foreign_key(None, 'house_info', ['house_id'], ['house_id'], ondelete='CASCADE')

    with op.batch_alter_table('rental_contract', schema=None) as batch_op:
        batch_op.drop_constraint('rental_contract_ibfk_1', type_='foreignkey')
        batch_op.create_foreign_key(None, 'private_channel', ['channel_id'], ['channel_id'], ondelete='CASCADE')

    with op.batch_alter_table('repair_request', schema=None) as batch_op:
        batch_op.drop_constraint('repair_request_ibfk_2', type_='foreignkey')
        batch_op.drop_constraint('repair_request_ibfk_1', type_='foreignkey')
        batch_op.drop_constraint('repair_request_ibfk_3', type_='foreignkey')
        batch_op.create_foreign_key(None, 'login', ['landlord_username'], ['username'], ondelete='CASCADE')
        batch_op.create_foreign_key(None, 'house_info', ['house_id'], ['house_id'], ondelete='CASCADE')
        batch_op.create_foreign_key(None, 'login', ['tenant_username'], ['username'], ondelete='CASCADE')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('repair_request', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_foreign_key('repair_request_ibfk_3', 'login', ['tenant_username'], ['username'], onupdate='RESTRICT', ondelete='CASCADE')
        batch_op.create_foreign_key('repair_request_ibfk_1', 'house_info', ['house_id'], ['house_id'], onupdate='RESTRICT', ondelete='CASCADE')
        batch_op.create_foreign_key('repair_request_ibfk_2', 'login', ['landlord_username'], ['username'], onupdate='RESTRICT', ondelete='CASCADE')

    with op.batch_alter_table('rental_contract', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_foreign_key('rental_contract_ibfk_1', 'private_channel', ['channel_id'], ['channel_id'], onupdate='RESTRICT', ondelete='CASCADE')

    with op.batch_alter_table('private_channel', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_foreign_key('private_channel_ibfk_1', 'login', ['landlord_username'], ['username'], onupdate='RESTRICT', ondelete='RESTRICT')
        batch_op.create_foreign_key('private_channel_ibfk_2', 'login', ['tenant_username'], ['username'], onupdate='RESTRICT', ondelete='RESTRICT')
        batch_op.create_foreign_key('private_channel_ibfk_3', 'house_info', ['house_id'], ['house_id'], onupdate='RESTRICT', ondelete='CASCADE')

    with op.batch_alter_table('news', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_foreign_key('news_ibfk_2', 'login', ['landlord_username'], ['username'], onupdate='RESTRICT', ondelete='CASCADE')

    with op.batch_alter_table('message', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_foreign_key('message_ibfk_3', 'private_channel', ['channel_id'], ['channel_id'], onupdate='RESTRICT', ondelete='CASCADE')
        batch_op.create_foreign_key('message_ibfk_1', 'login', ['receiver_username'], ['username'], onupdate='RESTRICT', ondelete='RESTRICT')
        batch_op.create_foreign_key('message_ibfk_2', 'login', ['sender_username'], ['username'], onupdate='RESTRICT', ondelete='RESTRICT')

    with op.batch_alter_table('house_listing_audit', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_foreign_key('house_listing_audit_ibfk_1', 'landlord', ['landlord_name'], ['landlord_name'], onupdate='RESTRICT', ondelete='RESTRICT')
        batch_op.create_foreign_key('house_listing_audit_ibfk_2', 'house_status', ['house_id', 'landlord_name'], ['house_id', 'landlord_name'], onupdate='RESTRICT', ondelete='CASCADE')

    with op.batch_alter_table('complaint', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_foreign_key('complaint_ibfk_1', 'login', ['handler_username'], ['username'], onupdate='RESTRICT', ondelete='RESTRICT')

    with op.batch_alter_table('comment', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_foreign_key('comment_ibfk_1', 'house_info', ['house_id'], ['house_id'], onupdate='RESTRICT', ondelete='CASCADE')

    with op.batch_alter_table('appointment', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_foreign_key('appointment_ibfk_2', 'tenant', ['tenant_name'], ['tenant_name'], onupdate='RESTRICT', ondelete='CASCADE')
        batch_op.create_foreign_key('appointment_ibfk_1', 'landlord', ['landlord_name'], ['landlord_name'], onupdate='RESTRICT', ondelete='CASCADE')
        batch_op.create_foreign_key('appointment_ibfk_3', 'house_info', ['house_id'], ['house_id'], onupdate='RESTRICT', ondelete='CASCADE')

    # ### end Alembic commands ###
