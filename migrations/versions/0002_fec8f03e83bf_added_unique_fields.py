"""added unique fields

Revision ID: fec8f03e83bf
Revises: 5f76e157c207
Create Date: 2023-05-01 16:57:35.202843

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision = 'fec8f03e83bf'
down_revision = '5f76e157c207'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(op.f('uq_users_email'), 'users', ['email'])
    op.create_unique_constraint(op.f('uq_users_username'), 'users', ['username'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(op.f('uq_users_username'), 'users', type_='unique')
    op.drop_constraint(op.f('uq_users_email'), 'users', type_='unique')
    # ### end Alembic commands ###