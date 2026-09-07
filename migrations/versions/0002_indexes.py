"""Align migration indexes with ORM lookup fields."""

from alembic import op

revision = "0002"
down_revision = "0001"
branch_labels = None
depends_on = None


def upgrade():
    op.create_index("ix_jobs_title", "jobs", ["title"])
    op.create_index("ix_jobs_company", "jobs", ["company"])
    op.create_index("ix_applications_stage", "applications", ["stage"])


def downgrade():
    op.drop_index("ix_applications_stage", table_name="applications")
    op.drop_index("ix_jobs_company", table_name="jobs")
    op.drop_index("ix_jobs_title", table_name="jobs")
