"""empty message

Revision ID: 421ba9f0ea0a
Revises: 008246f8471e
Create Date: 2020-02-11 01:15:25.807657

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "421ba9f0ea0a"
down_revision = "008246f8471e"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(
        "uq_unique_follow", "follows", ["follower_id", "following_id"]
    )
    op.create_check_constraint(
        "ck_no_follow_yourself", "follows", "follower_id <> following_id"
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint("uq_unique_follow", "follows", type_="unique")
    op.drop_constraint("ck_no_follow_yourself", "follows", type_="check")
    # ### end Alembic commands ###
