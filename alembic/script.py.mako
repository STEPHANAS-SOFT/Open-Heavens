"""\nRevision ID: ${up_revision}\nRevises: ${down_revision | comma,n}
Create Date: ${create_date}\n\n"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = ${repr(up_revision)}
down_revision = ${repr(down_revision)}
branch_labels = None
depends_on = None


def upgrade():
    pass


def downgrade():
    pass
