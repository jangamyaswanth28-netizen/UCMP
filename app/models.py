
import uuid
from sqlalchemy import Column, String, Boolean, Integer, Timestamp, ForeignKey, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from .database import Base

class User(Base):
    __tablename__ = "users"
    user_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String, unique=True, nullable=False)
    phone = Column(String)
    created_at = Column(Timestamp, server_default=func.now())
    updated_at = Column(Timestamp, server_default=func.now(), onupdate=func.now())

class ConsentType(Base):
    __tablename__ = "consent_types"
    consent_type_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    consent_code = Column(String, unique=True, nullable=False)
    description = Column(String)
    is_mandatory = Column(Boolean, default=False)
    created_at = Column(Timestamp, server_default=func.now())

class SourceSystem(Base):
    __tablename__ = "source_systems"
    source_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    source_name = Column(String, nullable=False)
    source_type = Column(String)
    created_at = Column(Timestamp, server_default=func.now())

class PolicyVersion(Base):
    __tablename__ = "policy_versions"
    policy_version_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    version_number = Column(String, nullable=False)
    policy_document_url = Column(String)
    effective_from = Column(Timestamp)
    effective_to = Column(Timestamp)

class ConsentEvent(Base):
    __tablename__ = "consent_events"
    event_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.user_id"))
    consent_type_id = Column(UUID(as_uuid=True), ForeignKey("consent_types.consent_type_id"))
    source_id = Column(UUID(as_uuid=True), ForeignKey("source_systems.source_id"))
    policy_version_id = Column(UUID(as_uuid=True), ForeignKey("policy_versions.policy_version_id"))
    status = Column(String)
    sequence_number = Column(Integer)
    event_timestamp = Column(Timestamp)
    received_at = Column(Timestamp, server_default=func.now())

    __table_args__ = (
        UniqueConstraint("user_id", "consent_type_id", "sequence_number", name="uq_event_seq"),
    )

class ConsentCurrent(Base):
    __tablename__ = "consent_current"
    current_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.user_id"))
    consent_type_id = Column(UUID(as_uuid=True), ForeignKey("consent_types.consent_type_id"))
    status = Column(String)
    latest_sequence_number = Column(Integer)
    updated_at = Column(Timestamp, server_default=func.now(), onupdate=func.now())

    __table_args__ = (
        UniqueConstraint("user_id", "consent_type_id", name="uq_current_user_consent"),
    )

class AuditLog(Base):
    __tablename__ = "audit_log"
    audit_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    event_id = Column(UUID(as_uuid=True), ForeignKey("consent_events.event_id"))
    action_type = Column(String)
    performed_by = Column(String)
    action_timestamp = Column(Timestamp, server_default=func.now())
