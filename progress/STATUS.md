# État actuel

Dernière mise à jour : 2026-09-26

## Partie

- Sauvegarde active : `Save3`
- Phase : progression AFK active sur une ferme 8×8
- Ressources observées : `1 017 hay`, `191 535 wood`, `10 carrot`, `1 808 pumpkin`, `860 water`, `582 power`
- Déblocages observés : `Speed` niveau 5, `Expand` niveau 5, `Pumpkins` niveau 4, `Sunflowers`, `Watering` niveau 5, et les primitives de navigation/scripting
- Script principal : `game/Save3/main.py`
- Boucle : carré de citrouilles 6×6, 10 tournesols, 12 parcelles de carottes, 6 cases d'herbe, arrosage sous 50 % et remplacement automatique des citrouilles mortes
- File Watcher : activé dans `options.txt`

## Infrastructure

- Pont MCP local présent dans `src/server.mjs`, avec achat direct de recherche et mesure bornée de productivité
- Outils disponibles : lecture disque, lecture live BepInEx, chargement de sauvegarde, exécution de script, capture d'écran, documentation et recettes
- API BepInEx locale installée : état, inventaire, déblocages, catalogue, grille, exécution/arrêt et achat de recherche
- Vérification du chemin MCP effectuée avec `npm run inspect`
- Documentation locale et snapshot de l'API présents dans `docs/`

## À faire ensuite

1. Laisser la puissance solaire accélérer le carré et reconstituer les graines.
2. Accumuler les méga-récoltes de citrouilles pour financer `Expand` niveau 6.
3. Accumuler `8 000` citrouilles pour l'expansion suivante.

Note : le parcours fiable exploite le wrap horizontal et vertical ; il parcourt chaque case exactement une fois et revient au point de départ.
