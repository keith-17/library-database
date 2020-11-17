import sqlite3
import os
import time

"""strings of common variables used throughout"""
database = r"C:\Users\maran\OneDrive - Loughborough University\COP501\coursework\library.db"
libraryData = "libraryBooks.txt"
loanData = "loan_historyExample.txt"
listInfoLib = ['BOOK ID: ','ISBN: ','Title: ','Author: ','Date: ','Member ID: ']

"""converts a list of tuples"""
def convList(test):
    test = ''.join(test)
    test = test[2:]
    test = test[:-2]
    test = test.replace("'","")
    test = "[" + test + "]"
    test = test.strip('][').split(',')
    test = [x.strip(' ') for x in test]
    return test

"""converts loan history to be formatted appropiatley"""
def convLoanHistory(oldHistory):
    i = 0
    newList = []
    length = len(oldHistory)
    while i < length:  
        tuple1 = oldHistory[i]
        tuple1 = tuple1[1:-1]
        tuple1 = tuple1.replace("'","")
        string1 = tuple1.replace(" ","")
        string1 = "[" + string1 + "]"
        list1 = string1.strip('][').split(',')
        list1 = [x.strip(' ') for x in list1]
        i += 1

        newList.append(list1)
        
    return newList

"""Creates library table"""
def create_tableLibrary(obj1):
    obj1.execute("""CREATE TABLE IF NOT EXISTS library(
            ID INTEGER PRIMARY KEY,
            ISBN text,
            Title text,
            Author text,
            Purchase_date text,
            Member_ID text)""")

"""creates loan history table"""
def create_tableHistory(obj1):
    obj1.execute("""CREATE TABLE IF NOT EXISTS loan_history(
            TRANSACTION_ID INTEGER PRIMARY KEY,
            BOOK_ID INTEGER,         
            Checkout_date text,
            Return_date text,
            Member_ID text)""")

"""single function that simulatenously runs table creation functions"""
def createTable():
    try: 
        conn = sqlite3.connect(database)
        c = conn.cursor()
        create_tableLibrary(c)
        create_tableHistory(c)
        conn.commit()
    except ValueError as e:
        print(e)
    conn.close()

"""Function created for the use of unit testing and debugging"""
def showTables():
    try:
        conn = sqlite3.connect(database)
        c = conn.cursor()
        d = conn.cursor()
        c.execute("SELECT * FROM library")
        d.execute("SELECT * FROM loan_history")
        conn.commit()
    except ValueError as e:
        print(e)
    """for terminal debugging"""
    print(c.fetchall())
    print(d.fetchall())
    conn.close()

"""function created for the use of abstraction"""
def insert_funcLibrary(obj1, dataList):    
    obj1.execute("INSERT OR IGNORE INTO library (ISBN,Title,Author,Purchase_date,Member_ID) VALUES (?,?,?,?,?)",dataList)

"""Populates library"""
def populateLibrary(textName,obj1):
    with open(textName) as infile:
        for line in infile:
            data = line.strip()
            data = data.split(",")
            insert_funcLibrary(obj1,data)

"""function created for the use of abstraction"""
def insert_funcHistory(obj1, dataList):
    obj1.execute("INSERT OR IGNORE INTO loan_history (BOOK_ID,Checkout_date, Return_date,Member_ID) VALUES(?,?,?,?)",dataList)

"""Abstracted function to write history into database"""
def populateHistory(textName,obj1):
    with open(textName) as infile:
        for line in infile:
            data = line.strip()
            data = data.split(",")
            insert_funcHistory(obj1,data)

"""populates databases"""
def populateDatabases():
    try:
        conn = sqlite3.connect(database)
        c = conn.cursor()
        populateLibrary(libraryData,c)
        d = conn.cursor()
        populateHistory(loanData,d)
        conn.commit()
    except ValueError as e:
        print(e)
    conn.close()

"""creates loan history list"""
def loanHistoryObject():
    try:
        conn = sqlite3.connect(database)
        c = conn.cursor()
        c.execute("SELECT * FROM loan_history")
        result = c.fetchall()
        list1 = list(map(str,result))
    except ValueError as e:
        print(e)
    conn.close()
    return list1

"""creates library database list"""
def bookCollectionObject():
    try:
        conn = sqlite3.connect(database)
        c = conn.cursor()
        c.execute("SELECT * FROM library")
        result = c.fetchall()
        list1 = list(map(str,result))
    except ValueError as e:
        print(e)
    conn.close()
    return list1

"""can be used to restart project"""
def restart():
    createTable()
    populateDatabases()
    showTables()

def initialiseDB():
    if os.path.exists("library.db"):
        os.remove("library.db")
    else:
        print("the file does not exist")
    time.sleep(0.5)
    createTable()
    populateDatabases()



    
