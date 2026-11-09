import argparse,sqlite3,tempfile
from pathlib import Path

def setup(source,target):
    with sqlite3.connect(source) as c:
        c.execute('CREATE TABLE IF NOT EXISTS transactions (id INTEGER PRIMARY KEY, updated_at TEXT NOT NULL, amount REAL NOT NULL)')
    with sqlite3.connect(target) as c:
        c.execute('CREATE TABLE IF NOT EXISTS transactions (id INTEGER PRIMARY KEY, updated_at TEXT NOT NULL, amount REAL NOT NULL)')
        c.execute('CREATE TABLE IF NOT EXISTS watermark (id INTEGER PRIMARY KEY CHECK(id=1), updated_at TEXT, record_id INTEGER)')
        c.execute("INSERT OR IGNORE INTO watermark VALUES (1,'',0)")

def synchronize(source,target):
    setup(source,target)
    with sqlite3.connect(target) as dst,sqlite3.connect(source) as src:
        ts,rid=dst.execute('SELECT updated_at,record_id FROM watermark WHERE id=1').fetchone()
        rows=src.execute('SELECT id,updated_at,amount FROM transactions WHERE (updated_at > ?) OR (updated_at = ? AND id > ?) ORDER BY updated_at,id',(ts,ts,rid)).fetchall()
        for ident,updated,amount in rows:
            dst.execute('INSERT INTO transactions VALUES (?,?,?) ON CONFLICT(id) DO UPDATE SET updated_at=excluded.updated_at,amount=excluded.amount',(ident,updated,amount))
            ts,rid=updated,ident
        if rows:
            dst.execute('UPDATE watermark SET updated_at=?,record_id=? WHERE id=1',(ts,rid))
        return len(rows)

def demo():
    with tempfile.TemporaryDirectory() as d:
        s,t=(str(Path(d)/x) for x in ('source.db','target.db'))
        setup(s,t)
        with sqlite3.connect(s) as c:
            c.executemany('INSERT INTO transactions VALUES (?,?,?)',[(1,'2026-01-01T10:00:00Z',12.5),(2,'2026-01-01T10:01:00Z',25.0)])
        return {'first_run':synchronize(s,t),'rerun':synchronize(s,t)}

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--demo',action='store_true');a=p.parse_args()
    if a.demo:print(demo())
