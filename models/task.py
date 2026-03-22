from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import relationship
from database import Base
from models.user import User

class Task(Base):
    __tablename__ = "tasks"

    id: int = Column(Integer, primary_key=True, index=True)
    title: str = Column(String, index=True)
    description: str | None = Column(String, index=True)
    completed: bool = Column(Boolean, default=False)
    created_at: DateTime = Column(DateTime, index=True)
    updated_at: DateTime = Column(DateTime, index=True)
    user_id: int = Column(Integer, index=True)
    user: User = relationship("User", back_populates="tasks")

    def __repr__(self):
        return f"Task(id={self.id}, title='{self.title}', description='{self.description}', completed={self.completed}, created_at='{self.created_at}', updated_at='{self.updated_at}', user_id={self.user_id})"