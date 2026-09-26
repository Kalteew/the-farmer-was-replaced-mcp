# Journal des sessions

Les entrées détaillées commencent ici. Utiliser le format défini dans `skills/tfwr-progress/SKILL.md`.

Date : 2026-09-26 10:12
Sauvegarde : Save3
Objectif : lancer la partie et préparer le premier déblocage.
Script : game/Save3/main.py
Action : run initial, puis deux récoltes bornées ; test de `unlock(Unlocks.Loops)`.
Résultat observé : pont BepInEx actif, exécution sans erreur pour les récoltes, inventaire à 5 foin. Le déblocage scripté est refusé tant que `Auto_Unlock` n'est pas acquis.
Progression : première étape de gameplay validée.
Blocage ou risque : achat initial de `Loops` à faire dans l'interface de recherche.
Prochaine étape : débloquer `Loops`, puis remplacer la récolte bornée par une boucle contrôlée.

## Modèle

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
