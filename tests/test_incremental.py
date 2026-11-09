import sqlite3,tempfile,sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from incremental import setup,synchronize
class TestIncremental(unittest.TestCase):
    def test_watermark(self):
        with tempfile.TemporaryDirectory() as d:
            s,t=Path(d)/'s.db',Path(d)/'t.db'
            setup(s,t)
            with sqlite3.connect(s) as c:c.executemany('INSERT INTO transactions VALUES (?,?,?)',[(1,'2026-01-01',3),(2,'2026-01-01',5)])
            self.assertEqual(synchronize(s,t),2)
            self.assertEqual(synchronize(s,t),0)
