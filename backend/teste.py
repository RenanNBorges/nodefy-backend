import psycopg

conn = psycopg.connect("postgres://admin:eOMgkBQhhbVIyqJ2J8pmRJQaCKYwZGyZ@dpg-clrgpd2e9h4c73b03d70-a.oregon-postgres.render.com/nodefy")

with conn.cursor() as cursor:
    cursor.execute("SELECT * FROM users")
    print(cursor.fetchall())