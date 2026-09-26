using System;
using System.Collections;
using System.Collections.Concurrent;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Net;
using System.Reflection;
using System.Text;
using System.Threading;
using BepInEx;
using BepInEx.Logging;
using UnityEngine;

[BepInPlugin("com.yaya.tfwr.bridge", "TFWR Bridge", "0.1.0")]
public sealed class TfwrBridgePlugin : BaseUnityPlugin
{
    private const string Prefix = "http://127.0.0.1:17342/";
    private readonly ConcurrentQueue<PendingRequest> pending = new ConcurrentQueue<PendingRequest>();
    private ManualLogSource log;
    private HttpListener listener;
    private Thread listenerThread;
    private volatile bool stopping;

    private sealed class PendingRequest
    {
        public string Path;
        public ManualResetEventSlim Done = new ManualResetEventSlim(false);
        public int StatusCode;
        public string Response;
    }

    private void Awake()
    {
        log = Logger;
        StartHttpBridge();
        log.LogInfo("TFWR Bridge loaded; waiting for the game simulation.");
    }

    private void Update()
    {
        for (var i = 0; i < 8 && pending.TryDequeue(out var request); i++)
        {
            try
            {
                request.StatusCode = 200;
                request.Response = Handle(request.Path);
            }
            catch (Exception ex)
            {
                request.StatusCode = 500;
                request.Response = ErrorJson(ex.Message);
                log.LogError(ex);
            }
            finally
            {
                request.Done.Set();
            }
        }
    }

    private void OnDestroy()
    {
        stopping = true;
        try { listener?.Stop(); } catch { }
        try { listenerThread?.Join(500); } catch { }
    }

    private void StartHttpBridge()
    {
        try
        {
            listener = new HttpListener();
            listener.Prefixes.Add(Prefix);
            listener.Start();
            listenerThread = new Thread(ListenLoop) { IsBackground = true, Name = "TFWR Bridge HTTP" };
            listenerThread.Start();
        }
        catch (Exception ex)
        {
            log.LogError("Could not start the local bridge: " + ex.Message);
        }
    }

    private void ListenLoop()
    {
        while (!stopping)
        {
            HttpListenerContext context;
            try { context = listener.GetContext(); }
            catch { if (stopping) return; continue; }

            var path = context.Request.Url.AbsolutePath.Trim('/');
            var request = new PendingRequest { Path = path };
            pending.Enqueue(request);
            request.Done.Wait(5000);

            var response = request.Response ?? ErrorJson("The Unity main thread did not answer in time.");
            var bytes = Encoding.UTF8.GetBytes(response);
            context.Response.StatusCode = request.StatusCode == 0 ? 504 : request.StatusCode;
            context.Response.ContentType = "application/json; charset=utf-8";
            context.Response.ContentEncoding = Encoding.UTF8;
            context.Response.ContentLength64 = bytes.Length;
            context.Response.Headers["Access-Control-Allow-Origin"] = "http://127.0.0.1";
            try
            {
                context.Response.OutputStream.Write(bytes, 0, bytes.Length);
            }
            finally
            {
                context.Response.Close();
            }
        }
    }

    private string Handle(string path)
    {
        switch (path.ToLowerInvariant())
        {
            case "":
            case "health": return HealthJson();
            case "state": return StateJson();
            case "inventory": return InventoryJson();
            case "unlocks": return UnlocksJson();
            case "catalog": return CatalogJson();
            case "grid": return GridJson();
            case "run": return RunJson();
            default:
                if (path.StartsWith("load/", StringComparison.OrdinalIgnoreCase)) return LoadJson(path.Substring("load/".Length));
                return ErrorJson("Unknown endpoint: /" + path);
        }
    }

    private string LoadJson(string saveName)
    {
        if (string.IsNullOrWhiteSpace(saveName) || !saveName.StartsWith("Save", StringComparison.OrdinalIgnoreCase))
            return ErrorJson("Nom de sauvegarde invalide.");
        var sim = MainSim.Inst;
        var menu = GetField(sim, "menu");
        if (menu == null) return ErrorJson("Le menu du jeu n'est pas disponible.");
        var method = menu.GetType().GetMethod("LoadSave", BindingFlags.Public | BindingFlags.NonPublic | BindingFlags.Instance);
        if (method == null) return ErrorJson("Menu.LoadSave est introuvable.");
        method.Invoke(menu, new object[] { saveName });
        var play = menu.GetType().GetMethod("Play", BindingFlags.Public | BindingFlags.NonPublic | BindingFlags.Instance);
        play?.Invoke(menu, null);
        return "{\"ok\":true,\"action\":\"load\",\"save\":" + JsonString(saveName) + "}";
    }

    private string RunJson()
    {
        var sim = MainSim.Inst;
        var codeWindow = GetField(sim, "activeCodeWindow");
        if (codeWindow == null)
        {
            var workspace = GetField(sim, "workspace");
            var codeWindows = GetField(workspace, "codeWindows") as IDictionary;
            if (codeWindows != null)
            {
                codeWindow = codeWindows["main"];
                if (codeWindow == null)
                    foreach (DictionaryEntry entry in codeWindows) { codeWindow = entry.Value; break; }
            }
        }
        if (codeWindow == null) return ErrorJson("Aucune fenêtre de code active.");
        var method = codeWindow.GetType().GetMethod("PressExecuteOrStop", BindingFlags.Public | BindingFlags.NonPublic | BindingFlags.Instance);
        if (method == null) return ErrorJson("CodeWindow.PressExecuteOrStop est introuvable.");
        method.Invoke(codeWindow, null);
        return "{\"ok\":true,\"action\":\"run\"}";
    }

    private string HealthJson()
    {
        var sim = MainSim.Inst;
        return "{\"ok\":true,\"plugin\":\"TFWR Bridge\",\"version\":\"0.1.0\",\"gameLoaded\":" + (sim != null ? "true" : "false") + "}";
    }

    private string StateJson()
    {
        var sim = MainSim.Inst;
        var sb = new StringBuilder("{\"ok\":true,\"gameLoaded\":");
        sb.Append(sim != null ? "true" : "false");
        if (sim == null) return sb.Append('}').ToString();

        sb.Append(",\"inventory\":").Append(InventoryArray(sim));
        sb.Append(",\"unlocks\":").Append(UnlockLevels(sim));
        sb.Append(",\"simulation\":{");
        var simulation = GetField(sim, "sim");
        sb.Append("\"paused\":").Append(JsonBool(GetProperty(simulation, "Paused")));
        sb.Append(",\"currentTime\":").Append(JsonNumber(GetProperty(simulation, "CurrentTime")));
        sb.Append(",\"speedFactor\":").Append(JsonNumber(GetProperty(simulation, "SpeedFactor")));
        sb.Append("}");
        sb.Append(",\"grid\":").Append(GridArray(sim));
        sb.Append(",\"catalogSummary\":{\"items\":").Append(Count(ResourceManager.GetAllItems()));
        sb.Append(",\"unlocks\":").Append(Count(ResourceManager.GetAllUnlocks()));
        sb.Append(",\"farmObjects\":").Append(Count(ResourceManager.GetAllFarmObjects())).Append('}');
        return sb.Append('}').ToString();
    }

    private string InventoryJson()
    {
        var sim = MainSim.Inst;
        return "{\"ok\":true,\"gameLoaded\":" + (sim != null ? "true" : "false") + ",\"items\":" + (sim == null ? "[]" : InventoryArray(sim)) + "}";
    }

    private string InventoryArray(MainSim sim)
    {
        var items = ResourceManager.GetAllItems();
        var sb = new StringBuilder("[");
        var first = true;
        foreach (var item in items ?? Enumerable.Empty<ItemSO>())
        {
            var id = Convert.ToInt32(GetField(item, "itemId"));
            double amount;
            try { amount = sim.GetNumItem(id); } catch { continue; }
            if (Math.Abs(amount) < 0.0000001) continue;
            if (!first) sb.Append(',');
            first = false;
            sb.Append("{\"id\":").Append(id);
            sb.Append(",\"name\":").Append(JsonString(GetField(item, "itemName")));
            sb.Append(",\"amount\":").Append(JsonNumber(amount)).Append('}');
        }
        return sb.Append(']').ToString();
    }

    private string UnlocksJson()
    {
        var sim = MainSim.Inst;
        var sb = new StringBuilder("{\"ok\":true,\"gameLoaded\":");
        sb.Append(sim != null ? "true" : "false").Append(",\"levels\":");
        sb.Append(sim == null ? "{}" : UnlockLevels(sim));
        sb.Append(",\"catalog\":").Append(UnlockCatalog(sim));
        return sb.Append('}').ToString();
    }

    private string UnlockLevels(MainSim sim)
    {
        var values = sim.GetUnlocks();
        var sb = new StringBuilder("{");
        var first = true;
        foreach (var pair in values ?? new Dictionary<string, int>())
        {
            if (!first) sb.Append(',');
            first = false;
            sb.Append(JsonString(pair.Key)).Append(':').Append(pair.Value);
        }
        return sb.Append('}').ToString();
    }

    private string UnlockCatalog(MainSim sim)
    {
        var sb = new StringBuilder("[");
        var first = true;
        foreach (var unlock in ResourceManager.GetAllUnlocks() ?? Enumerable.Empty<UnlockSO>())
        {
            if (!first) sb.Append(',');
            first = false;
            sb.Append("{\"name\":").Append(JsonString(GetField(unlock, "unlockName")));
            sb.Append(",\"description\":").Append(JsonString(GetField(unlock, "description")));
            sb.Append(",\"docs\":").Append(JsonString(GetField(unlock, "docs")));
            sb.Append(",\"parent\":").Append(JsonString(GetField(unlock, "parentUnlock")));
            sb.Append(",\"maxLevel\":").Append(JsonNumber(GetField(unlock, "maxUnlockLevel")));
            sb.Append(",\"cost\":").Append(CostJson(sim, unlock)).Append('}');
        }
        return sb.Append(']').ToString();
    }

    private string CatalogJson()
    {
        var sb = new StringBuilder("{\"ok\":true,\"items\":[");
        var first = true;
        foreach (var item in ResourceManager.GetAllItems() ?? Enumerable.Empty<ItemSO>())
        {
            if (!first) sb.Append(',');
            first = false;
            sb.Append("{\"id\":").Append(JsonNumber(GetField(item, "itemId")));
            sb.Append(",\"name\":").Append(JsonString(GetField(item, "itemName")));
            sb.Append(",\"description\":").Append(JsonString(GetField(item, "description")));
            sb.Append(",\"docs\":").Append(JsonString(GetField(item, "docs"))).Append('}');
        }
        sb.Append("],\"farmObjects\":[");
        first = true;
        foreach (var farmObject in ResourceManager.GetAllFarmObjects() ?? Enumerable.Empty<FarmObjectSO>())
        {
            if (!first) sb.Append(',');
            first = false;
            sb.Append("{\"name\":").Append(JsonString(GetField(farmObject, "objectName")));
            sb.Append(",\"className\":").Append(JsonString(GetField(farmObject, "className")));
            sb.Append(",\"description\":").Append(JsonString(GetField(farmObject, "description")));
            sb.Append(",\"docs\":").Append(JsonString(GetField(farmObject, "docs"))).Append('}');
        }
        return sb.Append("]}").ToString();
    }

    private string GridJson()
    {
        var sim = MainSim.Inst;
        return "{\"ok\":true,\"gameLoaded\":" + (sim != null ? "true" : "false") + ",\"grid\":" + (sim == null ? "{}" : GridArray(sim)) + "}";
    }

    private string GridArray(MainSim sim)
    {
        var simulation = GetField(sim, "sim");
        var farm = GetField(simulation, "farm");
        var grid = GetField(farm, "grid");
        var sb = new StringBuilder("{\"entities\":");
        sb.Append(ObjectMapJson(GetField(grid, "entities")));
        sb.Append(",\"grounds\":").Append(ObjectMapJson(GetField(grid, "grounds")));
        sb.Append(",\"drones\":").Append(DronesJson(farm));
        return sb.Append('}').ToString();
    }

    private string DronesJson(object farm)
    {
        var list = GetField(farm, "drones") as IEnumerable;
        var sb = new StringBuilder("[");
        var first = true;
        if (list != null)
        {
            foreach (var drone in list)
            {
                if (!first) sb.Append(',');
                first = false;
                var position = GetField(drone, "pos");
                sb.Append("{\"id\":").Append(JsonNumber(GetProperty(drone, "DroneId")));
                sb.Append(",\"position\":").Append(Vector2Json(position));
                sb.Append(",\"state\":").Append(JsonString(GetField(drone, "droneState"))).Append('}');
            }
        }
        return sb.Append(']').ToString();
    }

    private string ObjectMapJson(object map)
    {
        var dictionary = map as IDictionary;
        var sb = new StringBuilder("[");
        var first = true;
        if (dictionary != null)
        {
            foreach (DictionaryEntry entry in dictionary)
            {
                if (!first) sb.Append(',');
                first = false;
                var value = entry.Value;
                var objectSo = GetField(value, "objectSO");
                sb.Append("{\"position\":").Append(Vector2Json(entry.Key));
                sb.Append(",\"name\":").Append(JsonString(GetField(objectSo, "objectName")));
                sb.Append(",\"className\":").Append(JsonString(GetField(objectSo, "className")));
                sb.Append(",\"harvestable\":").Append(JsonBool(GetProperty(value, "Harvestable")));
                sb.Append(",\"grownPercent\":").Append(JsonNumber(GetProperty(value, "GrownPercent"))).Append('}');
            }
        }
        return sb.Append(']').ToString();
    }

    private string CostJson(MainSim sim, UnlockSO unlock)
    {
        try { return ItemBlockJson(sim.GetUnlockCost(unlock)); }
        catch { return "[]"; }
    }

    private string ItemBlockJson(object block)
    {
        var values = GetField(block, "items") as Array;
        var sb = new StringBuilder("[");
        var first = true;
        if (values != null)
        {
            for (var i = 0; i < values.Length; i++)
            {
                var amount = Convert.ToDouble(values.GetValue(i));
                if (Math.Abs(amount) < 0.0000001) continue;
                var item = ResourceManager.GetItem(i);
                if (!first) sb.Append(',');
                first = false;
                sb.Append("{\"id\":").Append(i);
                sb.Append(",\"name\":").Append(JsonString(GetField(item, "itemName")));
                sb.Append(",\"amount\":").Append(JsonNumber(amount)).Append('}');
            }
        }
        return sb.Append(']').ToString();
    }

    private static object GetField(object value, string name)
    {
        if (value == null) return null;
        var type = value.GetType();
        while (type != null)
        {
            var field = type.GetField(name, BindingFlags.Public | BindingFlags.NonPublic | BindingFlags.Instance | BindingFlags.Static);
            if (field != null) return field.GetValue(value);
            type = type.BaseType;
        }
        return null;
    }

    private static object GetProperty(object value, string name)
    {
        if (value == null) return null;
        var type = value.GetType();
        while (type != null)
        {
            var property = type.GetProperty(name, BindingFlags.Public | BindingFlags.NonPublic | BindingFlags.Instance | BindingFlags.Static);
            if (property != null && property.GetMethod != null)
            {
                try { return property.GetValue(value, null); } catch { return null; }
            }
            type = type.BaseType;
        }
        return null;
    }

    private static int Count(IEnumerable values)
    {
        if (values == null) return 0;
        var count = 0;
        foreach (var ignored in values) count++;
        return count;
    }

    private static string Vector2Json(object value)
    {
        if (value == null) return "null";
        return "{\"x\":" + JsonNumber(GetProperty(value, "x")) + ",\"y\":" + JsonNumber(GetProperty(value, "y")) + "}";
    }

    private static string JsonString(object value)
    {
        if (value == null) return "null";
        var text = Convert.ToString(value) ?? string.Empty;
        var sb = new StringBuilder("\"");
        foreach (var ch in text)
        {
            switch (ch)
            {
                case '\\': sb.Append("\\\\"); break;
                case '"': sb.Append("\\\""); break;
                case '\n': sb.Append("\\n"); break;
                case '\r': sb.Append("\\r"); break;
                case '\t': sb.Append("\\t"); break;
                default: sb.Append(ch); break;
            }
        }
        return sb.Append('"').ToString();
    }

    private static string JsonBool(object value)
    {
        return value is bool boolean ? (boolean ? "true" : "false") : "false";
    }

    private static string JsonNumber(object value)
    {
        if (value == null) return "0";
        if (value is Enum) return JsonString(value);
        if (value is IFormattable formattable) return formattable.ToString(null, System.Globalization.CultureInfo.InvariantCulture);
        return "0";
    }

    private static string ErrorJson(string message)
    {
        return "{\"ok\":false,\"error\":" + JsonString(message) + "}";
    }
}
