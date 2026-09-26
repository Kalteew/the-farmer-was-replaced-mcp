# État actuel

Dernière mise à jour : 2026-09-25

## Partie

- Sauvegarde active : `Save3`
- Phase : recherche et préparation, aucune progression volontaire depuis le début de cette phase
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

1. Vérifier que le MCP est bien enregistré dans l'environnement de jeu.
2. Lire l'état réel avec `tfwr_get_state`.
3. Tester un run minimal borné adapté aux déblocages actuels.
4. Mesurer le premier déblocage utile avec `get_cost()` dès que disponible.
