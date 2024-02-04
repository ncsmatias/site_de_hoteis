import sqlite3

connection = sqlite3.connect('hoteis.db')
cursor = connection.cursor()

table = '''CREATE TABLE IF NOT EXISTS hoteis (
          id int PRIMARY KEY, nome text, estrelas real, valor_diaria real, cidade text)'''

hotel = '''INSERT INTO hoteis 
          VALUES (1, 'Ibis - Conforty', 5, 120, 'São Paulo')'''

cursor.execute(table)
cursor.execute(hotel)

connection.commit()
connection.close()