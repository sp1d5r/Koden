"""Add Tasks to db.

Revision ID: 29046abc1ea8
Revises: e3efebf5495c
Create Date: 2025-06-08 17:18:31.909944

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = '29046abc1ea8'
down_revision: Union[str, None] = 'e3efebf5495c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('task',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('task_id', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('status', sa.String(length=20), server_default='pending', nullable=False),
    sa.Column('output_path', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('error_message', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.CheckConstraint("status IN ('pending', 'processing', 'completed', 'failed')", name='valid_task_status'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('repo_download_tasks',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('task_id', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('status', sa.String(length=20), server_default='pending', nullable=False),
    sa.Column('output_path', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('error_message', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.Column('repo_id', sa.Integer(), nullable=False),
    sa.CheckConstraint("status IN ('pending', 'processing', 'completed', 'failed')", name='valid_repo_download_task_status'),
    sa.ForeignKeyConstraint(['repo_id'], ['repo.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('repo_download_tasks')
    op.drop_table('task')
    # ### end Alembic commands ###
