# État actuel

Dernière mise à jour : 2026-09-26

## Partie

- Sauvegarde active : `Save3`
- Phase : progression active avec ferme 3×3 contrôlée
- Ressources observées : `1 hay`, `7 wood`, `39 carrot`
- Déblocages observés : `Loops`, `Speed` niveau 2, `Plant`, `Expand` niveau 2, `Carrots`, `Operators`, `Senses`, `Variables`, `Functions`
- Script principal : `game/Save3/main.py`
- File Watcher : activé dans `options.txt`

## Infrastructure

- Pont MCP local présent dans `src/server.mjs`, avec achat direct de recherche et mesure bornée de productivité
- Outils disponibles : lecture disque, lecture live BepInEx, chargement de sauvegarde, exécution de script, capture d'écran, documentation et recettes
- API BepInEx locale installée : état, inventaire, déblocages, catalogue, grille, exécution/arrêt et achat de recherche
- Vérification du chemin MCP effectuée avec `npm run inspect`
- Documentation locale et snapshot de l'API présents dans `docs/`

## À faire ensuite

1. Utiliser `tfwr_measure_run` dans le serveur MCP rechargé.
2. Remonter le bois pour `Expand` niveau 3 et les carottes pour `Trees`.
3. Stabiliser la ferme mixte avec une case d'herbe réservée au foin.

Note : le parcours fiable exploite le wrap horizontal et vertical ; il parcourt chaque case exactement une fois et revient au point de départ.
