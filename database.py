import sqlite3

con = sqlite3.connect('results.sqlite')
cur = con.cursor()
cur.execute("""
create table if not exists RECORDS (
    level text,
    score integer    
)""")
cur.execute("""
    INSERT INTO records(level, score) VALUES(1, 0)
    """)
cur.execute("""
    INSERT INTO records(level, score) VALUES(2, 0)
    """)
cur.execute("""
    INSERT INTO records(level, score) VALUES(3, 0)
    """)

con.commit()

def insert_into(level, score):
    con = sqlite3.connect('results.sqlite')
    cur = con.cursor()
    cur.execute("""
    INSERT INTO records(level, score) VALUES({level}, {score})
    """.format(level=level, score=score))
    con.commit()


def get_all_results():
    con = sqlite3.connect('results.sqlite')
    cur = con.cursor()
    result = cur.execute("""
        SELECT level, max(score) Score from Records
        GROUP by score
        ORDER by score DESC
        limit 10
        """).fetchall()
    return result


def get_result(level):
    s = ''
    con = sqlite3.connect('results.sqlite')
    cur = con.cursor()
    result = cur.execute("""
    SELECT level, max(score) Score from Records
    WHERE level = {n}
    GROUP by score
    ORDER by score DESC
    limit 3
    """.format(n=level)).fetchall()
    return result[0][1]

cur.close()
