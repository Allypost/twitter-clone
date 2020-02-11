"""empty message

Revision ID: 305bf169ef28
Revises: 6081fefff4ef
Create Date: 2020-02-11 21:39:08.613837

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "305bf169ef28"
down_revision = "6081fefff4ef"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("images", sa.Column("uploader_id", sa.Integer(), nullable=True))
    op.create_foreign_key(None, "images", "users", ["uploader_id"], ["id"])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, "images", type_="foreignkey")
    op.drop_column("images", "uploader_id")
    # ### end Alembic commands ###
