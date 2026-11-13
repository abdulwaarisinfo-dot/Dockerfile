# Local computer (Windows) pe chalao:  python make_sql.py
# JSON file se seed/data.sql banata ha.
import json, os

SRC = r"C:\Users\ZASS\Downloads\flintel_static_1-8636.json"
DB, TABLE = "flintel_static", "flintel_signals"

os.makedirs("seed", exist_ok=True)
data = json.load(open(SRC, encoding="utf-8"))

# JSON ke andar sab se bari list of objects dhoondo
cands = []
def walk(d, path="root"):
    if isinstance(d, list):
        if d and all(isinstance(x, dict) for x in d[:50]):
            cands.append((path, d))
        for i, x in enumerate(d[:50]):
            walk(x, f"{path}[{i}]")
    elif isinstance(d, dict):
        for k, v in d.items():
            walk(v, f"{path}.{k}")
walk(data)

if not cands:
    raise SystemExit("Koi rows nahi mili")

path, rows = max(cands, key=lambda c: len(c[1]))
cols = []
for r in rows:
    for k in r:
        if k not in cols:
            cols.append(k)

print("Path   :", path)
print("Rows   :", len(rows))
print("Columns:", cols)

def esc(v):
    if v is None: return "NULL"
    if isinstance(v, bool): return "1" if v else "0"
    if isinstance(v, (int, float)): return str(v)
    if isinstance(v, (dict, list)): v = json.dumps(v, ensure_ascii=False)
    return "'" + str(v).replace("\\", "\\\\").replace("'", "''") + "'"

cl = ",".join(f"`{c}`" for c in cols)
with open("seed/data.sql", "w", encoding="utf-8", newline="\n") as f:
    f.write("SET NAMES utf8mb4;\n")
    f.write(f"CREATE DATABASE IF NOT EXISTS `{DB}` CHARACTER SET utf8mb4;\n")
    f.write(f"CREATE TABLE IF NOT EXISTS `{DB}`.`{TABLE}` ({','.join(f'`{c}` LONGTEXT' for c in cols)});\n")
    for i in range(0, len(rows), 500):
        vals = ",\n".join("(" + ",".join(esc(x.get(c)) for c in cols) + ")" for x in rows[i:i+500])
        f.write(f"INSERT INTO `{DB}`.`{TABLE}` ({cl}) VALUES\n{vals};\n")

print("seed/data.sql tayyar ->", os.path.abspath("seed/data.sql"))
