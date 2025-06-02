from sqlalchemy import create_engine, Column, String, JSON, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import uuid

Base = declarative_base()

class AgentMemory(Base):
    __tablename__ = 'agent_memory'
    
    id = Column(
        String(36), 
        primary_key=True,
        default=lambda: str(uuid.uuid4())  # Auto-generate UUID
    )
    input_metadata = Column(JSON)
    extracted_fields = Column(JSON)
    actions_triggered = Column(JSON)
    decision_trace = Column(JSON)
    timestamp = Column(DateTime, default=datetime.utcnow)  # Store timestamp in UTC
    
class MemoryManager:
    def __init__(self, db_url):  # <-- Accept db_url here!
        self.engine = create_engine(db_url)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)

    def log_interaction(self, interaction_data):
        session = self.Session()
        try:
            new_entry = AgentMemory(
                id=str(uuid.uuid4()),  # Explicit ID generation
                input_metadata=interaction_data.get('input_metadata'),
                extracted_fields=interaction_data.get('extracted_fields'),
                actions_triggered=interaction_data.get('actions_triggered'),
                decision_trace=interaction_data.get('decision_trace')
            )
            session.add(new_entry)
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()