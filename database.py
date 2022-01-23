import sqlite3

con = sqlite3.connect('results.sqlite')
cur = con.cursor()
cur.execute("""
create table if not exists RECORDS (
    name text,
    score integer
)
""")

cur.execute("""
INSERT INTO records(name, score) VALUES('player', 5555)
""")
con.commit()


result = cur.execute("""
SELECT name, max(score) Score from Records
GROUP by score
ORDER by score DESC
limit 3
""").fetchall()

for elem in result:
    print(elem[1])
print(result)

cur.close()