# État actuel

Dernière mise à jour : 2026-09-26

## Partie

- Sauvegarde active : `Save3`
- Phase : prise en main contrôlée ; premier run réussi
- Ressources observées : `5 hay`
- Déblocages observés : `grass`, `soil`, `harvest`, `pass`, `do_a_flip`, `pet_the_piggy`, `grassland`, `hay`, `straw_hat`, `tap`
- Script principal : `game/Save3/main.py`
- File Watcher : activé dans `options.txt`

## Infrastructure

- Pont MCP local présent dans `src/server.mjs`
- Outils disponibles : lecture disque, lecture live BepInEx, chargement de sauvegarde, exécution de script, capture d'écran, documentation et recettes
- API BepInEx locale installée : état, inventaire, déblocages, catalogue, grille et actions de base
- Vérification du chemin MCP effectuée avec `npm run inspect`
- Documentation locale et snapshot de l'API présents dans `docs/`

## À faire ensuite

1. Débloquer `Loops` dans l'arbre de recherche du jeu.
2. Reprendre une récolte bornée avec une boucle `while`.
3. Mesurer le prochain déblocage avec `get_cost()` dès que disponible.

Note : `unlock(Unlocks.Loops)` a été refusé car `Unlocks.Auto_Unlock` n'est pas encore débloqué ; l'achat initial doit passer par l'interface de recherche.
