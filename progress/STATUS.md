# État actuel

Dernière mise à jour : 2026-09-27

## Partie

- Sauvegarde active : `Solo + AI`
- Phase : chaîne carottes → variables → fonctions → import terminée sur une ferme 1×3
- Ressources observées avant l'achat final : `84 carrots`, `98 wood`, `168 hay`
- Déblocages obtenus : `operators`, `carrots`, `variables`, `functions`, `import`
- Script principal : `Saves/Solo + AI/main.py`
- Boucle finale : deux cases de carottes et un buisson entretenus en continu
- Vérification live : `import` présent dans l'arbre des déblocages, sortie vide ; exécution arrêtée puis partie sauvegardée
- File Watcher : activé dans `options.txt`

## Infrastructure

- Pont MCP local présent dans `src/server.mjs`, avec achat direct de recherche et mesure bornée de productivité ; une mesure de 20 s a relevé environ `60` carottes/min et `257` foin/min, puis le script a été relancé et vérifié actif
- Outils disponibles : lecture disque, lecture live BepInEx, chargement de sauvegarde, exécution de script, capture d'écran, documentation et recettes
- API BepInEx locale installée : état, inventaire, déblocages, catalogue, grille, exécution/arrêt et achat de recherche
- Vérification du chemin MCP effectuée avec `npm run inspect`
- Documentation locale et snapshot de l'API présents dans `docs/`

## À faire ensuite

1. Utiliser `import` dans le prochain script guidé.
2. Étendre la ferme et produire davantage de carottes si nécessaire.

Note : le parcours fiable exploite le wrap horizontal et vertical ; il parcourt chaque case exactement une fois et revient au point de départ.
