from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime

import sqlalchemy as sa
from sqlalchemy import Engine, create_engine

from civic311.request_intake import ServiceRequestIntake, create_service_request_stub
from civic311.triage import suggest_triage


metadata = sa.MetaData()

service_request_records = sa.Table(
    "service_request_records",
    metadata,
    sa.Column("request_id", sa.String(160), primary_key=True),
    sa.Column("category", sa.String(255), nullable=False),
    sa.Column("description", sa.Text(), nullable=False),
    sa.Column("location", sa.String(500), nullable=False),
    sa.Column("intake_notes", sa.JSON(), nullable=False),
    sa.Column("disclaimer", sa.Text(), nullable=False),
    sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    schema="civic311",
)

triage_review_records = sa.Table(
    "triage_review_records",
    metadata,
    sa.Column("request_id", sa.String(160), primary_key=True),
    sa.Column("category", sa.String(255), nullable=False),
    sa.Column("priority", sa.String(120), nullable=False),
    sa.Column("suggested_department", sa.String(255), nullable=False),
    sa.Column("reasons", sa.JSON(), nullable=False),
    sa.Column("staff_review_required", sa.Boolean(), nullable=False),
    sa.Column("disclaimer", sa.Text(), nullable=False),
    sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    schema="civic311",
)


@dataclass(frozen=True)
class StoredTriageReview:
    request_id: str
    category: str
    priority: str
    suggested_department: str
    reasons: tuple[str, ...]
    staff_review_required: bool
    disclaimer: str
    created_at: datetime


class ServiceRequestRepository:
    """SQLAlchemy-backed resident service request and triage-review records."""

    def __init__(self, *, db_url: str | None = None, engine: Engine | None = None) -> None:
        base_engine = engine or create_engine(db_url or "sqlite+pysqlite:///:memory:", future=True)
        if base_engine.dialect.name == "sqlite":
            self.engine = base_engine.execution_options(schema_translate_map={"civic311": None})
        else:
            self.engine = base_engine
            with self.engine.begin() as connection:
                connection.execute(sa.text("CREATE SCHEMA IF NOT EXISTS civic311"))
        metadata.create_all(self.engine)

    def create_request(
        self, *, request_id: str, category: str, description: str, location: str
    ) -> ServiceRequestIntake:
        intake = create_service_request_stub(
            request_id=request_id,
            category=category,
            description=description,
            location=location,
        )
        now = datetime.now(UTC)
        with self.engine.begin() as connection:
            exists = connection.execute(
                sa.select(service_request_records.c.request_id).where(
                    service_request_records.c.request_id == intake.request_id
                )
            ).first()
            values = {
                "request_id": intake.request_id,
                "category": intake.category,
                "description": intake.description,
                "location": intake.location,
                "intake_notes": list(intake.intake_notes),
                "disclaimer": intake.disclaimer,
                "updated_at": now,
            }
            if exists is None:
                connection.execute(service_request_records.insert().values(**values, created_at=now))
            else:
                connection.execute(
                    service_request_records.update()
                    .where(service_request_records.c.request_id == intake.request_id)
                    .values(**values)
                )
        return intake

    def get_request(self, request_id: str) -> ServiceRequestIntake | None:
        with self.engine.begin() as connection:
            row = connection.execute(
                sa.select(service_request_records).where(
                    service_request_records.c.request_id == request_id
                )
            ).mappings().first()
        if row is None:
            return None
        return _row_to_request(row)

    def create_triage_review(
        self, *, request_id: str, category: str, description: str, location: str
    ) -> StoredTriageReview:
        triage = suggest_triage(category=category, description=description, location=location)
        stored = StoredTriageReview(
            request_id=request_id.strip() or "unassigned-request",
            category=triage.category,
            priority=triage.priority,
            suggested_department=triage.suggested_department,
            reasons=triage.reasons,
            staff_review_required=triage.staff_review_required,
            disclaimer=triage.disclaimer,
            created_at=datetime.now(UTC),
        )
        with self.engine.begin() as connection:
            connection.execute(
                triage_review_records.insert().values(
                    request_id=stored.request_id,
                    category=stored.category,
                    priority=stored.priority,
                    suggested_department=stored.suggested_department,
                    reasons=list(stored.reasons),
                    staff_review_required=stored.staff_review_required,
                    disclaimer=stored.disclaimer,
                    created_at=stored.created_at,
                )
            )
        return stored

    def get_triage_review(self, request_id: str) -> StoredTriageReview | None:
        with self.engine.begin() as connection:
            row = connection.execute(
                sa.select(triage_review_records).where(triage_review_records.c.request_id == request_id)
            ).mappings().first()
        if row is None:
            return None
        return _row_to_triage(row)


def _row_to_request(row: object) -> ServiceRequestIntake:
    data = dict(row)
    return ServiceRequestIntake(
        request_id=data["request_id"],
        category=data["category"],
        description=data["description"],
        location=data["location"],
        intake_notes=tuple(data["intake_notes"]),
        disclaimer=data["disclaimer"],
    )


def _row_to_triage(row: object) -> StoredTriageReview:
    data = dict(row)
    return StoredTriageReview(
        request_id=data["request_id"],
        category=data["category"],
        priority=data["priority"],
        suggested_department=data["suggested_department"],
        reasons=tuple(data["reasons"]),
        staff_review_required=data["staff_review_required"],
        disclaimer=data["disclaimer"],
        created_at=data["created_at"],
    )
