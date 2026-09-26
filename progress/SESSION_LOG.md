# Journal des sessions

Les entrées détaillées commencent ici. Utiliser le format défini dans `skills/tfwr-progress/SKILL.md`.

Date : 2026-09-26 10:12
Sauvegarde : Save3
Objectif : lancer la partie et préparer le premier déblocage.
Script : game/Save3/main.py
Action : run initial, puis deux récoltes bornées ; test de `unlock(Unlocks.Loops)`.
Résultat observé : pont BepInEx actif, exécution sans erreur pour les récoltes, inventaire à 5 foin. Le déblocage scripté est refusé tant que `Auto_Unlock` n'est pas acquis.
Progression : première étape de gameplay validée.
Blocage ou risque : achat initial de `Loops` à faire dans l'interface de recherche.
Prochaine étape : débloquer `Loops`, puis remplacer la récolte bornée par une boucle contrôlée.

Date : 2026-09-26 10:45
Sauvegarde : Save3
Objectif : fiabiliser la navigation et rendre les achats de recherche pilotables par MCP.
Script : game/Save3/main.py
Action : ajout de `tfwr_unlock`, arrêt direct du script, puis ajout de `tfwr_measure_run`. Validation d'un balayage torique 3×3 avec `for`, `range`, `get_world_size()` et retour exact en `(0,0)`.
Résultat observé : achats réussis de `Loops`, `Speed`, `Plant`, `Expand` niveau 2, `Carrots`, `Operators`, `Senses` et `Variables`. Le balayage de neuf cases a produit les ressources attendues sans mouvements de correction aux bords.
Progression : arbre de recherche autonome et navigation déterministe validés.
Blocage ou risque : `tfwr_measure_run` sera visible après rechargement du serveur MCP ; la ferme doit conserver une case d'herbe pour financer le foin des carottes.
Prochaine étape : mesurer une passe bornée, puis acheter `Functions` à 40 carottes.

Date : 2026-09-26 11:10
Sauvegarde : Save3
Objectif : valider la productivité et la navigation après correction du wrap.
Script : game/Save3/main.py
Action : ferme reconstruite avec 1 case d'herbe, 5 carottes et 3 buissons ; balayage avec `size = get_world_size()` et double boucle torique. Ajout puis test du MCP `tfwr_measure_run`.
Résultat observé : mesure de 12 secondes à `9/9` cases couvertes, `4` wraps détectés, `+9` carottes et `+2` bois nets, productivité de `44,83` carottes/minute et `9,96` bois/minute.
Progression : navigation déterministe et mesure de productivité validées ; `Functions` et `Speed` niveau 2 achetés via le pont.
Blocage ou risque : les ressources de plantation peuvent temporairement vider le foin et laisser des cases de sol vides ; la case d'herbe réservée rétablit le foin au passage suivant.
Prochaine étape : remonter le bois et les carottes, puis viser `Expand` niveau 3 et `Trees`.

Date : 2026-09-26 12:00
Sauvegarde : Save3
Objectif : passer d'un run borné à une ferme AFK autonome et progresser dans l'arbre.
Script : game/Save3/main.py
Action : boucle `while True`, réserve d'herbe, 5 parcelles carottes, arbres espacés, buissons de remplissage et arrosage automatique ; achats MCP de `Expand` 3-4, `Trees`, `Speed` 3 et `Watering` 1-3.
Résultat observé : couverture torique complète, grille 6×6, drone en `action`, aucun mouvement perdu ; rendement monté à `1 569` bois et `110` carottes avant `Expand` 5.
Progression : la ferme est désormais conçue pour tourner en AFK et financer les prochains paliers.
Blocage ou risque : `Expand` 5 et `Speed` 4 refusés faute de coût suffisant ; le motif impair doit rester surveillé après une future expansion.
Prochaine étape : laisser l'AFK produire, puis retenter les achats avec `tfwr_live_state` avant chaque action.

Date : 2026-09-26 13:00
Sauvegarde : Save3
Objectif : exploiter les citrouilles puis accélérer la récupération de carottes.
Script : game/Save3/main.py
Action : déblocage MCP de `Watering` 4, `Pumpkins` 1 et `Expand` 5 ; ferme citrouilles 6×6 avec récolte différée jusqu'à maturité complète ; retour en ferme mixte 8×8 avec 8 réserves de foin et 15 parcelles carottes.
Résultat observé : méga-récoltes de `216` citrouilles ; grille 8×8 stable avec arbres, buissons et carottes ; dernier état à `5 150` bois, `153` carottes et `158` foin, drone en `action`.
Progression : le débit carottes a été multiplié par environ trois par rapport au motif à 5 parcelles.
Blocage ou risque : `Speed` 4 et `Sunflowers` demandent `500` carottes ; la ferme mixte doit continuer à tourner.
Prochaine étape : laisser l'AFK atteindre `500` carottes, acheter `Speed` 4 puis `Sunflowers` via MCP.

Date : 2026-09-26 14:55
Sauvegarde : Save3
Objectif : exploiter le déblocage Sunflowers comme multiplicateur de productivité.
Script : game/Save3/main.py
Action : ajout de 10 parcelles de tournesols et d'une récolte différée du tournesol ayant le plus de pétales ; conservation des carottes, arbres, buissons et de la réserve de foin.
Résultat observé : après redémarrage propre, `10` tournesols présents, `6` puissance en inventaire, `speedFactor` doublé à `10,125`, drone en action.
Progression : la boucle AFK dispose maintenant du bonus de puissance solaire.
Blocage ou risque : l'eau reste un consommable limitant ; `Expand` niveau 6 demande `8 000` citrouilles.
Prochaine étape : acheter `Speed` niveau 5 et `Watering` niveau 5, puis lancer une ferme de citrouilles 8×8.

Date : 2026-09-26 15:00
Sauvegarde : Save3
Objectif : convertir le bonus solaire en progression d'arbre de recherche.
Script : game/Save3/main.py
Action : achats MCP de `Speed` niveau 5, `Watering` niveau 5 et `Pumpkins` niveau 2.
Résultat observé : `speedFactor` live à `15,1875` avec puissance active, drone en action, ressources suffisantes pour préparer le pivot citrouilles.
Progression : les trois améliorations rentables sont acquises ; `Expand` niveau 6 reste la prochaine cible à `8 000` citrouilles.
Blocage ou risque : le stock de citrouilles est encore à `80`, donc la ferme mixte doit être remplacée temporairement par un carré de citrouilles.
Prochaine étape : préparer puis lancer une ferme de citrouilles 8×8 sans perdre le contrôle du wrap torique.

Date : 2026-09-26
Sauvegarde : Save3
Objectif : maintenir la partie en AFK et fiabiliser les relances MCP.
Script : game/Save3/main.py
Action : rechargement de Save3, reprise contrôlée de la ferme mixte, correction de `tfwr_run`, puis achats MCP de `Pumpkins` niveaux 3 et 4.
Résultat observé : `10` tournesols, `15` carottes, `15` arbres, `16` buissons, `8` cases d'herbe ; `190 543` bois, `255` carottes, `80` citrouilles et `7,37` puissance ; simulation active à `speedFactor 15,1875`.
Progression : l'arbre est au niveau `Pumpkins 4`, la ferme tourne de nouveau sans erreur et `Expand 6` reste le prochain palier majeur.
Blocage ou risque : le stock de citrouilles doit remonter fortement ; le pivot 8×8 doit être validé avant de remplacer la ferme mixte.
Prochaine étape : tester puis lancer une boucle citrouilles robuste, accumuler `8 000` citrouilles et acheter `Expand 6`.

Date : 2026-09-26
Sauvegarde : Save3
Objectif : laisser tourner la ferme de citrouilles jusqu'à `Expand 6`.
Script : game/Save3/main.py
Action : carré 6×6 de citrouilles, replantation solaire, réserve de 6 cases d'herbe et correction des citrouilles mortes avant replantation.
Résultat observé : première méga-récolte à `1 808` citrouilles ; état live actif à `speedFactor 15,1875`, avec `10` tournesols, `26` citrouilles en croissance, `12` carottes et `6` herbes.
Progression : `Pumpkins` niveau 4 est acquis et l'automatisation AFK surveille désormais le prochain achat utile.
Blocage ou risque : les citrouilles mortes apparaissent aléatoirement et allongent certains cycles ; elles sont maintenant retirées automatiquement.
Prochaine étape : accumuler `8 000` citrouilles, acheter `Expand 6`, puis adapter le carré à la nouvelle taille.

Date : 2026-09-26
Sauvegarde : Save3
Objectif : préparer automatiquement la ferme à l'expansion suivante.
Script : game/Save3/main.py
Action : remplacement des coordonnées fixes par un carré de taille `get_world_size() - 2`, puis relance et vérification live.
Résultat observé : `3 536` citrouilles, `931` puissance, `speedFactor 15,1875`, drone actif et grille actuelle toujours saine.
Progression : la prochaine expansion ne nécessitera pas de réécriture du script ; la zone citrouilles passera de 6×6 à 8×8 automatiquement.
Blocage ou risque : le rythme dépend des cycles de croissance et des plants morts ; le script les remplace sans intervention.
Prochaine étape : atteindre `8 000` citrouilles et acheter `Expand 6` via l'automatisation.

Date : 2026-09-26
Sauvegarde : Save3
Objectif : financer l'expansion avec le carré AFK.
Script : game/Save3/main.py
Action : achat MCP de `Watering` niveau 6, puis surveillance de deux cycles de méga-récolte.
Résultat observé : `5 264` citrouilles, `1 261` eau, `1 696` puissance, drone actif ; il reste `2 736` citrouilles avant `Expand 6`.
Progression : le palier d'expansion est maintenant proche et l'automatisation peut l'acheter dès que le seuil est franchi.
Blocage ou risque : le cycle de croissance suivant peut varier selon les citrouilles mortes ; leur remplacement est automatique.
Prochaine étape : acheter `Expand 6`, puis vérifier le passage automatique du carré à 8×8.

Date : 2026-09-26
Sauvegarde : Save3
Objectif : franchir `Expand 6` et reprendre la production sur la nouvelle grille.
Script : game/Save3/main.py
Action : achat MCP de `Expand` niveau 6 après dépassement de `8 000` citrouilles, puis lecture live de la grille.
Résultat observé : grille `12×12`, stock restant de `720` citrouilles, `2 017` eau et `3 043` puissance ; le drone bouge et le script remplit le nouveau carré.
Progression : la ferme dynamique est maintenant dimensionnée en `10×10` citrouilles, avec tournesols, herbe et carottes sur la bordure.
Blocage ou risque : le premier cycle de croissance de la nouvelle zone est encore en cours ; aucun arrêt ni erreur observé.
Prochaine étape : attendre la première méga-récolte 10×10 et lire le prochain coût réel de l'arbre.

Date : 2026-09-26
Sauvegarde : Save3
Objectif : rendre la production de graines autonome après `Expand 6`.
Script : game/Save3/main.py
Action : diagnostic de la sortie live, bootstrap temporaire de carottes, puis remplacement par une boucle adaptative carottes/citrouilles.
Résultat observé : le bootstrap a produit plus de `1 400` carottes avec 8 colonnes d'herbe ; la boucle a ensuite replanté `78` citrouilles sur la grille 12×12, avec `676` carottes restantes et le drone actif.
Progression : le script sait maintenant financer les graines du carré 10×10 sans intervention manuelle après chaque méga-récolte.
Blocage ou risque : les citrouilles mortes et les coûts de plantation allongent le cycle ; le basculement automatique les absorbe.
Prochaine étape : laisser produire le carré 10×10, puis lire le coût réel d'`Expand 7` et l'acheter dès que possible.

Date : 2026-09-26
Sauvegarde : Save3
Objectif : maximiser le rendement du carré sur la grille 12×12.
Script : game/Save3/main.py
Action : nettoyage explicite des citrouilles mortes et réduction de la bordure à une colonne, soit un carré 11×11 ; relance et contrôle de la sortie live.
Résultat observé : nouvelle méga-récolte à `11 304` citrouilles, `1 416` puissance, drone actif et aucune sortie d'erreur.
Progression : le rendement par cycle est supérieur au carré 10×10 tout en conservant les 10 tournesols.
Blocage ou risque : le prochain Expand coûte `64 000` citrouilles ; le bootstrap de carottes reste nécessaire entre les récoltes.
Prochaine étape : poursuivre les cycles adaptatifs jusqu'à `Expand 7`.

Date : 2026-09-26
Sauvegarde : Save3
Objectif : poursuivre l'accumulation vers `Expand 7`.
Script : game/Save3/main.py
Action : vérification d'un cycle complet carré → méga-récolte → bootstrap de graines.
Résultat observé : stock monté à `13 056` citrouilles ; aucune sortie d'erreur, drone actif et bascule carottes automatique.
Progression : la ferme poursuit seule les cycles nécessaires vers `64 000` citrouilles.
Blocage ou risque : aucun achat disponible pour le moment ; `Pumpkins` et `Expand` coûtent chacun `64 000` dans le catalogue live.
Prochaine étape : laisser les cycles adaptatifs s'enchaîner jusqu'au prochain achat.

Date : 2026-09-26
Sauvegarde : Save3
Objectif : continuer l'accumulation vers `Expand 7`.
Script : game/Save3/main.py
Action : surveillance du cycle suivant sans modification de script ni dépense hors priorité.
Résultat observé : `14 848` citrouilles, drone actif, vitesse solaire maintenue et aucune erreur live.
Progression : la bascule bootstrap/citrouilles reste stable ; le seuil de `64 000` est le prochain achat utile.
Blocage ou risque : aucun blocage, seulement un cycle de croissance long sur la grille 12×12.
Prochaine étape : poursuivre l'AFK jusqu'à `Expand 7`.

Date : 2026-09-26
Sauvegarde : Save3
Objectif : fiabiliser la transition entre méga-récolte et bootstrap.
Script : game/Save3/main.py
Action : ajout de `clear()` lors du passage en mode carottes, puis relance contrôlée.
Résultat observé : `96` cases d'herbe restaurées, foin remonté à `2 450`, stock à `16 784` citrouilles ; aucun warning live.
Progression : les cycles ne conservent plus les plants morts et ne bloquent plus la production de foin.
Blocage ou risque : la puissance solaire est basse pendant le bootstrap, mais les tournesols sont replantés au retour en mode citrouilles.
Prochaine étape : continuer vers `64 000` citrouilles et `Expand 7`.

Date : 2026-09-26
Sauvegarde : Save3
Objectif : accélérer les phases de bootstrap sans perdre le bonus solaire.
Script : game/Save3/main.py
Action : ajout de 10 tournesols dans le bootstrap, puis suppression du nettoyage qui retardait la conversion carottes → citrouilles.
Résultat observé : `17 672` citrouilles, `5 068` foin, `99` puissance et `speedFactor 15,1875` ; sortie live vide de warnings.
Progression : la phase carottes conserve sa vitesse maximale et la phase citrouilles reprend directement sur les cases existantes.
Blocage ou risque : aucun blocage ; le seuil `64 000` reste le prochain achat.
Prochaine étape : poursuivre les cycles optimisés jusqu'à `Expand 7`.

## Modèle

```text
Date : YYYY-MM-DD HH:mm
Sauvegarde : SaveN
Objectif : ...
Script : ...
Action : ...
Résultat observé : ...
Progression : ...
Blocage ou risque : ...
Prochaine étape : ...
```
