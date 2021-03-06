"""empty message

Revision ID: 008246f8471e
Revises: a916447816d6
Create Date: 2020-02-10 23:56:57.968105

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "008246f8471e"
down_revision = "a916447816d6"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "follows",
        sa.Column("follower_id", sa.Integer(), nullable=False),
        sa.Column("following_id", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["follower_id"], ["users.id"]),
        sa.ForeignKeyConstraint(["following_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("follower_id", "following_id"),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("follows")
    # ### end Alembic commands ###
