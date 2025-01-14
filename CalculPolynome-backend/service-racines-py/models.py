from sqlalchemy import Column, Integer, String, Text, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

# Définition de la table pour stocker les racines
class PolynomialRoots(Base):
    __tablename__ = "polynomial_roots"

    id = Column(Integer, primary_key=True, autoincrement=True)
    equation = Column(Text, nullable=False)  # L'équation originale
    roots = Column(Text, nullable=False)  # Les racines calculées

# Configuration de la base de données
DATABASE_URL = "mysql+mysqlconnector://root@localhost:3306/polynome_racine"
engine = create_engine(DATABASE_URL, echo=True)

# Création des tables
Base.metadata.create_all(bind=engine)

# Configuration de la session
SessionLocal = sessionmaker(bind=engine)
