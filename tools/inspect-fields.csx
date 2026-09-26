using System;
using System.IO;
using System.Linq;
using System.Reflection;

var gameRoot = Environment.GetEnvironmentVariable("TFWR_GAME_ROOT")
    ?? Path.Combine(Environment.GetFolderPath(Environment.SpecialFolder.ProgramFilesX86), "Steam", "steamapps", "common", "The Farmer Was Replaced");
var managed = Path.Combine(gameRoot, "TheFarmerWasReplaced_Data", "Managed");
foreach (var name in new[] { "Core.dll", "NewAssembly.dll", "Utils.dll", "UnityEngine.CoreModule.dll" })
    Assembly.LoadFrom(Path.Combine(managed, name));

var scriptArgs = new[] { "SaveChooser", "SaveOption" };
var names = scriptArgs.Length == 0
    ? new[] { "MainSim", "Farm", "Inventory", "ResourceManager", "Drone", "GridManager", "Saver", "Workspace", "Simulation", "Execution" }
    : scriptArgs;

var assemblies = AppDomain.CurrentDomain.GetAssemblies();
foreach (var name in names)
{
    var type = assemblies.Where(a => a.GetName().Name is "Core" or "NewAssembly" or "Utils").SelectMany(a =>
    {
        try { return a.GetTypes(); } catch { return Array.Empty<Type>(); }
    }).FirstOrDefault(t => t.Name == name);

    if (type == null)
    {
        Console.WriteLine($"TYPE {name} NOT FOUND");
        continue;
    }

    Console.WriteLine($"TYPE {type.FullName} ASSEMBLY {type.Assembly.GetName().Name}");
    foreach (var field in type.GetFields(BindingFlags.Public | BindingFlags.NonPublic | BindingFlags.Static | BindingFlags.Instance | BindingFlags.DeclaredOnly))
        Console.WriteLine($"  FIELD {(field.IsStatic ? "static " : "")}{field.FieldType.FullName} {field.Name}");
    foreach (var prop in type.GetProperties(BindingFlags.Public | BindingFlags.NonPublic | BindingFlags.Static | BindingFlags.Instance | BindingFlags.DeclaredOnly))
        Console.WriteLine($"  PROP {prop.PropertyType.FullName} {prop.Name} get={prop.GetMethod != null} set={prop.SetMethod != null}");
    foreach (var ctor in type.GetConstructors(BindingFlags.Public | BindingFlags.NonPublic | BindingFlags.Instance | BindingFlags.Static | BindingFlags.DeclaredOnly))
        Console.WriteLine($"  CTOR {ctor}");
}
