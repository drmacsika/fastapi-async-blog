"""Removed index from email.

Revision ID: 9150a2b603d9
Revises: 48245b4ab25a
Create Date: 2021-10-14 23:08:22.507568

"""
from alembic import op
import sqlalchemy as sa
from core.base import Base


# revision identifiers, used by Alembic.
revision = '9150a2b603d9'
down_revision = '48245b4ab25a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_contacts_email', table_name='contacts')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_index('ix_contacts_email', 'contacts', ['email'], unique=False)
    # ### end Alembic commands ###
