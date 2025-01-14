from sqlalchemy import Column, Integer, Text, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# déclaration de la base pour les modèles SQLAlchemy
Base = declarative_base()

# Modèle pour la table des polynômes
class Polynomial(Base):
    __tablename__ = 'polynome'

    id = Column(Integer, primary_key=True, autoincrement=True)  # Clé primaire auto-incrémentée
    equation = Column(Text, nullable=False)  # Colonne pour l'équation d'entrée
    factorized_result = Column(Text, nullable=False)  # Colonne pour le résultat factorisé

# Configuration de la base de données
DATABASE_URL = "mysql+mysqlconnector://root@localhost:3306/factorisation_db"
engine = create_engine(DATABASE_URL, echo=True)  # echo=True pour afficher les requêtes SQL dans la console

# Création de la table automatiquement si elle n'existe pas
Base.metadata.create_all(bind=engine)

# Configuration de la session pour interagir avec la base de données
SessionLocal = sessionmaker(bind=engine)
