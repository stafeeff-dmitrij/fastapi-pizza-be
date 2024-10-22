"""Add description for pizza model

Revision ID: d1f997eda9be
Revises: 5464ed0e19d7
Create Date: 2024-10-22 17:18:43.660689

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd1f997eda9be'
down_revision: Union[str, None] = '5464ed0e19d7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('pizza', sa.Column('description', sa.String(length=300), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('pizza', 'description')
    # ### end Alembic commands ###
