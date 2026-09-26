# État actuel

Dernière mise à jour : 2026-09-26

## Partie

- Sauvegarde active : `Save3`
- Phase : progression AFK active sur une ferme 6×6
- Ressources observées avant le dernier run : `73 hay`, `769 wood`, `110 carrot`, `3 water`
- Déblocages observés : `Loops`, `Speed` niveau 3, `Plant`, `Expand` niveau 4, `Carrots`, `Trees`, `Watering` niveau 3, `Operators`, `Senses`, `Variables`, `Functions`
- Script principal : `game/Save3/main.py`
- Boucle : réserve de foin, carottes, arbres espacés, buissons de remplissage, arrosage sous 50 %
- File Watcher : activé dans `options.txt`

## Infrastructure

- Pont MCP local présent dans `src/server.mjs`, avec achat direct de recherche et mesure bornée de productivité
- Outils disponibles : lecture disque, lecture live BepInEx, chargement de sauvegarde, exécution de script, capture d'écran, documentation et recettes
- API BepInEx locale installée : état, inventaire, déblocages, catalogue, grille, exécution/arrêt et achat de recherche
- Vérification du chemin MCP effectuée avec `npm run inspect`
- Documentation locale et snapshot de l'API présents dans `docs/`

## À faire ensuite

1. Laisser tourner l'AFK pour financer `Speed` niveau 4 et `Expand` niveau 5.
2. Adapter le motif d'arbres si une prochaine expansion donne une taille impaire.
3. Continuer les achats via `tfwr_unlock` après lecture de l'état live.

Note : le parcours fiable exploite le wrap horizontal et vertical ; il parcourt chaque case exactement une fois et revient au point de départ.
