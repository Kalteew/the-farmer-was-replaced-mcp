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

Date : 2026-09-26 10:45
Sauvegarde : Save3
Objectif : fiabiliser la navigation et rendre les achats de recherche pilotables par MCP.
Script : game/Save3/main.py
Action : ajout de `tfwr_unlock`, arrêt direct du script, puis ajout de `tfwr_measure_run`. Validation d'un balayage torique 3×3 avec `for`, `range`, `get_world_size()` et retour exact en `(0,0)`.
Résultat observé : achats réussis de `Loops`, `Speed`, `Plant`, `Expand` niveau 2, `Carrots`, `Operators`, `Senses` et `Variables`. Le balayage de neuf cases a produit les ressources attendues sans mouvements de correction aux bords.
Progression : arbre de recherche autonome et navigation déterministe validés.
Blocage ou risque : `tfwr_measure_run` sera visible après rechargement du serveur MCP ; la ferme doit conserver une case d'herbe pour financer le foin des carottes.
Prochaine étape : mesurer une passe bornée, puis acheter `Functions` à 40 carottes.

Date : 2026-09-26 11:10
Sauvegarde : Save3
Objectif : valider la productivité et la navigation après correction du wrap.
Script : game/Save3/main.py
Action : ferme reconstruite avec 1 case d'herbe, 5 carottes et 3 buissons ; balayage avec `size = get_world_size()` et double boucle torique. Ajout puis test du MCP `tfwr_measure_run`.
Résultat observé : mesure de 12 secondes à `9/9` cases couvertes, `4` wraps détectés, `+9` carottes et `+2` bois nets, productivité de `44,83` carottes/minute et `9,96` bois/minute.
Progression : navigation déterministe et mesure de productivité validées ; `Functions` et `Speed` niveau 2 achetés via le pont.
Blocage ou risque : les ressources de plantation peuvent temporairement vider le foin et laisser des cases de sol vides ; la case d'herbe réservée rétablit le foin au passage suivant.
Prochaine étape : remonter le bois et les carottes, puis viser `Expand` niveau 3 et `Trees`.

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
