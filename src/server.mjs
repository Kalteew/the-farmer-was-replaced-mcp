import { existsSync } from "node:fs";
import { mkdir, readFile, readdir, rename, stat, unlink, writeFile } from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { execFile } from "node:child_process";
import { promisify } from "node:util";
import { McpServer } from "@modelcontextprotocol/server";
import { serveStdio } from "@modelcontextprotocol/server/stdio";
import * as z from "zod/v4";

const execFileAsync = promisify(execFile);
const projectRoot = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const projectGameRoot = path.join(projectRoot, "game");
const docsRoot = path.join(projectRoot, "docs");
const gameRoot = path.resolve(
  process.env.TFWR_DATA_ROOT ??
    path.join(process.env.LOCALAPPDATA ?? path.join(process.env.USERPROFILE ?? "", "AppData", "Local"), "..", "LocalLow", "TheFarmerWasReplaced", "TheFarmerWasReplaced"),
);
const savesRoot = path.join(gameRoot, "Saves");
const optionsPath = path.join(gameRoot, "options.txt");
const outputPath = path.join(gameRoot, "output.txt");
const logPath = path.join(gameRoot, "Player.log");
const keyHelper = path.join(projectRoot, "scripts", "send-game-key.ps1");
const captureHelper = path.join(projectRoot, "scripts", "capture-game.ps1");
const recipeCatalogPath = path.join(projectRoot, "data", "recipes.json");
const bridgeUrl = (process.env.TFWR_BRIDGE_URL ?? "http://127.0.0.1:17342").replace(/\/$/, "");

function textResult(value) {
  return { content: [{ type: "text", text: typeof value === "string" ? value : JSON.stringify(value, null, 2) }] };
}

function errorResult(error) {
  return { isError: true, content: [{ type: "text", text: error instanceof Error ? error.message : String(error) }] };
}

function inside(parent, candidate) {
  const relative = path.relative(parent, candidate);
  return relative === "" || (relative !== ".." && !relative.startsWith(`..${path.sep}`) && !path.isAbsolute(relative));
}

function saveName(value) {
  const name = value ?? "";
  if (!/^Save\d+$/i.test(name)) throw new Error("Nom de sauvegarde invalide. Exemple : Save3.");
  return name;
}

async function readOptions() {
  try {
    const raw = await readFile(optionsPath, "utf8");
    const values = Object.fromEntries(raw.split(/\r?\n/).map((line) => {
      const match = line.match(/^\s*([^=]+?)\s*=\s*(.*?)\s*$/);
      return match ? [match[1], match[2]] : ["", ""];
    }).filter(([key]) => key));
    return values;
  } catch {
    return {};
  }
}

async function activeSaveName() {
  const options = await readOptions();
  return saveName(options.activeSave || "Save0");
}

async function resolveSave(requested) {
  const name = requested ? saveName(requested) : await activeSaveName();
  const folder = path.join(savesRoot, name);
  if (!inside(savesRoot, folder)) throw new Error("Sauvegarde hors du dossier autorisé.");
  if (!existsSync(folder)) throw new Error(`Sauvegarde introuvable : ${name}`);
  return { name, folder };
}

function scriptPath(folder, requested) {
  if (!requested || typeof requested !== "string") throw new Error("Le nom du script est requis.");
  const normalized = requested.replaceAll("/", path.sep);
  if (!normalized.toLowerCase().endsWith(".py")) throw new Error("Seuls les fichiers .py sont autorisés.");
  const full = path.resolve(folder, normalized);
  if (!inside(folder, full)) throw new Error("Le script doit rester dans la sauvegarde active.");
  return full;
}

function workspaceScriptPath(save, requested) {
  const folder = path.join(projectGameRoot, save);
  return existsSync(folder) ? scriptPath(folder, requested) : null;
}

async function listScripts(folder) {
  const result = [];
  async function visit(current) {
    for (const entry of await readdir(current, { withFileTypes: true })) {
      if (entry.name === "__pycache__" || entry.name.startsWith(".mcp-")) continue;
      const full = path.join(current, entry.name);
      if (entry.isDirectory()) await visit(full);
      else if (entry.isFile() && entry.name.toLowerCase().endsWith(".py")) {
        const info = await stat(full);
        result.push({ path: path.relative(folder, full).replaceAll(path.sep, "/"), bytes: info.size, modified: info.mtime.toISOString() });
      }
    }
  }
  await visit(folder);
  return result.sort((a, b) => a.path.localeCompare(b.path));
}

async function readSaveJson(folder) {
  try {
    return JSON.parse(await readFile(path.join(folder, "save.json"), "utf8"));
  } catch {
    return {};
  }
}

async function readJson(file, fallback) {
  try { return JSON.parse(await readFile(file, "utf8")); } catch { return fallback; }
}

async function replaceFile(file, content) {
  const temporary = `${file}.mcp-tmp-${process.pid}`;
  await writeFile(temporary, content, "utf8");
  try {
    await rename(temporary, file);
  } catch (error) {
    await writeFile(file, content, "utf8");
    await unlink(temporary).catch(() => {});
    if (error?.code !== "EEXIST" && error?.code !== "EPERM") throw error;
  }
}

function scalar(value) {
  if (typeof value !== "string") return value;
  const trimmed = value.trim();
  if (trimmed === "true") return true;
  if (trimmed === "false") return false;
  if (trimmed === "null") return null;
  const number = Number(trimmed);
  return Number.isNaN(number) ? trimmed : number;
}

function parseDataString(value) {
  if (typeof value !== "string") return {};
  return Object.fromEntries(value.split(",").map((part) => {
    const separator = part.indexOf("=");
    if (separator < 0) return [part.trim(), true];
    return [part.slice(0, separator).trim(), scalar(part.slice(separator + 1))];
  }).filter(([key]) => key));
}

function nameOfItem(value) {
  if (typeof value !== "string") return String(value);
  return value.replace(/^Items\./, "");
}

function parseInventory(saveData) {
  const raw = saveData?.items?.serializeList ?? [];
  const quantities = {};
  const add = (name, amount) => {
    if (name == null || amount == null || Number.isNaN(Number(amount))) return;
    const key = nameOfItem(name);
    quantities[key] = (quantities[key] ?? 0) + Number(amount);
  };
  const entries = Array.isArray(raw) ? raw : [raw];
  for (const entry of entries) {
    if (typeof entry === "object" && entry !== null) {
      const name = entry.item ?? entry.type ?? entry.key ?? entry.name ?? entry.id;
      const amount = entry.amount ?? entry.count ?? entry.quantity ?? entry.value;
      add(name, amount);
      continue;
    }
    const text = String(entry);
    const match = text.match(/(?:Items\.)?([A-Za-z_]+)\s*(?:[:=]|,\s*amount\s*=)\s*(-?\d+(?:\.\d+)?)/i);
    if (match) add(match[1], match[2]);
  }
  return { quantities, rawEntries: entries.length };
}

function parseWorldEntries(entries = []) {
  return entries.map((entry) => ({
    x: entry?.pos?.x ?? null,
    y: entry?.pos?.y ?? null,
    ...parseDataString(entry?.data),
    raw: entry?.data ?? null,
  }));
}

async function progressionData() {
  return readJson(path.join(projectRoot, "data", "progression.json"), { unlocks: [] });
}

async function tail(file, maxBytes = 12000) {
  try {
    const value = await readFile(file, "utf8");
    return value.length > maxBytes ? value.slice(-maxBytes) : value;
  } catch {
    return "";
  }
}

async function bridgeFetch(endpoint) {
  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), 1200);
  try {
    const response = await fetch(`${bridgeUrl}/${endpoint.replace(/^\//, "")}`, { signal: controller.signal });
    const body = await response.text();
    let value;
    try { value = JSON.parse(body); } catch { throw new Error(`Réponse BepInEx invalide : ${body.slice(0, 300)}`); }
    if (!response.ok || value?.ok === false) throw new Error(value?.error ?? `BepInEx HTTP ${response.status}`);
    return value;
  } finally {
    clearTimeout(timeout);
  }
}

async function gameState(requested) {
  const save = await resolveSave(requested);
  const data = await readSaveJson(save.folder);
  let live = null;
  let liveError = null;
  try { live = await bridgeFetch("state"); } catch (error) { liveError = error?.message ?? String(error); }
  return {
    gameRoot,
    activeSave: save.name,
    options: await readOptions(),
    unlocks: data.unlocks ?? [],
    inventory: parseInventory(data),
    grounds: parseWorldEntries(data.grounds),
    entities: parseWorldEntries(data.entities),
    research: (await progressionData()).unlocks.filter((entry) => (data.unlocks ?? []).some((value) => value.toLowerCase() === entry.id.toLowerCase() || value.toLowerCase() === entry.gameKey?.toLowerCase())),
    version: data.version ?? null,
    scripts: await listScripts(save.folder),
    output: await tail(outputPath),
    playerLog: await tail(logPath, 6000),
    live,
    liveError,
  };
}

async function recipes() {
  const value = await readJson(recipeCatalogPath, { version: 1, recipes: [] });
  return Array.isArray(value) ? value : (value.recipes ?? []);
}

async function writeRecipes(value) {
  await mkdir(path.dirname(recipeCatalogPath), { recursive: true });
  if (existsSync(recipeCatalogPath)) {
    const backup = path.join(projectRoot, "data", ".backups", `${Date.now()}.json`);
    await mkdir(path.dirname(backup), { recursive: true });
    await writeFile(backup, await readFile(recipeCatalogPath));
  }
  await replaceFile(recipeCatalogPath, JSON.stringify({ version: 1, recipes: value }, null, 2) + "\n");
}

async function captureScreen() {
  if (!existsSync(captureHelper)) throw new Error(`Helper capture introuvable : ${captureHelper}`);
  const cache = path.join(projectRoot, ".mcp-cache");
  const file = path.join(cache, "game-screen.png");
  await mkdir(cache, { recursive: true });
  try {
    const { stdout, stderr } = await execFileAsync("powershell.exe", [
      "-NoProfile", "-NonInteractive", "-ExecutionPolicy", "Bypass", "-File", captureHelper, file,
    ], { windowsHide: true, timeout: 15000 });
    const image = await readFile(file);
    return { content: [
      { type: "text", text: (stdout || stderr || "Interface capturée").trim() },
      { type: "image", data: image.toString("base64"), mimeType: "image/png" },
    ] };
  } catch (error) {
    throw new Error(`Impossible de capturer l'interface : ${error?.stderr || error?.message || error}`);
  }
}

async function sendGameKey(key) {
  if (!existsSync(keyHelper)) throw new Error(`Helper clavier introuvable : ${keyHelper}`);
  try {
    const { stdout, stderr } = await execFileAsync("powershell.exe", [
      "-NoProfile", "-NonInteractive", "-ExecutionPolicy", "Bypass", "-File", keyHelper, key,
    ], { windowsHide: true, timeout: 15000 });
    return (stdout || stderr || "").trim();
  } catch (error) {
    const detail = error?.stderr || error?.message || String(error);
    throw new Error(`Impossible d'envoyer ${key} au jeu : ${detail}`);
  }
}

async function runGame(requestedSave) {
  const save = await resolveSave(requestedSave);
  const main = scriptPath(save.folder, "main.py");
  if (!existsSync(main)) throw new Error(`main.py absent de ${save.name}. Écris-le d'abord avec tfwr_write_script.`);
  try {
    return { save: save.name, action: "run", control: "bepinex", result: await bridgeFetch("run") };
  } catch (firstError) {
    try {
      await bridgeFetch(`load/${save.name}`);
      return { save: save.name, action: "run", control: "bepinex", loaded: true, result: await bridgeFetch("run") };
    } catch {
      return { save: save.name, action: "run", control: "keyboard-fallback", result: await sendGameKey("F5"), bridgeError: firstError?.message ?? String(firstError) };
    }
  }
}

function register(server) {
  server.registerTool("tfwr_bridge_health", {
    description: "Vérifie si le plugin BepInEx est chargé et si le jeu expose son état en mémoire.",
    inputSchema: z.object({}),
  }, async () => {
    try { return textResult(await bridgeFetch("health")); } catch (error) { return errorResult(error); }
  });

  server.registerTool("tfwr_load_save", {
    description: "Charge une sauvegarde directement via le menu interne du jeu, sans automatiser un clic graphique.",
    inputSchema: z.object({ save: z.string().regex(/^Save\d+$/i).describe("Exemple : Save3") }),
  }, async ({ save }) => {
    try { return textResult(await bridgeFetch(`load/${save}`)); } catch (error) { return errorResult(error); }
  });

  server.registerTool("tfwr_live_state", {
    description: "Interroge directement le jeu via BepInEx : inventaire, déblocages, simulation, grille et drones.",
    inputSchema: z.object({}),
  }, async () => {
    try { return textResult(await bridgeFetch("state")); } catch (error) { return errorResult(error); }
  });

  server.registerTool("tfwr_live_inventory", {
    description: "Lit l'inventaire réel en mémoire, avec les identifiants et noms des objets.",
    inputSchema: z.object({}),
  }, async () => {
    try { return textResult(await bridgeFetch("inventory")); } catch (error) { return errorResult(error); }
  });

  server.registerTool("tfwr_live_unlocks", {
    description: "Lit directement l'arbre des déblocages, leurs niveaux, coûts et documentation exposés par le jeu.",
    inputSchema: z.object({}),
  }, async () => {
    try { return textResult(await bridgeFetch("unlocks")); } catch (error) { return errorResult(error); }
  });

  server.registerTool("tfwr_unlock", {
    description: "Achète ou améliore directement un déblocage dans l'arbre de recherche du jeu via BepInEx.",
    inputSchema: z.object({ unlock: z.string().min(1).describe("Exemple : Loops ou Unlocks.Loops") }),
  }, async ({ unlock }) => {
    try { return textResult(await bridgeFetch(`unlock/${encodeURIComponent(unlock)}`)); } catch (error) { return errorResult(error); }
  });

  server.registerTool("tfwr_live_catalog", {
    description: "Lit le catalogue interne du jeu : items, objets de ferme et documentation disponible.",
    inputSchema: z.object({}),
  }, async () => {
    try { return textResult(await bridgeFetch("catalog")); } catch (error) { return errorResult(error); }
  });

  server.registerTool("tfwr_live_grid", {
    description: "Lit la grille réelle de la ferme : objets, sols et drones avec leurs positions.",
    inputSchema: z.object({}),
  }, async () => {
    try { return textResult(await bridgeFetch("grid")); } catch (error) { return errorResult(error); }
  });

  server.registerTool("tfwr_get_state", {
    description: "Lit l'état de la sauvegarde active : déblocages, scripts, options et sortie récente du jeu.",
    inputSchema: z.object({ save: z.string().optional().describe("Exemple : Save3. Par défaut, la sauvegarde active.") }),
  }, async ({ save }) => {
    try { return textResult(await gameState(save)); } catch (error) { return errorResult(error); }
  });

  server.registerTool("tfwr_list_saves", {
    description: "Liste les sauvegardes The Farmer Was Replaced disponibles.",
    inputSchema: z.object({}),
  }, async () => {
    try {
      const entries = await readdir(savesRoot, { withFileTypes: true });
      const saves = [];
      for (const entry of entries) {
        if (!entry.isDirectory() || !/^Save\d+$/i.test(entry.name)) continue;
        const folder = path.join(savesRoot, entry.name);
        const data = await readSaveJson(folder);
        saves.push({ name: entry.name, unlocks: data.unlocks ?? [], version: data.version ?? null, scripts: await listScripts(folder) });
      }
      return textResult(saves.sort((a, b) => a.name.localeCompare(b.name)));
    } catch (error) { return errorResult(error); }
  });

  server.registerTool("tfwr_read_script", {
    description: "Lit un script .py de la sauvegarde active.",
    inputSchema: z.object({ save: z.string().optional(), path: z.string().describe("Chemin relatif, par exemple main.py") }),
  }, async ({ save: requestedSave, path: requestedPath }) => {
    try {
      const save = await resolveSave(requestedSave);
      return textResult(await readFile(scriptPath(save.folder, requestedPath), "utf8"));
    } catch (error) { return errorResult(error); }
  });

  server.registerTool("tfwr_write_script", {
    description: "Crée ou remplace un script .py. Une copie de sécurité est faite avant remplacement.",
    inputSchema: z.object({ save: z.string().optional(), path: z.string().describe("Chemin relatif .py"), content: z.string() }),
  }, async ({ save: requestedSave, path: requestedPath, content }) => {
    try {
      const save = await resolveSave(requestedSave);
      const destination = scriptPath(save.folder, requestedPath);
      const workspaceDestination = workspaceScriptPath(save.name, requestedPath);
      await mkdir(path.dirname(destination), { recursive: true });
      const backupDir = path.join(save.folder, ".mcp-backups", new Date().toISOString().replaceAll(":", "-").replaceAll(".", "-"));
      if (existsSync(destination)) {
        await mkdir(backupDir, { recursive: true });
        await writeFile(path.join(backupDir, path.basename(destination)), await readFile(destination));
      }
      await replaceFile(destination, content);
      if (workspaceDestination) {
        await mkdir(path.dirname(workspaceDestination), { recursive: true });
        await writeFile(workspaceDestination, content, "utf8");
      }
      return textResult({ save: save.name, path: path.relative(save.folder, destination).replaceAll(path.sep, "/"), bytes: Buffer.byteLength(content), watcher: "enabled in current game settings" });
    } catch (error) { return errorResult(error); }
  });

  server.registerTool("tfwr_run", {
    description: "Lance main.py via le bouton d'exécution interne du jeu; utilise F5 en repli.",
    inputSchema: z.object({ save: z.string().optional() }),
  }, async ({ save: requestedSave }) => {
    try { return textResult(await runGame(requestedSave)); } catch (error) { return errorResult(error); }
  });

  server.registerTool("tfwr_stop", {
    description: "Arrête l'exécution du code dans le jeu en envoyant Maj+F5.",
    inputSchema: z.object({}),
  }, async () => {
    try { return textResult(await bridgeFetch("stop")); } catch (firstError) {
      try { return textResult({ action: "stop", result: await sendGameKey("Shift+F5"), bridgeError: firstError?.message ?? String(firstError) }); }
      catch (error) { return errorResult(error); }
    }
  });

  server.registerTool("tfwr_pause", {
    description: "Met en pause ou reprend l'exécution du code dans le jeu avec Ctrl+F5.",
    inputSchema: z.object({}),
  }, async () => {
    try { return textResult({ action: "pause-toggle", result: await sendGameKey("Ctrl+F5") }); } catch (error) { return errorResult(error); }
  });

  server.registerTool("tfwr_save", {
    description: "Sauvegarde la partie active avec Ctrl+S.",
    inputSchema: z.object({}),
  }, async () => {
    try { return textResult({ action: "save", result: await sendGameKey("Ctrl+S") }); } catch (error) { return errorResult(error); }
  });

  server.registerTool("tfwr_get_output", {
    description: "Lit la sortie récente du jeu après une exécution.",
    inputSchema: z.object({ maxChars: z.number().int().min(1).max(50000).optional() }),
  }, async ({ maxChars }) => textResult({ output: await tail(outputPath, maxChars ?? 12000), playerLog: await tail(logPath, 6000) }));

  server.registerTool("tfwr_read_reference", {
    description: "Lit une référence locale du jeu pour choisir une stratégie compatible avec les déblocages actuels.",
    inputSchema: z.object({ file: z.string().optional().describe("Par défaut TFWR_REFERENCE.md; autre exemple : source_snapshot/api/builtins.py") }),
  }, async ({ file }) => {
    try {
      const requested = file ?? "TFWR_REFERENCE.md";
      const full = path.resolve(docsRoot, requested.replaceAll("/", path.sep));
      if (!inside(docsRoot, full)) throw new Error("La référence doit rester dans docs/.");
      return textResult(await readFile(full, "utf8"));
    } catch (error) { return errorResult(error); }
  });

  server.registerTool("tfwr_capture_screen", {
    description: "Capture l'interface visible de The Farmer Was Replaced pour lire visuellement la ferme, les compteurs et le menu de recherche.",
    inputSchema: z.object({}),
  }, async () => {
    try { return await captureScreen(); } catch (error) { return errorResult(error); }
  });

  server.registerTool("tfwr_list_recipes", {
    description: "Liste les recettes et relations de production connues dans le catalogue local.",
    inputSchema: z.object({ category: z.string().optional() }),
  }, async ({ category }) => {
    try {
      const all = await recipes();
      return textResult(category ? all.filter((recipe) => recipe.category === category) : all);
    } catch (error) { return errorResult(error); }
  });

  server.registerTool("tfwr_recipe_tree", {
    description: "Construit un sous-arbre de dépendances à partir d'une recette ou d'une ressource.",
    inputSchema: z.object({ root: z.string(), depth: z.number().int().min(0).max(8).optional() }),
  }, async ({ root, depth }) => {
    try {
      const all = await recipes();
      const limit = depth ?? 4;
      const nodes = new Map();
      const edges = [];
      const visit = (item, level) => {
        if (level > limit || nodes.has(item)) return;
        nodes.set(item, { id: item, level });
        for (const recipe of all) {
          const outputs = Object.keys(recipe.outputs ?? {});
          if (!outputs.some((output) => output.toLowerCase() === item.toLowerCase())) continue;
          for (const input of Object.keys(recipe.inputs ?? {})) {
            edges.push({ from: input, to: item, recipe: recipe.id });
            visit(input, level + 1);
          }
        }
      };
      visit(root, 0);
      return textResult({ root, nodes: [...nodes.values()], edges });
    } catch (error) { return errorResult(error); }
  });

  server.registerTool("tfwr_add_recipe", {
    description: "Ajoute ou met à jour une recette dans le catalogue local, sans modifier directement la sauvegarde du jeu.",
    inputSchema: z.object({
      id: z.string().regex(/^[a-zA-Z0-9._-]+$/),
      name: z.string(),
      category: z.string().optional(),
      inputs: z.record(z.string(), z.number().nonnegative()).default({}),
      outputs: z.record(z.string(), z.number().nonnegative()).default({}),
      notes: z.string().optional(),
      source: z.string().optional(),
    }),
  }, async (recipe) => {
    try {
      const all = await recipes();
      const index = all.findIndex((entry) => entry.id === recipe.id);
      const normalized = { ...recipe, category: recipe.category ?? "custom", inputs: recipe.inputs ?? {}, outputs: recipe.outputs ?? {} };
      if (index >= 0) all[index] = normalized; else all.push(normalized);
      await writeRecipes(all);
      return textResult({ saved: normalized, count: all.length });
    } catch (error) { return errorResult(error); }
  });
}

function createServer() {
  const server = new McpServer(
    { name: "the-farmer-was-replaced", version: "0.1.0" },
    { instructions: "Utilise tfwr_bridge_health puis tfwr_live_state avant d'agir quand BepInEx est disponible. Utilise tfwr_get_state comme repli disque. Écris les scripts avec tfwr_write_script, puis tfwr_run. Le serveur ne peut lire et écrire que les sauvegardes du jeu et le catalogue local de recettes." },
  );
  register(server);
  return server;
}

if (process.argv.includes("--inspect")) {
  console.error(JSON.stringify({ gameRoot, savesRoot, optionsPath, keyHelper }, null, 2));
  process.exit(0);
}

serveStdio(createServer);
