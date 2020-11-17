import sqlite3
import database as dB

"""This function fetches specific title from data base"""
def query(term):
    try:
        conn = sqlite3.connect(dB.database)
        c = conn.cursor()
        c.execute("SELECT * FROM library WHERE Title=?",(term,))
        result = str(c.fetchall())
    except RuntimeError as e:
        print(e)
    conn.close()
    return result

"""This function used by gui to insert ziped list into the box"""
def bookQuery(term):
    listTitle = query(term)
    fail = ['Book not found', 'Try again']

    if listTitle == '[]':
        result = fail
    else:        
        listTitle = dB.convList(listTitle)
        result = [i + j for i, j in zip(dB.listInfoLib, listTitle)]

    return result

