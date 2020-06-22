"""better invitations and resets

Revision ID: 6eb79ba67acb
Revises: 9b9fdebcdcb8
Create Date: 2020-06-17 12:09:13.015879

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6eb79ba67acb'
down_revision = '9b9fdebcdcb8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user_invitation',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(length=128), nullable=True),
    sa.Column('token', sa.String(length=32), nullable=False),
    sa.Column('creation_date', sa.DateTime(), nullable=True),
    sa.Column('expiration_date', sa.DateTime(), nullable=False),
    sa.Column('accepted_date', sa.DateTime(), nullable=True),
    sa.Column('is_expired', sa.Boolean(), nullable=True),
    sa.Column('is_admin', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('token')
    )
    with op.batch_alter_table('email_token', schema=None) as batch_op:
        batch_op.drop_index('ix_email_token_token_type')

    op.drop_table('email_token')
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('creation_date', sa.DateTime(), nullable=True))
        batch_op.add_column(sa.Column('is_active', sa.Boolean(), nullable=True))
        batch_op.add_column(sa.Column('password_reset_expiration', sa.DateTime(), nullable=True))
        batch_op.add_column(sa.Column('password_reset_token', sa.String(length=32), nullable=True))
        batch_op.create_unique_constraint("uq_pw_reset_token", ['password_reset_token'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='unique')
        batch_op.drop_column('password_reset_token')
        batch_op.drop_column('password_reset_expiration')
        batch_op.drop_column('is_active')
        batch_op.drop_column('creation_date')

    op.create_table('email_token',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('token', sa.VARCHAR(length=32), nullable=False),
    sa.Column('date_generated', sa.DATETIME(), nullable=False),
    sa.Column('user_id', sa.INTEGER(), nullable=False),
    sa.Column('token_type', sa.VARCHAR(length=8), nullable=False),
    sa.Column('token_expiration', sa.DATETIME(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('token')
    )
    with op.batch_alter_table('email_token', schema=None) as batch_op:
        batch_op.create_index('ix_email_token_token_type', ['token_type'], unique=False)

    op.drop_table('user_invitation')
    # ### end Alembic commands ###
