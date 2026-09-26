# État actuel

Dernière mise à jour : 2026-09-26

## Partie

- Sauvegarde active : `Save3`
- Phase : progression AFK active sur une ferme 12×12
- Ressources observées : `5 068 hay`, `123 412 wood`, `703 carrot`, `17 672 pumpkin`, `1 272 water`, `99 power`
- Déblocages observés : `Speed` niveau 5, `Expand` niveau 6, `Pumpkins` niveau 4, `Sunflowers`, `Watering` niveau 6, et les primitives de navigation/scripting
- Script principal : `game/Save3/main.py`
- Boucle : bootstrap adaptatif (herbe + carottes + 10 tournesols), puis carré de citrouilles dynamique (`taille - 1`, actuellement 11×11), vitesse solaire et remplacement automatique des citrouilles mortes
- File Watcher : activé dans `options.txt`

## Infrastructure

- Pont MCP local présent dans `src/server.mjs`, avec achat direct de recherche et mesure bornée de productivité
- Outils disponibles : lecture disque, lecture live BepInEx, chargement de sauvegarde, exécution de script, capture d'écran, documentation et recettes
- API BepInEx locale installée : état, inventaire, déblocages, catalogue, grille, exécution/arrêt et achat de recherche
- Vérification du chemin MCP effectuée avec `npm run inspect`
- Documentation locale et snapshot de l'API présents dans `docs/`

## À faire ensuite

1. Laisser le bootstrap/carré adaptatif maintenir les graines et les méga-récoltes.
2. Lire le prochain coût réel d'expansion et acheter `Expand 7` dès que le stock le permet.
3. Accumuler `64 000` citrouilles pour `Expand 7`.

Note : le parcours fiable exploite le wrap horizontal et vertical ; il parcourt chaque case exactement une fois et revient au point de départ.
