import sqlite3
 
DB_PATH = 'database.db'
 
def dml_ddl(query, params=()):
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute(query, params)
        conn.commit()
        return cursor.rowcount
    except sqlite3.Error as e:
        conn.rollback()
        raise RuntimeError(f"Erro ao executar DML/DDL: {e}")
    finally:
        conn.close()
 
 
def dql_one(query, params=()):
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute(query, params)
        result = cursor.fetchone()
        return dict(result) if result else None
    except sqlite3.Error as e:
        raise RuntimeError(f"Erro ao executar SELECT: {e}")
    finally:
        conn.close()
 
 
def dql_all(query, params=()):
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute(query, params)
        results = cursor.fetchall()
        return [dict(row) for row in results]
    except sqlite3.Error as e:
        raise RuntimeError(f"Erro ao executar SELECT: {e}")
    finally:
        conn.close()
 
 
def executar_script(script_sql):
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.executescript(script_sql)
        conn.commit()
    except sqlite3.Error as e:
        raise RuntimeError(f"Erro ao executar script SQL: {e}")
    finally:
        conn.close()
 
 
if __name__ == "__main__":
    dml_ddl("""
        CREATE TABLE IF NOT EXISTS livros (
            isbn TEXT PRIMARY KEY,
            titulo TEXT,
            autor TEXT
        );
    """)
 
    dml_ddl("INSERT OR IGNORE INTO livros VALUES (?, ?, ?);", ('978-1', 'Dom Casmurro', 'Machado de Assis'))
    dml_ddl("INSERT OR IGNORE INTO livros VALUES (?, ?, ?);", ('978-2', 'Memórias Póstumas', 'Machado de Assis'))
 
    livro = dql_one("SELECT * FROM livros WHERE isbn = ?;", ('978-1',))
    print("Um livro:", livro)
 
    livros = dql_all("SELECT * FROM livros;")
    for l in livros:
        print(l)
 
    afetadas = dml_ddl("UPDATE livros SET autor = ? WHERE isbn = ?;", ('M. de Assis', '978-1'))
    print(f"Linhas atualizadas: {afetadas}")