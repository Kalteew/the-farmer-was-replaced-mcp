# MCP — The Farmer Was Replaced

[![English](https://img.shields.io/badge/Language-English-blue)](README.md)
[![Français](https://img.shields.io/badge/Language-Français-green)](README.fr.md)

---

Local bridge between an MCP client and the game, with direct access to game state through BepInEx.

Public project: https://github.com/Kalteew/the-farmer-was-replaced-mcp

The server is registered in the Codex configuration as `the_farmer_was_replaced`.
After restarting Codex, its `tfwr_*` tools will be available.

The `bridge/TFWRBridge/` directory contains the BepInEx plugin. It exposes a local API that reads the game state directly at `127.0.0.1:17342`.

## Extension rule

Whenever an issue is encountered while playing, turn it into a reusable MCP method where appropriate: loading saves, running scripts directly, reading state, performing actions, accessing documentation and recipes, etc. Keyboard or screen-based fallbacks are emergency options, not the primary workflow.

## Installation

```powershell
npm install
```

Requirements: the game installed, Node.js 20+, the .NET SDK with the .NET Framework 4.7.2 target, and [BepInEx 5.4.23.5](https://github.com/BepInEx/BepInEx/releases/tag/v5.4.23.5). The default Steam path is detected automatically; otherwise, set `TFWR_GAME_ROOT`.

To register the server in Codex:

```toml
[mcp_servers.the_farmer_was_replaced]
type = "stdio"
command = "node"
args = ["C:\\path\\to\\the-farmer-was-replaced-mcp\\src\\server.mjs"]
startup_timeout_sec = 30
```

The server exposes `tfwr_*` tools and uses the active save specified by `options.txt`. Scripts are written to the `Saves/SaveN` directory and, if it exists, to the `game/SaveN` working copy; the game's File Watcher must remain enabled.

The local reference documentation is in `docs/LOCAL_KNOWLEDGE.md`. A snapshot of the game's bundled sources is archived in `docs/source_snapshot/`.

## Tools

- `tfwr_get_state`, `tfwr_list_saves`, `tfwr_capture_screen`
- `tfwr_bridge_health`, `tfwr_new_save`, `tfwr_load_save`, `tfwr_live_state`, `tfwr_live_inventory`
- `tfwr_live_unlocks`, `tfwr_unlock`, `tfwr_live_catalog`, `tfwr_live_grid`
- `tfwr_read_script`, `tfwr_write_script`, `tfwr_refresh_scripts`
- `tfwr_run`, `tfwr_measure_run`, `tfwr_stop`, `tfwr_pause`, `tfwr_save`
- `tfwr_get_output`, `tfwr_read_reference`
- `tfwr_list_recipes`, `tfwr_recipe_tree`, `tfwr_add_recipe`

`tfwr_write_script` creates a backup in `.mcp-backups` before overwriting an existing file. After a new module is created, `tfwr_refresh_scripts` registers it in the game's internal editor without automating the mouse. `tfwr_run` executes the script directly through the BepInEx bridge; F5 is a fallback if the bridge is unavailable.

`tfwr_measure_run` executes a bounded pass and returns inventory changes, productivity per minute, visited positions, grid coverage, position changes, and wraps detected on both axes.

### In-game actions

- `tfwr_new_save` creates and loads a new save through the game's internal menu.
- `tfwr_unlock` purchases or upgrades an unlock by name (`Loops` or `Unlocks.Loops`).
- `tfwr_stop` directly stops the active script through the bridge, falling back to Shift+F5.
- `tfwr_save` sends Ctrl+S to the game window.

Before taking a progression action, first read `tfwr_live_unlocks` and the game's current state, then use `tfwr_unlock`. Costs are calculated by the game.

Farm movement is toroidal: crossing an edge wraps the drone to the opposite edge, horizontally and vertically. A reliable sweep should therefore use exactly `get_world_size()` moves per axis, without corrective moves at the edges.

`tfwr_get_state` reads the save JSON (unlocks, serialized inventory, terrain, and entities when saved by the game). `tfwr_capture_screen` also provides an image of the live interface. Documented recipes and costs are a local reference; confirm dynamic in-game costs with `get_cost()` before important actions.

## BepInEx bridge

Build the plugin project with:

```powershell
dotnet build bridge/TFWRBridge/TFWRBridge.csproj
```

After installing BepInEx in the game directory, install the plugin with:

```powershell
powershell -File tools/install-bepinex.ps1
```

The plugin exposes the local API at `http://127.0.0.1:17342`: game state, inventory, unlocks, catalog, grid, save loading, and script execution.

For a different installation path:

```powershell
$env:TFWR_GAME_ROOT = 'D:\\SteamLibrary\\steamapps\\common\\The Farmer Was Replaced'
dotnet build bridge/TFWRBridge/TFWRBridge.csproj /p:GameRoot="$env:TFWR_GAME_ROOT"
powershell -File tools/install-bepinex.ps1
```

## Manual testing

```powershell
npm run inspect
npm run mcp
```

## Skills and local tracking

- `skills/tfwr-play/`: play through the MCP bridge.
- `skills/tfwr-research/`: investigate mechanics without modifying the save.
- `skills/tfwr-progress/`: maintain game state, the roadmap, and history.
- `progress/`: ongoing game progress tracking.
- `docs/LOCAL_KNOWLEDGE.md`: consolidated knowledge base.
