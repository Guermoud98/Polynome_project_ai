from sqlalchemy import Column, Integer, Float, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Base de SQLAlchemy
Base = declarative_base()

# Modèle pour stocker les équations quadratiques et leurs solutions
class QuadraticEquation(Base):
    __tablename__ = 'quadratic_equations'

    id = Column(Integer, primary_key=True, autoincrement=True)
    a = Column(Float, nullable=False)
    b = Column(Float, nullable=False)
    c = Column(Float, nullable=False)
    equation = Column(String(255), nullable=False)
    roots = Column(String(255), nullable=False)

# Configuration de la base de données
DATABASE_URL = "mysql+mysqlconnector://root@localhost:3306/quadratic_db"
engine = create_engine(DATABASE_URL, echo=True)
Base.metadata.create_all(bind=engine)

# Session pour interagir avec la base
SessionLocal = sessionmaker(bind=engine)
