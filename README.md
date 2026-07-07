# Système de Vente de Tickets en Ligne

Mini-projet de fin de session (AUC) — application de vente de tickets en ligne
appliquant les principes de la **Clean Architecture**.

## Les 4 couches

- **domain** → les entités et règles métier de base
- **use_cases** → la logique de l'application
- **interface_adapters** → repositories et controllers
- **frameworks_drivers** → Flask + MySQL

## Installation

```bash
pip install -r requirements.txt
```

## Lancer l'application

```bash
python -m frameworks_drivers.web.app
```

## Auteur

Lovensky — Étudiant en informatique, AUC