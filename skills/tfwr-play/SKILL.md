---
name: tfwr-play
description: Jouer à The Farmer Was Replaced depuis le projet en utilisant le pont MCP local, les scripts de sauvegarde et la connaissance versionnée du jeu. À utiliser pour lire l'état, écrire du code, l'exécuter, diagnostiquer une erreur ou planifier la prochaine progression.
---

# Jouer à The Farmer Was Replaced

Ce skill est local au projet. Il suppose que le serveur MCP du projet expose les outils `tfwr_*`.

## Avant d'agir

Lire `progress/STATUS.md`, `docs/LOCAL_KNOWLEDGE.md`, puis la référence ciblée dans `docs/source_snapshot/` si nécessaire.

Toujours appeler `tfwr_get_state` avant de modifier ou d'exécuter un script. Ne jamais déduire les déblocages, scripts ou coûts à partir d'une ancienne observation.

## Boucle de jeu contrôlée

1. Observer l'état réel avec `tfwr_get_state`.
2. Choisir une tâche courte et vérifiable, adaptée aux déblocages disponibles.
3. Écrire le script avec `tfwr_write_script` ; le MCP crée une sauvegarde avant remplacement.
4. Exécuter avec `tfwr_run`.
5. Lire `tfwr_get_output`, puis relire `tfwr_get_state`.
6. Arrêter avec `tfwr_stop` si le script boucle mal, consomme une ressource inattendue ou produit une erreur.
7. Mettre à jour `progress/STATUS.md`, `progress/CHANGELOG.md` et `progress/SESSION_LOG.md`.

Privilégier des runs bornés et observables. Utiliser `simulate()` seulement lorsqu'il est débloqué et pour comparer des variantes sans modifier la ferme réelle.

## Stratégie de progression

- Début : produire le foin nécessaire aux premiers déblocages.
- Ensuite : débloquer les boucles, les conditions, le mouvement et les sens.
- Construire un balayage de grille robuste avant de spécialiser les cultures.
- Utiliser `get_cost()` et `num_unlocked()` pour choisir dynamiquement le prochain déblocage.
- Ajouter eau, vitesse et tournesols avant les optimisations coûteuses.
- Traiter citrouilles, polyculture, cactus, labyrinthes et dinosaures dans des scripts séparés.
- Ne passer aux drones multiples qu'après une tâche mono-drone fiable.

## Contraintes

- Ne pas utiliser la souris si le MCP suffit.
- Ne pas lancer un `while True` non testé sur la ferme réelle.
- Ne pas appeler `clear()` ou `set_world_size()` sur la vraie ferme sans demande explicite et sauvegarde vérifiée.
- Ne jamais supprimer une sauvegarde ou désactiver Steam Cloud sans confirmation explicite.
- Marquer toute information contradictoire ou non vérifiée comme telle dans `docs/LOCAL_KNOWLEDGE.md`.
