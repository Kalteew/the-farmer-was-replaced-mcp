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

## 2026-09-26 — progression AFK

- Ajout d'une boucle `while True` sûre pour la ferme AFK, avec couverture torique complète.
- Corrigé la détection après récolte : l'herbe reste une entité `Grass`, donc le script suit désormais le flag de récolte pour replanter.
- Débloqué `Expand` niveau 3 puis `Trees`, `Speed` niveau 3 et `Watering` niveaux 1 à 3 via MCP.
- Débloqué `Expand` niveau 4 : la grille active est passée à `6×6`.
- Motif d'arbres espacé selon la parité pour les tailles paires, et motif sans collision de bord pour les tailles impaires.
- Rendement observé en AFK : `1 569` bois et `110` carottes avant la tentative d'Expand 5 ; `Speed` 4 et `Expand` 5 restent hors budget.
- La méga-ferme de citrouilles a produit `216` citrouilles par récolte et permis `Expand` niveau 5.
- La grille est passée à `8×8` ; le script a été reconverti en ferme mixte de récupération.
- Optimisation du débit : `8` cases de foin, `15` parcelles de carottes et parité torique pour les arbres.
- Débloqué `Watering` niveau 4 et `Pumpkins` niveau 1 ; le stock observé a atteint `5 150` bois, `153` carottes et `158` foin.
