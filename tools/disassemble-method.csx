#r "../.deps/bepinex-5.4.23.5/package/BepInEx/core/Mono.Cecil.dll"

using System;
using System.Linq;
using Mono.Cecil;
using Mono.Cecil.Cil;

var gameRoot = Environment.GetEnvironmentVariable("TFWR_GAME_ROOT")
    ?? Path.Combine(Environment.GetFolderPath(Environment.SpecialFolder.ProgramFilesX86), "Steam", "steamapps", "common", "The Farmer Was Replaced");
var assembly = AssemblyDefinition.ReadAssembly(Path.Combine(gameRoot, "TheFarmerWasReplaced_Data", "Managed", "Core.dll"));
foreach (var typeName in new[] { "Menu", "SaveChooser" })
{
    var type = assembly.MainModule.GetType(typeName);
    Console.WriteLine($"TYPE {typeName} METHODS: {string.Join(", ", type?.Methods.Select(m => m.Name) ?? Enumerable.Empty<string>())}");
    foreach (var methodName in new[] { "Start", "LoadSave", "Play", "ChooseSave" })
    {
        var method = type?.Methods.FirstOrDefault(m => m.Name == methodName);
        Console.WriteLine($"METHOD {typeName}.{methodName}: {method}");
        if (method == null || !method.HasBody) continue;
        foreach (var instruction in method.Body.Instructions)
            Console.WriteLine($"  {instruction.Offset:X4}: {instruction.OpCode} {instruction.Operand}");
    }
}
