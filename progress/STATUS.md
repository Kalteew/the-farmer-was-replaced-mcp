# État actuel

Dernière mise à jour : 2026-09-27

## Partie

- Sauvegarde active : `Solo + AI`
- Phase : première boucle de récolte sur une ferme 1×3
- Ressource observée : `60 hay` après lancement, contre `32` au départ
- Déblocages observés : boucles, conditions, `can_harvest`, mouvement et directions nord/sud/est/ouest
- Script principal : `Saves/Solo + AI/main.py`
- Boucle : `can_harvest()` → `harvest()` → `move(North)`, répétée avec `while True`
- Vérification live : le drone est passé en `y=1`, état `moving`, sans erreur de sortie
- File Watcher : activé dans `options.txt`

## Infrastructure

- Pont MCP local présent dans `src/server.mjs`, avec achat direct de recherche et mesure bornée de productivité ; une mesure de 20 s a relevé environ `60` carottes/min et `257` foin/min, puis le script a été relancé et vérifié actif
- Outils disponibles : lecture disque, lecture live BepInEx, chargement de sauvegarde, exécution de script, capture d'écran, documentation et recettes
- API BepInEx locale installée : état, inventaire, déblocages, catalogue, grille, exécution/arrêt et achat de recherche
- Vérification du chemin MCP effectuée avec `npm run inspect`
- Documentation locale et snapshot de l'API présents dans `docs/`

## À faire ensuite

1. Laisser la ferme et les labyrinthes produire l’or jusqu’à `Megafarm` 2 (`8 000`).
2. Accumuler `20 000` citrouilles pour `Cactus` 2, puis produire les `12 000` cactus nécessaires à `Mazes` 2.
3. Reconfigurer ensuite le champ en cactus triés, puis viser `Expand 7` à `64 000` citrouilles et `Pumpkins 5` à `64 000` carottes.

Note : le parcours fiable exploite le wrap horizontal et vertical ; il parcourt chaque case exactement une fois et revient au point de départ.
