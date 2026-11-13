#!/bin/bash
# Render Shell ma chalao:  bash /seed/import.sh
# Sirf EK baar chalana, warna rows duplicate ho jayengi.

if [ ! -f /seed/data.sql ]; then
  echo "/seed/data.sql nahi mili. Pehle make_sql.py chala ke push karo."
  exit 1
fi

COUNT=$(mysql -u root -p"$MYSQL_ROOT_PASSWORD" -N -e "SELECT COUNT(*) FROM flintel_static.flintel_signals;" 2>/dev/null)
if [ -n "$COUNT" ] && [ "$COUNT" != "0" ] && [ "$FORCE" != "1" ]; then
  echo "Table ma pehle se $COUNT rows hain. Insert nahi kiya."
  echo "Phir bhi karna ho to:  FORCE=1 bash /seed/import.sh"
  exit 1
fi

mysql -u root -p"$MYSQL_ROOT_PASSWORD" --default-character-set=utf8mb4 < /seed/data.sql \
  && mysql -u root -p"$MYSQL_ROOT_PASSWORD" -e "SELECT COUNT(*) AS total FROM flintel_static.flintel_signals;"
