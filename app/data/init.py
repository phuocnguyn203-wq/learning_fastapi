import os
from pathlib import Path
from sqlite3 import connect, Connection, Cursor

_conn: Connection | None = None
_curs: Cursor | None = None

def get_db(name: str | None = None, reset: bool = True) -> tuple[Connection, Cursor]:
    global _conn, _curs
    if _conn is not None and _curs is not None and not reset:
        return _conn, _curs
    
    if _conn is not None:
        _conn.close()
    
    if name is None:
        top_dir = Path(__file__).resolve().parents[1]
        db_path = top_dir / 'db' / 'cryptid.db'
        name = os.getenv('CRYPTID_SQLITE_DB', str(db_path))
    
    if name != ':memory:':
        Path(name).expanduser().parent.mkdir(parents=True, exist_ok=True)

    _conn = connect(name, check_same_thread=False)
    _curs = _conn.cursor()
    return (_conn, _curs)

conn, curs = get_db()
