# Historique

## 2026-09-25

- Mise en place du projet local The Farmer Was Replaced.
- Ajout du pont MCP local pour lire l'état, écrire les scripts et contrôler l'exécution.
- Archivage de la documentation française et de l'API embarquées dans l'installation Steam.
- Création des skills locaux `tfwr-play`, `tfwr-research` et `tfwr-progress`.
- Création de la feuille de route et du journal de progression.
- Aucun run de gameplay effectué pendant la phase de préparation.

## 2026-09-26

- Jeu relancé avec le pont BepInEx actif sur `Save3`.
- Exécuté un run borné de deux `harvest()` : inventaire confirmé à 5 foin.
- Testé `unlock(Unlocks.Loops)` ; refus attendu car `Auto_Unlock` n'est pas débloqué.
- Script principal remis dans un état valide avec une récolte simple.
- Ajout de `tfwr_unlock` et de l'arrêt direct via le pont BepInEx.
- Débloqué `Loops`, `Speed`, `Plant`, `Expand` niveau 2, `Carrots`, `Operators`, `Senses` et `Variables`.
- Ajout de `tfwr_measure_run` pour mesurer inventaire, productivité, couverture, déplacements et wraps.
- Corrigé le parcours de grille : le terrain est torique sur les axes vertical et horizontal.
- Débloqué `Variables`, `Functions` et `Speed` niveau 2.
- Mesure complète validée : couverture `9/9`, `4` wraps détectés, `+9` carottes et `+2` bois nets sur 12 secondes.
