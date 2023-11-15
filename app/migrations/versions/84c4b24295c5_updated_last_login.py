"""updated last_login

Revision ID: 84c4b24295c5
Revises: 49af15ac2ace
Create Date: 2023-11-15 15:00:54.441519+04:00

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '84c4b24295c5'
down_revision: Union[str, None] = '49af15ac2ace'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('products', 'price',
               existing_type=sa.REAL(),
               type_=sa.Float(precision=2),
               existing_nullable=False,
               existing_server_default=sa.text("'0'::real"))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('products', 'price',
               existing_type=sa.Float(precision=2),
               type_=sa.REAL(),
               existing_nullable=False,
               existing_server_default=sa.text("'0'::real"))
    # ### end Alembic commands ###
