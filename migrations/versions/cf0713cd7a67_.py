"""Add transaction type

Revision ID: cf0713cd7a67
Revises: 941d3daf60e1
Create Date: 2018-06-06 22:36:07.052209

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision = 'cf0713cd7a67'
down_revision = '941d3daf60e1'
branch_labels = None
depends_on = None


def upgrade():
    transaction_type = postgresql.ENUM('buy', 'sell', name='transactiontype')
    transaction_type.create(op.get_bind())
    op.add_column('transactions', sa.Column('type', sa.Enum('buy', 'sell', name='transactiontype'), nullable=True))


def downgrade():
    op.drop_column('transactions', 'type')
    transaction_type = postgresql.ENUM('buy', 'sell', name='transactiontype')
    transaction_type.drop(op.get_bind())
