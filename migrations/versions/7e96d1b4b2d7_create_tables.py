"""create tables

Revision ID: 7e96d1b4b2d7
Revises: 
Create Date: 2024-12-09 12:18:02.257773

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "7e96d1b4b2d7"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "apk1",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("file_id", sa.String(), nullable=False),
        sa.Column("caption_en", sa.String(), nullable=False),
        sa.Column("caption_ua", sa.String(), nullable=False),
        sa.Column("caption_ru", sa.String(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column(
            "updated_at",
            sa.DateTime(),
            server_default=sa.text("(CURRENT_TIMESTAMP)"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "apk2",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("file_id", sa.String(), nullable=False),
        sa.Column("caption_en", sa.String(), nullable=False),
        sa.Column("caption_ua", sa.String(), nullable=False),
        sa.Column("caption_ru", sa.String(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column(
            "updated_at",
            sa.DateTime(),
            server_default=sa.text("(CURRENT_TIMESTAMP)"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "galery_category",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("title_en", sa.String(length=100), nullable=False),
        sa.Column("title_ua", sa.String(length=100), nullable=False),
        sa.Column("title_ru", sa.String(length=100), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column(
            "updated_at",
            sa.DateTime(),
            server_default=sa.text("(CURRENT_TIMESTAMP)"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("title_en"),
        sa.UniqueConstraint("title_ru"),
        sa.UniqueConstraint("title_ua"),
    )
    op.create_table(
        "ref_start_text",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("ref", sa.String(length=64), nullable=False),
        sa.Column("ref_url", sa.String(), nullable=False),
        sa.Column("img", sa.String(), nullable=False),
        sa.Column("en", sa.String(), nullable=False),
        sa.Column("ua", sa.String(), nullable=False),
        sa.Column("ru", sa.String(), nullable=False),
        sa.Column("btn_en", sa.String(), nullable=False),
        sa.Column("btn_ua", sa.String(), nullable=False),
        sa.Column("btn_ru", sa.String(), nullable=False),
        sa.Column("answer_en", sa.String(), nullable=False),
        sa.Column("answer_ua", sa.String(), nullable=False),
        sa.Column("answer_ru", sa.String(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column(
            "updated_at",
            sa.DateTime(),
            server_default=sa.text("(CURRENT_TIMESTAMP)"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "sub_channel",
        sa.Column("id", sa.BigInteger(), nullable=False),
        sa.Column("username", sa.String(), nullable=False),
        sa.Column("invate_url", sa.String(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column(
            "updated_at",
            sa.DateTime(),
            server_default=sa.text("(CURRENT_TIMESTAMP)"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "users",
        sa.Column("id", sa.BigInteger(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("active", sa.Boolean(), nullable=False),
        sa.Column("chat_type", sa.String(length=20), nullable=False),
        sa.Column("subscribe", sa.Boolean(), nullable=False),
        sa.Column("premium", sa.Boolean(), nullable=False),
        sa.Column("referal", sa.String(length=50), nullable=True),
        sa.Column("locale", sa.String(length=2), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column(
            "updated_at",
            sa.DateTime(),
            server_default=sa.text("(CURRENT_TIMESTAMP)"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "img_galery",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("img_id", sa.String(), nullable=False),
        sa.Column("category_id", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column(
            "updated_at",
            sa.DateTime(),
            server_default=sa.text("(CURRENT_TIMESTAMP)"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(["category_id"], ["galery_category.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("img_galery")
    op.drop_table("users")
    op.drop_table("sub_channel")
    op.drop_table("ref_start_text")
    op.drop_table("galery_category")
    op.drop_table("apk2")
    op.drop_table("apk1")
    # ### end Alembic commands ###
