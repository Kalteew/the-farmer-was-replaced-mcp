# Instructions du projet

- Le dépôt public est `https://github.com/Kalteew/the-farmer-was-replaced-mcp`.
- Chaque problème rencontré pendant le développement doit devenir une méthode MCP réutilisable quand c'est pertinent.
- Après chaque modification : vérifier le serveur avec `node --check src/server.mjs` et, si le pont C# est concerné, lancer `dotnet build bridge/TFWRBridge/TFWRBridge.csproj --nologo`.
- Quand les vérifications passent, committer et pousser automatiquement sur `origin/main`.
- Ne jamais publier `node_modules`, `.deps`, `bin`, `obj`, `.mcp-cache`, des sauvegardes locales, des journaux ou des secrets.
