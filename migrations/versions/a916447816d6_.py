"""empty message

Revision ID: a916447816d6
Revises: 
Create Date: 2020-02-07 20:36:49.951858

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "a916447816d6"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "images",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("fs_path", sa.String(length=511), nullable=False),
        sa.Column("hash", sa.String(length=511), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name"),
    )
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.Column("username", sa.String(length=255), nullable=False),
        sa.Column("password", sa.String(length=511), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("username"),
    )
    op.create_table(
        "tweets",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.Column("text", sa.Text(), nullable=False),
        sa.Column("poster_id", sa.Integer(), nullable=False),
        sa.Column("image_id", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(["image_id"], ["images.id"]),
        sa.ForeignKeyConstraint(["poster_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("tweets")
    op.drop_table("users")
    op.drop_table("images")
    # ### end Alembic commands ###