from datetime import datetime
from uuid import uuid4

from sqlalchemy import DateTime, Float, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.database import Base


class Transaction(Base):
    __tablename__ = "transactions"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    customer: Mapped[str] = mapped_column(String(255), nullable=False)
    amount: Mapped[float] = mapped_column(Float, nullable=False)
    currency: Mapped[str] = mapped_column(String(10), nullable=False, default="USD")
    location: Mapped[str] = mapped_column(String(255), nullable=False)
    merchant: Mapped[str] = mapped_column(String(255), nullable=False)
    risk: Mapped[str] = mapped_column(String(50), nullable=False)
    status: Mapped[str] = mapped_column(String(50), nullable=False)
    action: Mapped[str] = mapped_column(String(100), nullable=False)
    risk_score: Mapped[int] = mapped_column(Integer, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    investigations: Mapped[list["Investigation"]] = relationship(back_populates="transaction", cascade="all, delete-orphan")


class Investigation(Base):
    __tablename__ = "investigations"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    transaction_id: Mapped[str] = mapped_column(ForeignKey("transactions.id", ondelete="CASCADE"), nullable=False, index=True)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="open")
    severity: Mapped[str] = mapped_column(String(50), nullable=False, default="medium")
    assigned_to: Mapped[str | None] = mapped_column(String(255), nullable=True)
    summary: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    transaction: Mapped[Transaction] = relationship(back_populates="investigations")
    memories: Mapped[list["Memory"]] = relationship(back_populates="investigation", cascade="all, delete-orphan")


class Memory(Base):
    __tablename__ = "memories"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    investigation_id: Mapped[str | None] = mapped_column(ForeignKey("investigations.id", ondelete="SET NULL"), nullable=True, index=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    risk_level: Mapped[str] = mapped_column(String(50), nullable=False)
    fraud_type: Mapped[str] = mapped_column(String(100), nullable=False)
    confidence: Mapped[float] = mapped_column(Float, nullable=False)
    learning_impact: Mapped[str | None] = mapped_column(String(255), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    investigation: Mapped[Investigation | None] = relationship(back_populates="memories")


class HindsightMemory(Base):
    """Stores analyst feedback on investigation outcomes."""
    __tablename__ = "hindsight_memories"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    investigation_id: Mapped[str] = mapped_column(ForeignKey("investigations.id", ondelete="CASCADE"), nullable=False, index=True)
    transaction_id: Mapped[str] = mapped_column(String(36), nullable=False, index=True)
    
    # Transaction context
    amount: Mapped[float] = mapped_column(Float, nullable=False)
    location: Mapped[str] = mapped_column(String(255), nullable=False)
    merchant: Mapped[str] = mapped_column(String(255), nullable=False)
    
    # Original investigation outcome
    original_risk_level: Mapped[str] = mapped_column(String(50), nullable=False)
    original_confidence: Mapped[float] = mapped_column(Float, nullable=False)
    
    # Analyst feedback
    feedback_type: Mapped[str] = mapped_column(String(50), nullable=False)  # "confirm_fraud", "false_positive", "legitimate"
    analyst_notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    
    # Actual outcome
    actual_outcome: Mapped[str] = mapped_column(String(100), nullable=False)  # What actually happened
    
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)