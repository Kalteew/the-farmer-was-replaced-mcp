---
name: tfwr-research
description: Rechercher et consolider les mécaniques, l'API, les déblocages et les stratégies de The Farmer Was Replaced dans les fichiers locaux du projet, sans jouer ni modifier la sauvegarde.
---

# Recherche locale du jeu

Ce skill sert à apprendre le jeu avant de lancer une progression.

## Sources

Privilégier dans cet ordre :

1. `docs/source_snapshot/fr/docs/` et `docs/source_snapshot/fr/Strings/` ;
2. `docs/source_snapshot/api/builtins.py` ;
3. `docs/LOCAL_KNOWLEDGE.md` et l'état de sauvegarde lu en lecture seule ;
4. wiki ou notes officielles pour compléter les trous, en indiquant la source et la date.

Les guides communautaires anciens peuvent viser une version antérieure. Ne pas les utiliser pour corriger une information locale sans signaler le conflit.

## Mise à jour de la base

Pour chaque découverte utile :

- ajouter la règle ou le comportement dans `docs/LOCAL_KNOWLEDGE.md` ;
- conserver le détail ou la doc originale dans `docs/source_snapshot/` ;
- noter les contradictions dans une section « à vérifier » ;
- ne pas inventer les coûts : utiliser `get_cost()` quand le jeu est disponible ;
- distinguer comportement documenté, observation réelle et hypothèse.

La recherche ne doit pas écrire dans `Saves/SaveN`, modifier le code du jeu, ni lancer de script de gameplay.
