from sqlalchemy import Column, Integer, String, Float, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Définition de la base pour la déclaration des modèles
Base = declarative_base()

# Définition du modèle pour stocker les résultats de la méthode de Newton
class NewtonResult(Base):
    __tablename__ = 'newton_results'  # Nom de la table dans la base de données

    id = Column(Integer, primary_key=True, autoincrement=True)  # Clé primaire
    equation = Column(String(255), nullable=False)  # L'équation saisie par l'utilisateur
    solution = Column(Float, nullable=False)  # La solution trouvée par la méthode de Newton
    iterations = Column(Integer, nullable=False)  # Nombre d'itérations effectuées
    success = Column(String(255), nullable=False)  # Indicateur de succès ou d'échec

# Configuration de la base de données
DATABASE_URL = "mysql+mysqlconnector://root@localhost:3306/newton_resolution_db"  # URL de connexion à la base de données
engine = create_engine(DATABASE_URL, echo=True)  # `echo=True` pour afficher les requêtes SQL exécutées

# Création automatique des tables
Base.metadata.create_all(bind=engine)

# Configuration de la session pour interagir avec la base
SessionLocal = sessionmaker(bind=engine)
