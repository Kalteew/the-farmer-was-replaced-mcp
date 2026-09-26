using System;
using System.IO;
using System.Linq;
using System.Reflection;

var gameRoot = Environment.GetEnvironmentVariable("TFWR_GAME_ROOT")
    ?? Path.Combine(Environment.GetFolderPath(Environment.SpecialFolder.ProgramFilesX86), "Steam", "steamapps", "common", "The Farmer Was Replaced");
var managed = Path.Combine(gameRoot, "TheFarmerWasReplaced_Data", "Managed");
foreach (var name in new[] { "Core.dll", "NewAssembly.dll" })
{
    var assembly = Assembly.LoadFrom(Path.Combine(managed, name));
    Console.WriteLine($"ASSEMBLY {assembly.FullName}");
    foreach (var type in assembly.GetTypes().OrderBy(t => t.FullName))
    {
        Console.WriteLine(type.FullName);
        foreach (var method in type.GetMethods(BindingFlags.Public | BindingFlags.NonPublic | BindingFlags.Static | BindingFlags.Instance | BindingFlags.DeclaredOnly).OrderBy(m => m.Name))
        {
            if (method.Name.Contains("Save", StringComparison.OrdinalIgnoreCase) ||
                method.Name.Contains("Item", StringComparison.OrdinalIgnoreCase) ||
                method.Name.Contains("Drone", StringComparison.OrdinalIgnoreCase) ||
                method.Name.Contains("Execute", StringComparison.OrdinalIgnoreCase) ||
                method.Name.Contains("Farm", StringComparison.OrdinalIgnoreCase) ||
                method.Name.Contains("Game", StringComparison.OrdinalIgnoreCase) ||
                method.Name.Contains("Unlock", StringComparison.OrdinalIgnoreCase) ||
                method.Name.Contains("Code", StringComparison.OrdinalIgnoreCase))
                Console.WriteLine($"  {method}");
        }
    }
}
