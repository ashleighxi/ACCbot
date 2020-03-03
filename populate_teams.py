from __future__ import print_function
from datetime import date, datetime, timedelta
import mysql.connector

cnx = mysql.connector.connect(user='', password='', database='acc_league')
cursor = cnx.cursor()


add_team = ("INSERT INTO teams "
               "(team_id, team_name, matches_won, matches_lost) "
               "VALUES (%s, %s, %s, %s)")


team_data = [
    ('676582967400726559', 'Clemson', 0, 0),
    ('676582918289621022', 'Florida State', 0, 0),
    ('676582917534777345', 'Louisville', 0, 0),
    ('676582519923015683', 'NC State', 0, 0),
    ('676582522259243008', 'Syracuse', 0, 0),
    ('676582971704213564', 'Georgia Tech', 0, 0),
    ('676582518711123969', 'North Carolina', 0, 0),
    ('676582521970098197', 'Pittsburgh', 0, 0),
    ('676582522909360133', 'Virginia', 0, 0),
    ('676582294814851082', 'Virginia Tech', 0, 0)
]

# Insert new team
cursor.executemany(add_team, team_data)

# Make sure data is committed to the database
cnx.commit()
print(cursor.rowcount, "was inserted")

cursor.close()
cnx.close()
