---
name: tfwr-progress
description: "Maintenir le suivi local de The Farmer Was Replaced : état courant, progression, décisions, résultats des runs et prochaines étapes. À utiliser après toute action de recherche, d'écriture de code ou d'exécution dans le jeu."
---

# Suivi de progression

Le dossier `progress/` est la mémoire de travail locale du projet.

## Fichiers à maintenir

- `STATUS.md` : vérité courte et actuelle ; le lire en premier.
- `ROADMAP.md` : objectifs ordonnés et critères de réussite.
- `CHANGELOG.md` : historique chronologique concis.
- `SESSION_LOG.md` : détail des runs, scripts, sorties et erreurs.

## Après chaque changement significatif

Mettre à jour la sauvegarde concernée, le script modifié, l'état observé, le résultat réel et la prochaine action la plus utile.

Ne jamais présenter une hypothèse comme une progression acquise. Si l'état n'est pas disponible, écrire `à vérifier via tfwr_get_state`.

## Format d'une entrée de session

```text
Date : YYYY-MM-DD HH:mm
Sauvegarde : SaveN
Objectif : ...
Script : ...
Action : ...
Résultat observé : ...
Progression : ...
Blocage ou risque : ...
Prochaine étape : ...
```

Garder `STATUS.md` court ; déplacer les détails dans `SESSION_LOG.md`.
