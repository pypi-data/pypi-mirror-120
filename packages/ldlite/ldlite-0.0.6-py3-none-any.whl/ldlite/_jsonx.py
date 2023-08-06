import json
import sys

from tqdm import tqdm

from ._camelcase import _decode_camel_case
from ._sqlx import _escape_sql
from ._sqlx import _sqlid

def _compile_attrs(table, jdict, newattrs, level):
    if level > 2:
        return
    for k, v in jdict.items():
        if k is None or v is None:
            continue
        if isinstance(v, dict):
            _compile_attrs(table+"_"+k, v, newattrs, level+1)
        elif isinstance(v, list):
            # TODO array
            pass
        elif isinstance(v, bool):
            if table not in newattrs:
                newattrs[table] = {"id": ("id", "varchar")}
            if k not in newattrs[table]:
                newattrs[table][k] = (_decode_camel_case(k), "boolean")
        elif isinstance(v, int):
            if table not in newattrs:
                newattrs[table] = {"id": ("id", "varchar")}
            if k not in newattrs[table]:
                newattrs[table][k] = (_decode_camel_case(k), "integer")
        else:
            if table not in newattrs:
                newattrs[table] = {"id": ("id", "varchar")}
            if k not in newattrs[table] or newattrs[table][k] != "varchar":
                newattrs[table][k] = (_decode_camel_case(k), "varchar")

def _transform_data(db, table, jdict, newattrs, level, record_id, row_ids):
    if level > 2:
        return
    if record_id is None and "id" in jdict:
        rec_id = jdict["id"]
    rowdict = {}
    for k, v in jdict.items():
        if k is None:
            continue
        if isinstance(v, dict):
            _transform_data(db, table+"_"+k, v, newattrs, level+1, rec_id, row_ids)
        elif isinstance(v, list):
            # TODO array
            pass
        if k not in newattrs[table]:
            continue
        decoded_attr, dtype = newattrs[table][k]
        if dtype == "integer":
            rowdict[decoded_attr] = str(v)
        elif dtype == "boolean":
            rowdict[decoded_attr] = "TRUE" if v else "FALSE"
        else:
            rowdict[decoded_attr] = "'"+str(v)+"'"
    row = list(rowdict.items())
    if "id" not in jdict and record_id is not None:
        row.append( ("id", "'"+record_id+"'") )
    q = "INSERT INTO "+_sqlid(table)+"(__id,"
    q += ",".join([_sqlid(kv[0]) for kv in row])
    q += ")VALUES(" + str(row_ids[table]) + ","
    q += ",".join([kv[1] for kv in row])
    q += ")"
    cur = db.cursor()
    cur.execute(q)
    row_ids[table] += 1

def _transform_json(db, table, total, quiet):
    # Scan all fields for JSON data
    # First get a list of the string attributes
    cur = db.cursor()
    cur.execute("SELECT * FROM \""+table+"\" LIMIT 1")
    str_attrs = set()
    for a in cur.description:
        if a[1] == "STRING" or a[1] == 1043:
            str_attrs.add(a[0])
    # Scan data for JSON objects
    str_attr_list = list(str_attrs)
    cur = db.cursor()
    cur.execute("SELECT "+",".join([_sqlid(a) for a in str_attr_list])+" FROM "+_sqlid(table))
    json_attrs = set()
    newattrs = {}
    while True:
        row = cur.fetchone()
        if row == None:
            break
        for i, data in enumerate(row):
            if data is None:
                continue
            d = data.strip()
            if len(d) == 0 or d[0] != "{":
                continue
            try:
                jdict = json.loads(d)
            except ValueError as e:
                continue
            json_attrs.add(str_attr_list[i])
            _compile_attrs(table+"_j", jdict, newattrs, 1)
    # Create table schemas
    cur = db.cursor()
    for t, attrs in newattrs.items():
        cur.execute("DROP TABLE IF EXISTS "+_sqlid(t))
        cur.execute("CREATE TABLE "+_sqlid(t)+"(__id integer)")
        cur.execute("ALTER TABLE "+_sqlid(t)+" ADD COLUMN id varchar")
        for attr in sorted(list(attrs)):
            if attr == "id":
                continue
            decoded_attr, dtype = attrs[attr]
            cur.execute("ALTER TABLE "+_sqlid(t)+" ADD COLUMN "+_sqlid(decoded_attr)+" "+dtype)
    # Set all row IDs to 1
    row_ids = {}
    for t in newattrs.keys():
        row_ids[t] = 1
    # Run transformation
    # Select only JSON columns
    json_attr_list = list(json_attrs)
    cur = db.cursor()
    cur.execute("SELECT "+",".join([_sqlid(a) for a in json_attr_list])+" FROM "+_sqlid(table)+"")
    if not quiet:
        pbar = tqdm(total=total)
        pbartotal = 0
    while True:
        row = cur.fetchone()
        if row == None:
            break
        for i, data in enumerate(row):
            if data is None:
                continue
            d = data.strip()
            if len(d) == 0 or d[0] != "{":
                continue
            try:
                jdict = json.loads(d)
            except ValueError as e:
                continue
            _transform_data(db, table+"_j", jdict, newattrs, 1, None, row_ids)
        if not quiet:
            pbartotal += 1
            pbar.update(1)
    if not quiet:
        pbar.close()
    return sorted(newattrs.keys())

