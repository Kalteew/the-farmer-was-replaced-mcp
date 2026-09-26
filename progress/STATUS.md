# État actuel

Dernière mise à jour : 2026-09-26

## Partie

- Sauvegarde active : `Save3`
- Phase : progression AFK active sur une ferme 12×12
- Ressources observées : `19 087 hay`, `52 326 wood`, `1 121 carrot`, `328 pumpkin`, `1 907 weird_substance`, `2 176 gold`, `1 000 water`, `1 104 fertilizer`, `419 power`
- Déblocages observés : `Speed` niveau 5, `Expand` niveau 6, `Pumpkins` niveau 4, `Sunflowers`, `Watering` niveau 6, `Polyculture` 1, `Cactus` 1, `Fertilizer` niveau 4, `Timing`, `Utilities`, `Mazes` 1, `Megafarm` 1, `Auto_Unlock` et les primitives de navigation/scripting
- Script principal : `game/Save3/main.py`
- Boucle : bootstrap adaptatif (herbe + carottes + 18 arbres espacés + 10 tournesols), puis carré de citrouilles dynamique (`taille - 1`, actuellement 11×11), boucle de labyrinthes et remplacement automatique des citrouilles mortes
- Parallélisme : `Megafarm` niveau 1 est utilisé pour confier les arbres fertilisés à un second drone pendant le bootstrap
- File Watcher : activé dans `options.txt`

## Infrastructure

- Pont MCP local présent dans `src/server.mjs`, avec achat direct de recherche et mesure bornée de productivité ; une mesure de 20 s a relevé environ `60` carottes/min et `257` foin/min, puis le script a été relancé et vérifié actif
- Outils disponibles : lecture disque, lecture live BepInEx, chargement de sauvegarde, exécution de script, capture d'écran, documentation et recettes
- API BepInEx locale installée : état, inventaire, déblocages, catalogue, grille, exécution/arrêt et achat de recherche
- Vérification du chemin MCP effectuée avec `npm run inspect`
- Documentation locale et snapshot de l'API présents dans `docs/`

## À faire ensuite

1. Laisser la ferme et les labyrinthes produire l’or jusqu’à `Simulation` (`5 000`) puis `Megafarm` 2 (`8 000`).
2. Accumuler `20 000` citrouilles pour `Cactus` 2, puis produire les `12 000` cactus nécessaires à `Mazes` 2.
3. Reconfigurer ensuite le champ en cactus triés, puis viser `Expand 7` à `64 000` citrouilles et `Pumpkins 5` à `64 000` carottes.

Note : le parcours fiable exploite le wrap horizontal et vertical ; il parcourt chaque case exactement une fois et revient au point de départ.
