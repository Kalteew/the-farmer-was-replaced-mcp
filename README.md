# MCP — The Farmer Was Replaced

Pont local entre un client MCP et le jeu, avec lecture directe de l'état via BepInEx.

Projet public : https://github.com/Kalteew/the-farmer-was-replaced-mcp

Le serveur est enregistré dans la configuration Codex sous `the_farmer_was_replaced`.
Après un redémarrage de Codex, ses outils `tfwr_*` seront disponibles.

Le dossier `bridge/TFWRBridge/` contient le plugin BepInEx. Il expose une API locale en lecture directe du jeu, sur `127.0.0.1:17342`.

## Règle d'extension

Chaque problème rencontré pendant une partie doit devenir une méthode MCP réutilisable : chargement de sauvegarde, exécution directe, lecture d'état, actions, documentation, recettes, etc. Les fallbacks clavier ou écran restent des secours, pas le fonctionnement principal.

## Installation

```powershell
npm install
```

Prérequis : le jeu installé, Node.js 20+, le SDK .NET avec la cible .NET Framework 4.7.2, et [BepInEx 5.4.23.5](https://github.com/BepInEx/BepInEx/releases/tag/v5.4.23.5). Le chemin Steam par défaut est détecté automatiquement ; sinon définir `TFWR_GAME_ROOT`.

Pour enregistrer le serveur dans Codex :

```toml
[mcp_servers.the_farmer_was_replaced]
type = "stdio"
command = "node"
args = ["C:\\chemin\\the-farmer-was-replaced-mcp\\src\\server.mjs"]
startup_timeout_sec = 30
```

Le serveur expose les outils `tfwr_*` et utilise la sauvegarde active indiquée par `options.txt`. Les scripts sont écrits dans le dossier `Saves/SaveN` et, si elle existe, dans la copie de travail `game/SaveN`; le File Watcher du jeu doit rester activé.

La documentation de référence locale est dans `docs/LOCAL_KNOWLEDGE.md`. Les sources embarquées du jeu sont archivées dans `docs/source_snapshot/`.

## Outils

- `tfwr_get_state`, `tfwr_list_saves`, `tfwr_capture_screen`
- `tfwr_bridge_health`, `tfwr_load_save`, `tfwr_live_state`, `tfwr_live_inventory`
- `tfwr_live_unlocks`, `tfwr_unlock`, `tfwr_live_catalog`, `tfwr_live_grid`
- `tfwr_read_script`, `tfwr_write_script`, `tfwr_refresh_scripts`
- `tfwr_run`, `tfwr_measure_run`, `tfwr_stop`, `tfwr_pause`, `tfwr_save`
- `tfwr_get_output`, `tfwr_read_reference`
- `tfwr_list_recipes`, `tfwr_recipe_tree`, `tfwr_add_recipe`

`tfwr_write_script` crée une copie dans `.mcp-backups` avant d'écraser un fichier existant. Après la création d'un nouveau module, `tfwr_refresh_scripts` l'enregistre dans l'éditeur interne du jeu sans automatiser la souris. `tfwr_run` exécute directement le script via le pont BepInEx ; F5 reste un secours si le pont n'est pas disponible.

`tfwr_measure_run` exécute une passe bornée et retourne les variations d'inventaire, la productivité par minute, les positions visitées, la couverture de grille, les changements de position et les wraps détectés sur les deux axes.

### Actions en jeu

- `tfwr_unlock` achète ou améliore un déblocage par son nom (`Loops` ou `Unlocks.Loops`).
- `tfwr_stop` arrête directement le script actif via le pont, avec repli sur Maj+F5.
- `tfwr_save` envoie Ctrl+S à la fenêtre du jeu.

Pour une action de progression, lire d'abord `tfwr_live_unlocks` et l'état réel du jeu, puis utiliser `tfwr_unlock`. Les coûts restent calculés par le jeu.

Les déplacements de la ferme sont toriques : dépasser un bord fait réapparaître le drone sur le bord opposé, horizontalement comme verticalement. Un balayage fiable doit donc utiliser exactement `get_world_size()` déplacements par axe, sans mouvements de correction aux bords.

`tfwr_get_state` lit le JSON de sauvegarde (déblocages, inventaire sérialisé, terrain et entités quand le jeu les a enregistrés). `tfwr_capture_screen` fournit en plus une image de l'interface réelle. Les recettes et coûts documentés sont une base locale : les coûts dynamiques du jeu devront être confirmés avec `get_cost()` avant une action importante.

## Pont BepInEx

Le projet du plugin se compile avec :

```powershell
dotnet build bridge/TFWRBridge/TFWRBridge.csproj
```

Après installation de BepInEx dans le dossier du jeu, installer le plugin avec :

```powershell
powershell -File tools/install-bepinex.ps1
```

Le plugin expose l'API locale `http://127.0.0.1:17342` : état, inventaire, déblocages, catalogue, grille, chargement de sauvegarde et exécution de script.

Pour un autre emplacement :

```powershell
$env:TFWR_GAME_ROOT = 'D:\\SteamLibrary\\steamapps\\common\\The Farmer Was Replaced'
dotnet build bridge/TFWRBridge/TFWRBridge.csproj /p:GameRoot="$env:TFWR_GAME_ROOT"
powershell -File tools/install-bepinex.ps1
```

## Test manuel

```powershell
npm run inspect
npm run mcp
```

## Skills et suivi local

- `skills/tfwr-play/` : jouer via le pont MCP.
- `skills/tfwr-research/` : approfondir les mécaniques sans modifier la sauvegarde.
- `skills/tfwr-progress/` : maintenir l'état, la feuille de route et l'historique.
- `progress/` : suivi permanent de la progression dans le jeu.
- `docs/LOCAL_KNOWLEDGE.md` : base de connaissances consolidée.
