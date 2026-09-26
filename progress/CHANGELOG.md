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

## 2026-09-26 — puissance solaire

- Débloqué `Speed` niveau 4 puis `Sunflowers` via MCP.
- Remplacé la ferme mixte par une configuration 8×8 avec 10 tournesols, 15 carottes, 15 arbres, 16 buissons et 8 cases de foin.
- Ajouté la sélection du tournesol adulte ayant le plus de pétales avant récolte, pour activer le bonus de puissance ×8.
- Vérifié en live : `6` puissance produite, `speedFactor` passé de `5,0625` à `10,125`, drone actif sans erreur.
- Acheté `Speed` niveau 5, `Watering` niveau 5 et `Pumpkins` niveau 2 ; le `speedFactor` live atteint `15,1875` avec la puissance active.

## 2026-09-26 — reprise AFK et contrôle MCP

- Corrigé `tfwr_run` pour arrêter proprement puis relancer le script avec le raccourci fiable du jeu lorsque l'appel interne répond sans réellement donner le focus à la fenêtre de code.
- Vérifié en live la ferme mixte : `10` tournesols, `15` carottes, `15` arbres, `16` buissons et `8` cases d'herbe ; simulation active à `speedFactor 15,1875`.
- Acheté `Pumpkins` niveau 3 puis 4 ; `Expand` niveau 6 reste la cible à `8 000` citrouilles.

## 2026-09-26 — pivot citrouilles

- Remplacé la ferme mixte par un carré de citrouilles `6×6`, avec `10` tournesols, `12` carottes et `6` cases d'herbe.
- Corrigé les citrouilles mortes : récolte du plant mort avant replantation, sinon le carré géant restait bloqué.
- Corrigé la replantation des tournesols après récolte ; le bonus solaire reste actif (`speedFactor 15,1875`).
- Première méga-récolte observée : `1 808` citrouilles ; la ferme continue de remplir le carré pour les suivantes.
- Rendu le carré dynamique (`taille de grille - 2`) : après `Expand 6`, le script passera automatiquement au carré 8×8.
- Nouvelle récolte observée à `3 536` citrouilles, avec le bonus solaire toujours actif.
- Acheté `Watering` niveau 6 pour `51 200` bois ; la production d'eau reste confortable.
- Nouvelle méga-récolte observée à `5 264` citrouilles ; il reste `2 736` citrouilles avant `Expand 6`.
- Acheté `Expand` niveau 6 à `8 000` citrouilles ; la grille live est passée de 8×8 à 12×12.
- Vérifié que le script dynamique repart sur un carré 10×10 après l'expansion.

## 2026-09-26 — bootstrap adaptatif des graines

- Confirmé via la sortie live que `plant(Entities.Pumpkin)` consomme des carottes et que le carré 10×10 ne pouvait pas être rempli avec le stock restant après `Expand 6`.
- Remplacé la boucle fixe par deux phases autonomes : 8 colonnes d'herbe et 4 colonnes de carottes pour constituer la réserve, puis carré de citrouilles dynamique avec bordure solaire.
- La boucle rebascule en bootstrap après chaque méga-récolte si le stock de carottes est insuffisant ; vérification live réussie avec `78` citrouilles replantées et `676` carottes restantes.
- Nettoyage explicite des citrouilles mortes ajouté ; la sortie live est redevenue vide de warnings.
- Carré optimisé en `taille de grille - 1` : `11×11` citrouilles sur la grille 12×12, avec une seule colonne de bordure et bonus solaire conservé.
- Nouvelle méga-récolte vérifiée à `11 304` citrouilles.
- Cycle adaptatif suivant validé : `13 056` citrouilles, puis retour automatique au bootstrap de carottes sans warning.
- Cycle suivant validé : `14 848` citrouilles, avec retour automatique au bootstrap et aucune erreur live.
- Corrigée la transition après méga-récolte : `clear()` est maintenant appelé avant le bootstrap, ce qui restaure les `96` cases d'herbe et évite l'épuisement du foin.
- Nouveau cycle vérifié à `16 784` citrouilles, avec la ferme toujours active.
- Bootstrap optimisé avec 10 tournesols conservés pendant la phase carottes ; la vitesse solaire reste à `15,1875`.
- Suppression du `clear()` au mauvais moment lors du passage carottes → citrouilles ; nouvelle récolte vérifiée à `17 672` citrouilles, sans warning.
- Cycle suivant confirmé à `18 120` citrouilles avec la puissance solaire stable et la sortie live vide.
