from typing import Optional
from sqlalchemy import String, Float, ForeignKey, Table, Column
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    relationship,
)


class Base(DeclarativeBase):
    pass


organization_activity = Table(
    "organization_activity",
    Base.metadata,
    Column("organization_id", ForeignKey("organizations.id"), primary_key=True),
    Column("activity_id", ForeignKey("activities.id"), primary_key=True),
)


class Building(Base):
    __tablename__ = "buildings"

    id: Mapped[int] = mapped_column(primary_key=True)
    address: Mapped[str] = mapped_column(String(255))
    latitude: Mapped[float] = mapped_column(Float)
    longitude: Mapped[float] = mapped_column(Float)

    organizations: Mapped[list["Organization"]] = relationship(back_populates="building")


class Activity(Base):
    __tablename__ = "activities"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255))
    parent_id: Mapped[Optional[int]] = mapped_column(ForeignKey("activities.id"), nullable=True)

    parent: Mapped[Optional["Activity"]] = relationship(
        remote_side=[id],
        back_populates="children"
    )
    children: Mapped[list["Activity"]] = relationship(back_populates="parent")

    organizations: Mapped[list["Organization"]] = relationship(
        secondary=organization_activity,
        back_populates="activities",
    )


class Organization(Base):
    __tablename__ = "organizations"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255))

    building_id: Mapped[int] = mapped_column(ForeignKey("buildings.id"))
    building: Mapped["Building"] = relationship(back_populates="organizations")

    activities: Mapped[list["Activity"]] = relationship(
        secondary=organization_activity,
        back_populates="organizations",
    )

    phones: Mapped[list["Phone"]] = relationship(back_populates="organization")


class Phone(Base):
    __tablename__ = "phones"

    id: Mapped[int] = mapped_column(primary_key=True)
    number: Mapped[str] = mapped_column(String(50))
    organization_id: Mapped[int] = mapped_column(ForeignKey("organizations.id"))

    organization: Mapped["Organization"] = relationship(back_populates="phones")
