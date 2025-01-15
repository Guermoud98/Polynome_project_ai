# Polynome_project_ai **Résolution d'Équations Polynômiales avec une Architecture Microservices**

Ce projet vise à fournir une solution modulaire et extensible pour résoudre des équations polynomiales à l'aide d'une architecture basée sur les microservices. Le système intègre des technologies modernes comme *Spring Boot*, *React*, et *Flutter* pour garantir performance et adaptabilité.

---

## **Table des Matières**
- [Description du Projet](#description-du-projet)
- [Technologies Utilisées](#technologies-utilisées)
- [Architecture](#architecture)
- [Fonctionnalités](#fonctionnalités)
- [Installation](#installation)
- [Utilisation](#utilisation)
- [Exemples Illustratifs](#exemples-illustratifs)
- [Contributeurs](#contributeurs)
- [Licence](#licence)

---

## **Description du Projet**

Cette application résout des équations polynomiales en utilisant des méthodes analytiques et numériques. Elle est conçue pour être scalable, modulaire, et capable d'intégrer facilement de nouvelles fonctionnalités. Voici les méthodes principales prises en charge :

- **Calcul des racines** : Méthodes pour trouver les racines des polynômes.
- **Factorisation** : Techniques pour factoriser les polynômes.
- **Calcul par la méthode de Newton** : Approches analytiques pour raffiner les solutions.
- **Calcul quadratique** : Résolutions spécifiques à des polynômes du second degré.
- **Visualisation graphique** : Présentation des solutions sous forme de graphes.

---

## **Technologies Utilisées**

- **Frontend** : React, Flutter
- **Backend** : Spring Boot avec Spring Cloud Gateway Python Flask
- **Service Discovery** : Netflix Eureka
- **Base de Données** : MySQL

---

## **Architecture**

L'application est divisée en plusieurs composants :

- **Client REST API** : Les frontends envoient des requêtes utilisateur au backend.
- **Passerelle** : Spring Cloud Gateway route les requêtes vers les microservices appropriés.
- **Microservices** : Services indépendants pour traiter des tâches spécifiques.
- **Service Discovery** : Netflix Eureka pour la découverte dynamique des microservices.

[Consultez l'architecture ici](https://app.eraser.io/workspace/ckNFDmpsj8GlPOET39RP?origin=share)

---

## **Fonctionnalités**

- **Calcul des racines** : Trouver les solutions d'un polynôme.
- **Factorisation** : Diviser les polynômes en facteurs.
- **Calcul par la méthode de Newton** : Approximation des solutions analytiques.
- **Calcul quadratique** : Résolution des polynômes du second degré.
- **Visualisation graphique** : Représentation graphique des polynômes et de leurs racines.

---

## **Installation**

### **Backend**
1. Cloner ce dépôt :
   ```bash
   git clone https://github.com/Neha-ETTALEBY/PolynomesSolver-microservices.git
   ```
2. Naviguer dans le répertoire backend et lancer les services :
   ```bash
   cd CalculPolynome-backend
   mvn clean install
   mvn spring-boot:run
   ```

### **Frontend React**
1. Aller dans le répertoire React :
   ```bash
   cd polynome_front_react
   ```
2. Installer les dépendances :
   ```bash
   npm install
   ```
3. Lancer le serveur de développement :
   ```bash
   npm start
   ```

### **Frontend Flutter**
1. Naviguer dans le répertoire Flutter :
   ```bash
   cd polynome_front_flutter
   ```
2. Vérifier l'installation de Flutter :
   ```bash
   flutter doctor
   ```
3. Lancer l'application :
   ```bash
   flutter run
   ```

---

## **Utilisation**

1. Accédez à l'interface utilisateur via `http://localhost:3000` pour React ou `http://10.0.2.2:8081` pour Flutter.
2. Saisissez une équation polynomiale et sélectionnez la méthode de résolution souhaitée.
3. Consultez les résultats affichés sur l'interface.

---

## **Exemples Illustratifs**

### Exemple 1 : Résolution d'un polynôme 
**Polynôme :** `x² - 5x + 6 = 0`  
**Résultat :** `x = 2, x = 3`

---

## **Vidéo Démonstrative**

- [Démonstration Backend & Frontend](https://github.com/user-attachments/assets/52c34e39-b6e8-420a-af23-55b1330a4ec2)
- [Démonstration Mobile Flutter](https://github.com/user-attachments/assets/68736cf1-891f-4c27-a825-03b8cb6e1e44)

---

## **Contributeurs**

- **Maria GUERMOUD**
- **Aya ELFAHIMI**
- **Douaa ELFAHIMI**
- **Aziza ATIGUI**
- **Neha ET-TALEBY**

---

## **Licence**

Ce projet est sous licence MIT. Voir le fichier LICENSE pour plus de détails.
