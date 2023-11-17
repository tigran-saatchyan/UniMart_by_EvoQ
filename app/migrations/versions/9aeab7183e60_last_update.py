"""last update

Revision ID: 9aeab7183e60
Revises: b81f481e022a
Create Date: 2023-11-17 12:32:36.974051+04:00

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9aeab7183e60'
down_revision: Union[str, None] = 'b81f481e022a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('cart', 'price',
               existing_type=sa.REAL(),
               type_=sa.Float(precision=2),
               existing_nullable=False,
               existing_server_default=sa.text("'0'::real"))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('cart', 'price',
               existing_type=sa.Float(precision=2),
               type_=sa.REAL(),
               existing_nullable=False,
               existing_server_default=sa.text("'0'::real"))
    # ### end Alembic commands ###