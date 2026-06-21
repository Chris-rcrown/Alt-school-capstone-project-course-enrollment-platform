from sqlalchemy.orm import declarative_base

Base = declarative_base()

# Import models so they are registered on Base.metadata.
import app.models.user  # noqa: E402,F401
import app.models.course  # noqa: E402,F401
import app.models.enrollment  # noqa: E402,F401
import app.models.enrollment_audit_log  # noqa: E402,F401
