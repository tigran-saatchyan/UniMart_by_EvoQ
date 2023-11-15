"""updated email field params

Revision ID: 95adae9f1847
Revises: c7735f336fcf
Create Date: 2023-11-15 12:26:06.800931+04:00

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '95adae9f1847'
down_revision: Union[str, None] = 'c7735f336fcf'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('products', 'price',
               existing_type=sa.REAL(),
               type_=sa.Float(precision=2),
               existing_nullable=False,
               existing_server_default=sa.text("'0'::real"))
    op.alter_column('users', 'email',
               existing_type=sa.VARCHAR(length=255),
               type_=sa.String(length=320),
               existing_nullable=False)
    op.drop_constraint('users_email_key', 'users', type_='unique')
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.create_unique_constraint('users_email_key', 'users', ['email'])
    op.alter_column('users', 'email',
               existing_type=sa.String(length=320),
               type_=sa.VARCHAR(length=255),
               existing_nullable=False)
    op.alter_column('products', 'price',
               existing_type=sa.Float(precision=2),
               type_=sa.REAL(),
               existing_nullable=False,
               existing_server_default=sa.text("'0'::real"))
    # ### end Alembic commands ###
