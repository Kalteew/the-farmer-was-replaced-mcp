# État actuel

Dernière mise à jour : 2026-09-26

## Partie

- Sauvegarde active : `Save3`
- Phase : progression AFK active sur une ferme 12×12
- Ressources observées : `10 283 hay`, `50 615 wood`, `757 carrot`, `136 pumpkin`, `1 025 water`, `220 fertilizer`, `716 power`
- Déblocages observés : `Speed` niveau 5, `Expand` niveau 6, `Pumpkins` niveau 4, `Sunflowers`, `Watering` niveau 6, `Polyculture` 1, `Cactus` 1, `Fertilizer` niveau 4, `Timing`, `Auto_Unlock` et les primitives de navigation/scripting
- Script principal : `game/Save3/main.py`
- Boucle : bootstrap adaptatif (herbe + carottes + 10 tournesols), puis carré de citrouilles dynamique (`taille - 1`, actuellement 11×11), vitesse solaire, fertilisation ciblée de l'herbe et remplacement automatique des citrouilles mortes
- File Watcher : activé dans `options.txt`

## Infrastructure

- Pont MCP local présent dans `src/server.mjs`, avec achat direct de recherche et mesure bornée de productivité ; une mesure de 20 s a relevé environ `60` carottes/min et `257` foin/min, puis le script a été relancé et vérifié actif
- Outils disponibles : lecture disque, lecture live BepInEx, chargement de sauvegarde, exécution de script, capture d'écran, documentation et recettes
- API BepInEx locale installée : état, inventaire, déblocages, catalogue, grille, exécution/arrêt et achat de recherche
- Vérification du chemin MCP effectuée avec `npm run inspect`
- Documentation locale et snapshot de l'API présents dans `docs/`

## À faire ensuite

1. Laisser le bootstrap/carré adaptatif maintenir les graines et les méga-récoltes.
2. Accumuler la substance étrange avec l'herbe fertilisée, puis ouvrir les labyrinthes et l'or.
3. Acheter `Utilities` dès que les `1 000` citrouilles sont disponibles, puis `Expand 7` à `64 000` citrouilles.

Note : le parcours fiable exploite le wrap horizontal et vertical ; il parcourt chaque case exactement une fois et revient au point de départ.
