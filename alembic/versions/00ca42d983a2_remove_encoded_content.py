"""remove_encoded_content

Revision ID: 00ca42d983a2
Revises: 
Create Date: 2024-12-26 13:57:45.123456

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '00ca42d983a2'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 修改 content 字段类型为 VARCHAR(255)
    op.alter_column('disaster_data', 'content',
                    existing_type=sa.Text(),
                    type_=sa.String(length=255),
                    existing_nullable=True)
    
    # 删除 encoded_content 字段
    op.drop_column('disaster_data', 'encoded_content')


def downgrade() -> None:
    # 添加 encoded_content 字段
    op.add_column('disaster_data',
                  sa.Column('encoded_content', sa.Text(), nullable=True))
    
    # 恢复 content 字段类型为 TEXT
    op.alter_column('disaster_data', 'content',
                    existing_type=sa.String(length=255),
                    type_=sa.Text(),
                    existing_nullable=True)
