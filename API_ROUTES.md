# API Routes - GP Admin

## Génération automatique des codes

Lors de la création d'un employé, le système génère automatiquement :
- **code_unique** : Code à 4 chiffres pour l'authentification biométrique
- **employee_code** : Code à 4 chiffres pour identifier l'employé

Ces codes sont uniques et ne peuvent pas être dupliqués.

## Routes pour la gestion des employés et empreintes

### 1. Obtenir l'ID d'un utilisateur par employee_code
```
GET /employes/by-code/{employee_code}
```
**Paramètres :**
- `employee_code` (string) : Le code employé

**Réponse :**
```json
{
  "user_id": "uuid-de-l-employe",
  "full_name": "Nom complet de l'employé"
}
```

### 2. Mettre à jour les empreintes d'un utilisateur
```
PUT /employes/{user_id}/empreintes
```
**Paramètres :**
- `user_id` (string) : L'ID UUID de l'utilisateur

**Body :**
```json
{
  "empreinte_ids": [1, 2, 3]
}
```

**Réponse :**
```json
{
  "message": "Empreintes mises à jour avec succès. 3 empreinte(s) enregistrée(s)"
}
```

### 3. Obtenir les empreintes d'un employé par employee_code
```
GET /employes/{employee_code}/empreintes
```
**Paramètres :**
- `employee_code` (string) : Le code employé

**Réponse :**
```json
{
  "empreinte_ids": [1, 2, 3]
}
```

### 4. Signaler présence
```
POST /employes/presences/signal
```
**Body :**
```json
{
  "employee_code": "1234"
}
```

**Réponse :**
```json
{
  "id": "uuid-de-la-presence",
  "employe_id": "uuid-de-l-employe",
  "employee_code": "1234",
  "date_presence": "2024-01-15",
  "heure_arrivee": "2024-01-15T08:30:00",
  "heure_depart": null,
  "type_presence": "entrée",
  "notes": null,
  "created_at": "2024-01-15T08:30:00"
}
```

**Note :** La date, l'heure d'arrivée et le type de présence sont automatiquement générés au moment du signalement.

### 5. Obtenir toutes les présences d'un employé
```
GET /employes/{employee_code}/presences
```
**Paramètres :**
- `employee_code` (string) : Le code employé

**Réponse :**
```json
[
  {
    "id": "uuid-de-la-presence",
    "employe_id": "uuid-de-l-employe",
    "employee_code": "EMP001",
    "date_presence": "2024-01-15",
    "heure_arrivee": "2024-01-15T08:00:00",
    "heure_depart": "2024-01-15T17:00:00",
    "type_presence": "entrée",
    "notes": "Présence normale",
    "created_at": "2024-01-15T08:00:00"
  }
]
```

## Routes existantes conservées

- `POST /employes/` - Créer un employé (génère automatiquement un employee_code à 4 chiffres)
- `GET /employes/` - Obtenir tous les employés
- `GET /employes/verify-code/{code_unique}` - Vérifier un code unique

## Nouvelles routes ajoutées

### 6. Modifier l'employee_code d'un employé
```
PUT /employes/{user_id}/employee-code
```
**Paramètres :**
- `user_id` (string) : L'ID UUID de l'utilisateur

**Body :**
```json
{
  "employee_code": "1234"
}
```

**Réponse :**
```json
{
  "message": "Code employé mis à jour avec succès: 1234"
}
```

### 7. Signaler la sortie d'un employé
```
PUT /employes/presences/{presence_id}/sortie
```
**Paramètres :**
- `presence_id` (string) : L'ID UUID de la présence

**Réponse :**
```json
{
  "message": "Sortie signalée avec succès",
  "heure_depart": "2024-01-15T17:30:00"
}
```

### 8. Modifier le type de présence
```
PUT /employes/presences/{presence_id}/type?type_presence=pause
```
**Paramètres :**
- `presence_id` (string) : L'ID UUID de la présence
- `type_presence` (string) : Type de présence ("entrée", "sortie", "pause", "reprise")

**Réponse :**
```json
{
  "message": "Type de présence mis à jour: pause"
}
```

### 9. Ajouter des notes à une présence
```
PUT /employes/presences/{presence_id}/notes?notes=Présence exceptionnelle
```
**Paramètres :**
- `presence_id` (string) : L'ID UUID de la présence
- `notes` (string) : Notes à ajouter

**Réponse :**
```json
{
  "message": "Notes ajoutées avec succès"
}
```

## Structure de la base de données

### Table `employes`
- `id` (UUID, Primary Key)
- `employee_code` (String, Unique)
- `code_unique` (String, Unique)
- `full_name` (String)
- `email` (String, Unique)
- ... autres champs

### Table `empreintes`
- `id` (UUID, Primary Key)
- `employe_id` (UUID, Foreign Key vers employes.id)
- `empreinte_id` (Integer) - Les IDs d'empreintes (1, 2, 3, etc.)
- `created_at` (DateTime)

### Table `presences`
- `id` (UUID, Primary Key)
- `employe_id` (UUID, Foreign Key vers employes.id)
- `employee_code` (String)
- `date_presence` (Date)
- `heure_arrivee` (DateTime)
- `heure_depart` (DateTime, nullable)
- `type_presence` (String) - "entrée", "sortie", "pause"
- `notes` (Text, nullable)
- `created_at` (DateTime) 