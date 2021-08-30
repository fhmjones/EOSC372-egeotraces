# steps to deploy on eoastest5.xyz:8000

1. `ssh n3jov`
2. `cd ~/repos/ocgy-dataviewr`
3. git fetch and update raw branch __(be sure about using either `origin` or `upstream`)__ (in this case, FJ's repo is `upstream`)
   - `git fetch https://github.com/fhmjones/ocgy-dataviewer raw` ("raw" is the branch being used on eoastest5.xyz)
   - If you do not care about the jovyan code: `git reset --hard upstream/raw`
   - If there is a change on jovyan you want to keep: `git rebase upstream/raw`
   - Use `git diff --name-only upstream/raw` or `git diff upstream/raw` to check difference between current and "fetched" branch.
4. `docker-compose build ocgy_dash`
5. `docker-compose down`
6. `docker-compose up -d`
