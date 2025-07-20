import enum
from datetime import datetime, timezone

from .engine import Base
from sqlalchemy import Boolean, Column, DateTime, Enum, ForeignKey, Integer, String
from sqlalchemy.orm import relationship


class EmbeddingStatus(str, enum.Enum):
    PENDING = "PENDING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    github_id = Column(Integer, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True)
    avatar_url = Column(String)
    access_token = Column(String, nullable=False)  # TODO: REMEMBER TO ENCRYPT!
    created_at = Column(DateTime(timezone=True),
                        default=lambda: datetime.now(timezone.utc))

    # Relationship to GithubRepository
    repositories = relationship("GithubRepository", back_populates="owner")


class GithubRepository(Base):
    __tablename__ = "github_repositories"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    repo_id = Column(Integer, unique=True, index=True, nullable=False)
    repo_name = Column(String, nullable=False)
    repo_full_name = Column(String, nullable=False)
    is_private = Column(Boolean, default=False)
    embedding_status = Column(Enum(EmbeddingStatus),
                              default=EmbeddingStatus.PENDING)
    last_embedded_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True),
                        default=lambda: datetime.now(timezone.utc))

    # Relationship to User
    owner = relationship("User", back_populates="repositories")
