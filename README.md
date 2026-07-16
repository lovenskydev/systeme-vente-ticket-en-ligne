# Système de Vente de Billets en Ligne — Clean Architecture en Python

Ce projet est un système complet et fonctionnel de vente de billets en ligne, conçu selon les principes de la **Clean Architecture** (d'après Robert C. Martin). 

Le projet est entièrement découplé de toute interface ou base de données spécifique. Il utilise une base de données SQLite pour la persistance locale et une interface en ligne de commande (CLI) interactive et colorée.

---

## Principes de l'Architecture Propre (Clean Architecture)

L'architecture est organisée en couches concentriques où la règle d'or est respectée : **les dépendances ne pointent que vers l'intérieur**.

```
  +------------------------------------------+
  |  FRAMEWORKS & DRIVERS (CLI, SQLite)      |  Couche 4 (la plus externe)
  |   +--------------------------------+     |
  |   |  INTERFACE ADAPTERS            |     |  Couche 3
  |   |   +----------------------+   |     |
  |   |   |  USE CASES           |   |     |  Couche 2
  |   |   |   +--------------+   |   |     |
  |   |   |   |  ENTITIES    |   |   |     |  Couche 1 (le cœur)
  |   |   |   |              |   |   |     |
  |   |   |   +--------------+   |   |     |
  |   |   +----------------------+   |     |
  |   +--------------------------------+     |
  +------------------------------------------+
```

1. **Entities (Couche 1 - Cœur)** : Les objets métier purs (`Event`, `EventCategory`, `Ticket`) contenant les règles métier fondamentales (gestion des stocks, transitions d'états de billets). Ils ne dépendent d'aucune bibliothèque externe ou base de données.
2. **Use Cases (Couche 2 - Règles applicatives)** : Les cas d'usage de l'application (lister les événements, acheter un billet, lister les achats, annuler un billet, valider un billet). Ils définissent des interfaces abstraites (**Ports**) pour la persistance.
3. **Interface Adapters (Couche 3 - Adaptateurs)** : Les contrôleurs, présentateurs et implémentations de dépôts (Repositories SQLite et In-Memory) servant de pont entre la logique métier et les outils techniques.
4. **Frameworks & Drivers (Couche 4 - Périphérie)** : La base SQLite, le système de fichiers, et l'interface interactive en ligne de commande (CLI).

---

## Fonctionnalités Implémentées

Le système propose un menu interactif structuré comme suit :

1. **Afficher les événements & prix** : Affiche les détails des événements, leurs catégories de billets associées, le prix et les places disponibles en temps réel.
2. **Acheter un billet** : Permet à un utilisateur d'acheter un billet.
   - *Amélioration premium* : L'utilisateur recherche l'événement (l'ID complet ou ses premiers caractères suffisent).
   - *Menu dynamique* : Les catégories disponibles s'affichent sous forme de liste numérotée (ex: `1) VIP, 2) Regular`). L'utilisateur n'a qu'à saisir le chiffre correspondant pour choisir sa catégorie.
   - Réduit automatiquement le stock de places disponibles pour cette catégorie.
3. **Voir mes billets achetés** : Recherche et affiche tous les billets associés à l'adresse e-mail de l'acheteur avec leur statut actuel (Actif, Annulé, Utilisé).
4. **Annuler un billet** : Permet à un acheteur d'annuler son billet (en fournissant son e-mail de contrôle). Cette opération rembourse l'acheteur et remet automatiquement la place en stock pour l'événement.
5. **[ADMIN] Valider un billet à l'entrée** : Permet au personnel de l'événement de scanner/valider un billet (le marquant comme **Utilisé**). Un billet utilisé ou annulé ne peut pas être re-validé ou re-annulé.
6. **Quitter** : Ferme l'application proprement.

---

## Structure du Projet

```
Sales online Ticket/
│
├── src/
│   ├── entities/               # Couche 1 — Objets métier et règles métier pures
│   │   ├── event.py            # Modèles Event et EventCategory + validation de stocks
│   │   └── ticket.py           # Modèle Ticket + machine à états (Active, Cancelled, Used)
│   │
│   ├── use_cases/              # Couche 2 — Logique applicative orchestrant les entités
│   │   ├── interfaces/         # Les PORTS (Socket de connexion pour les adaptateurs)
│   │   │   ├── event_repository.py
│   │   │   └── ticket_repository.py
│   │   ├── list_events.py
│   │   ├── buy_ticket.py
│   │   ├── list_purchased_tickets.py
│   │   ├── cancel_ticket.py
│   │   └── validate_ticket.py
│   │
│   ├── interface_adapters/     # Couche 3 — Traducteurs de flux
│   │   ├── repositories/       # Implémentations concrètes des dépôts (ADAPTATEURS)
│   │   │   ├── in_memory_event_repository.py
│   │   │   ├── in_memory_ticket_repository.py
│   │   │   ├── sqlite_event_repository.py   # Persistance SQL standard (mapping ORM-free)
│   │   │   └── sqlite_ticket_repository.py  # Persistance SQL standard (mapping ORM-free)
│   │   ├── controllers/        # Contrôleur agnostique gérant les commandes d'interface
│   │   │   └── ticketing_controller.py
│   │   └── presenters/         # Convertit les entités brutes en structures d'affichage
│   │       └── ticketing_presenter.py
│   │
│   └── frameworks/             # Couche 4 — Livraison et infrastructure
│       └── cli/
│           └── cli_app.py      # Application console interactive colorée
│
├── tests/                      # Suite de tests automatisés (pytest)
│   ├── test_entities.py        # Tests unitaires des règles de validation métier
│   └── test_use_cases.py       # Tests d'intégration des interacteurs applicatifs
│
├── main_cli.py                 # Point d'entrée de l'application (Injection des Dépendances)
├── requirements.txt            # Dépendances de développement (pytest, pytest-cov)
└── ticketing.db                # Base de données SQLite auto-générée au premier lancement
```

---

## Installation & Démarrage

### 1. Prérequis
Assurez-vous d'avoir Python 3 installé sur votre machine.

### 2. Démarrer l'application
Exécutez le script d'entrée dans votre console :
```bash
py main_cli.py
```
*(Au premier démarrage, si la base de données est vide, trois événements de démonstration de grande envergure avec des stocks configurés seront automatiquement créés).*

### 3. Exécuter les tests automatisés
Pour lancer la suite complète des tests de validation et de cas d'usage :
```bash
py -m pytest tests/ -v
```

---

## Fonctionnalités Premium (Expérience Utilisateur)

- **Saisie simplifiée par Préfixe (Prefix ID Matching)** :
  Les identifiants générés pour les billets sont des UUIDs de 36 caractères complexes à saisir manuellement dans la console. Les adaptateurs intègrent un résolveur intelligent : vous pouvez saisir uniquement les premiers caractères de l'ID d'un événement ou d'un billet (ex: `even` pour l'événement `event-1` ou les 4 premiers caractères du code d'un billet), le système s'occupe de retrouver l'enregistrement complet de manière unique.
- **Sélection Numérotée de Catégorie** :
  Lors de l'achat, après avoir sélectionné l'événement, les catégories disponibles de billets (VIP, Standard, etc.) sont affichées avec un numéro. Saisissez simplement `1` ou `2` pour faire votre choix, évitant ainsi toute erreur de frappe.
