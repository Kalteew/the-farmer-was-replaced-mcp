# Référence locale — The Farmer Was Replaced

> Synthèse courte. Pour la base complète et la documentation extraite de l'installation locale, voir [LOCAL_KNOWLEDGE.md](LOCAL_KNOWLEDGE.md) et `source_snapshot/`.

## Boucle de jeu

Programmer un drone dans un langage proche de Python, récolter des ressources, acheter des déblocages, agrandir la ferme et optimiser les scripts. L'expansion peut réinitialiser le terrain : les scripts doivent donc savoir reconstruire la ferme.

## Progression générale

1. Herbe, foin et récolte simple.
2. Boucles, conditions et déplacements.
3. Sol, carottes, arbres, tournesols et citrouilles.
4. Variables, fonctions, listes, dictionnaires, ensembles et imports.
5. Eau, engrais, polyculture et vitesse.
6. Labyrinthes, cactus, dinosaures et drones multiples.
7. Simulations et classements chronométrés.

## Fonctions prioritaires

```text
harvest(), plant(), till(), move(), swap(), use_item()
can_harvest(), can_move()
get_entity_type(), get_ground_type(), get_pos_x(), get_pos_y()
get_world_size(), get_water(), measure(), get_companion()
num_items(), get_cost(), unlock(), num_unlocked()
spawn_drone(), wait_for(), has_finished()
print(), quick_print(), get_tick_count(), get_time(), simulate()
```

Le langage n'est pas Python complet : pas de classes, lambdas, compréhensions, `async/await`, `global` ou paramètres nommés classiques. Les nombres sont des flottants. `quick_print()` est préférable dans les boucles.

## Ressources et mécaniques

- **Foin** : herbe ; premiers déblocages.
- **Bois** : buissons et arbres ; les arbres donnent davantage mais poussent plus lentement côte à côte.
- **Carottes** : culture sur sol labouré ; servent notamment aux citrouilles.
- **Citrouilles** : les groupes fusionnent ; certaines peuvent mourir, il faut les replanter.
- **Énergie** : tournesols ; accélère l'exécution. Comparer les pétales avec `measure()`.
- **Eau** : accélère la croissance.
- **Engrais / substance étrange** : accélère et ouvre les mécaniques de labyrinthes.
- **Or** : trésors des labyrinthes.
- **Cactus** : récolte en chaîne si la zone est triée.
- **Os** : dinosaures.

## Règles d'automatisation

- Tester avant d'agir : `can_harvest()` avant `harvest()`.
- Éviter `till()` sans condition : la fonction alterne l'état du sol.
- Parcourir la ferme en serpentin pour limiter les déplacements.
- Utiliser `get_cost()` plutôt que coder les coûts en dur.
- Pour les drones, répartir les zones et synchroniser avec `wait_for()`.
- Mesurer les variantes avec `get_tick_count()` ou `simulate()`.
- Garder les fonctions idempotentes : elles doivent réparer une case quel que soit son état initial.
- Ne pas utiliser `clear()` ou `set_world_size()` sur la partie réelle sans sauvegarde préalable : ces fonctions peuvent détruire le terrain.

## Sources

- Wiki : https://thefarmerwasreplaced.wiki.gg/
- API : https://thefarmerwasreplaced.wiki.gg/wiki/Available_Functions
- Déblocages : https://thefarmerwasreplaced.wiki.gg/wiki/Unlocks
- Page Steam : https://store.steampowered.com/app/2060160/The_Farmer_Was_Replaced/
- Sauvegardes Steam : https://steamdb.info/app/2060160/ufs/
