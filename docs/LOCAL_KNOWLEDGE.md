# Base de connaissances locale — The Farmer Was Replaced

Résumé de recherche avant toute partie. La référence détaillée est archivée dans `docs/source_snapshot/`.

## Sources prioritaires

1. Documentation et `builtins.py` de l'installation locale.
2. État réel de `Save3/save.json`.
3. Wiki et notes Steam pour les informations manquantes.

## État de Save3

Sauvegarde version `3`, au début de la progression. Déblocages observés :

```text
grass, soil, harvest, pass, do_a_flip, pet_the_piggy,
grassland, hay, straw_hat, tap
```

Le code local est dans `game/Save3/main.py`. Le pont MCP de l'autre agent lit et écrit directement dans le dossier de sauvegarde.

## Langage

Langage proche de Python, débloqué progressivement : indentation, variables, conditions, boucles, fonctions, listes, tuples, dictionnaires, sets et imports. Ce n'est pas Python complet : pas de classes, lambdas, compréhensions, `async/await`, `global` ou paramètres nommés classiques.

Les fenêtres de code sont des fichiers `.py`. Le jeu fournit un `__builtins__.py` pour l'auto-complétion, archivé dans `docs/source_snapshot/api/builtins.py`.

Au tout début, les commandes disponibles sont `harvest()` et `do_a_flip()`.

## API essentielle

```text
harvest(), can_harvest(), plant(), till(), use_item(), clear(), change_hat()
move(), can_move(), get_pos_x(), get_pos_y(), get_world_size()
get_entity_type(), get_ground_type(), get_water(), num_items()
get_companion(), measure()
get_cost(), unlock(), num_unlocked()
spawn_drone(), wait_for(), has_finished(), max_drones(), num_drones()
get_time(), get_tick_count(), quick_print(), print()
set_execution_speed(), set_world_size(), simulate(), leaderboard_run()
```

Les actions physiques réussies coûtent généralement `200` ticks ; les capteurs coûtent `1` tick. `get_time()`, `get_tick_count()` et `quick_print()` sont gratuits. `print()` prend environ une seconde.

`get_cost()` doit être utilisé plutôt que des coûts codés en dur. `unlock()` automatise les achats. `num_unlocked()` renvoie un niveau pour les déblocages et `0/1` pour les éléments non améliorables.

## Terrain et entités

- `Grassland` : terrain par défaut ; l'herbe repousse automatiquement.
- `Soil` : obtenu avec `till()` ; nécessaire aux carottes, citrouilles, tournesols et cactus.
- `Grass` : pousse en environ `0,5 s`, produit du foin.
- `Bush` : pousse en environ `4 s`, produit du bois.
- `Tree` : environ `7 s`, donne `5` bois ; chaque voisin cardinal double le temps de croissance.
- `Carrot` : environ `6 s`, sur sol.
- `Pumpkin` : environ `2 s`, fusionne en méga-citrouille ; environ 20 % de mortalité.
- `Sunflower` : environ `5 s`, produit de la puissance ; pétales mesurables.
- `Cactus` : environ `1 s`, taille de 0 à 9, récolte en chaîne si trié.
- `Dinosaur`, `Apple`, `Hedge`, `Treasure` : mini-jeux dinosaure et labyrinthe.

## Mécaniques à connaître

### Eau et engrais

L'eau va de `0` à `1` et accélère la croissance d'environ `1x` à `5x`. Le sol perd en moyenne 1 % de son eau actuelle par seconde. Un réservoir de `0,25` arrive toutes les 10 secondes ; les améliorations de `Watering` doublent la quantité reçue.

`use_item(Items.Fertilizer)` retire 2 secondes de croissance et infecte la plante. Une plante infectée transforme la moitié de son rendement en `Weird_Substance`. Cette substance inverse l'infection de la plante et de ses voisines.

### Tournesols

Les tournesols ont de 7 à 15 pétales. Avec au moins 10 tournesols, récolter celui qui a le maximum de pétales donne un bonus de puissance. La documentation française installée indique `8x`, tandis qu'une docstring de `builtins.py` indique `5x` : à vérifier avec le futur MCP avant optimisation.

La puissance accélère le drone et consomme environ 1 unité toutes les 30 actions.

### Citrouilles

Une méga-citrouille de côté `n` rapporte `n³` pour `n <= 5`, puis `6n²` pour `n >= 6`. Les citrouilles mortes doivent être remplacées.

### Polyculture

`get_companion()` renvoie le type et la position du compagnon souhaité. La préférence est aléatoire par plante, le compagnon n'a pas besoin d'être adulte. Le multiplicateur est documenté à `5` avant amélioration et double à chaque niveau.

### Cactus

Les tailles vont de 0 à 9. Pour être triée, une zone doit être croissante vers le nord et l'est, décroissante vers le sud et l'ouest. `swap(direction)` échange deux voisins. Une récolte propagée sur `n` cactus donne `n²` cactus.

### Labyrinthes

`use_item(Items.Weird_Substance, quantité)` sur un buisson crée un labyrinthe. Sans amélioration, `n` substances donnent un labyrinthe `n×n`. Le trésor vaut la surface du labyrinthe en or. `move()`/`can_move()` détectent les murs et `measure()` la position du trésor.

### Dinosaures

`change_hat(Hats.Dinosaur_Hat)` lance le mini-jeu. Le drone mange des pommes pour faire grandir sa queue. Retirer le chapeau récolte une quantité d'os égale au carré de la longueur de la queue. `measure()` sur une pomme indique la prochaine position.

### Drones multiples

Chaque drone a sa propre copie mémoire : pas de mémoire globale partagée. Les arguments sont copiés. Les actions simultanées sur la même case peuvent provoquer des conditions de course. Il faut répartir les zones et synchroniser avec `wait_for()`.

## Progression de référence

```text
Herbe/foin
→ boucles, conditions, mouvement
→ sol, carottes, arbres
→ tournesols, citrouilles
→ variables, fonctions, listes, dictionnaires, imports
→ eau, engrais, polyculture, vitesse
→ labyrinthes, cactus, dinosaures, drones multiples
→ simulations et classements
```

Déblocages importants : `Loops`, `Operators`, `Variables`, `Senses`, `Expand`, `Plant`, `Carrots`, `Trees`, `Speed`, `Sunflowers`, `Pumpkins`, `Functions`, `Lists`, `Dictionaries`, `Watering`, `Fertilizer`, `Polyculture`, `Mazes`, `Cactus`, `Dinosaurs`, `Megafarm`, `Simulation`, `Timing` et `Leaderboard`.

## Optimisation

1. Parcours en serpentin.
2. Tester avant `harvest`, `plant`, `till` et `use_item`.
3. Garder les fonctions idempotentes.
4. Utiliser `get_cost()` pour choisir automatiquement la prochaine culture.
5. Réserver `clear()` et `set_world_size()` aux tests ou aux runs explicitement réinitialisés.
6. Comparer les variantes avec `get_tick_count()` et `simulate()` sur une graine fixe.
7. Éviter les imports avec effets de bord.

## Vérifications réservées au MCP

- état précis de la grille et du drone ;
- coûts courants et déblocages réellement disponibles ;
- multiplicateur réel des tournesols ;
- format des scripts après sauvegarde ;
- délai du File Watcher ;
- puissance, eau et conditions de course en exécution réelle.
