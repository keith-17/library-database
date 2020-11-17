import sqlite3
import database as dB
import datetime as dt

#IS the member ID valid returns boolean outcome
def memberID(term):
    try:
        conn = sqlite3.connect(dB.database)
        c = conn.cursor()
        c.execute("SELECT * FROM library WHERE Member_ID=?",(term,))
        result = str(c.fetchall())
    except ValueError as e:
        print(e)
    conn.close()

    if result == "[]":
        query = False
    else:
        query = True
    return query

#is the book valid  BOOLean outcome
def bookID(term):
    try: 
        conn = sqlite3.connect(dB.database)
        c = conn.cursor()
        c.execute("SELECT ID FROM library WHERE ID=?",(term,))
        result = str(c.fetchall())
    except ValueError as e:
        print(e)
    conn.close()

    if result == "[]":
        query = False
    else:
        query = True
    return query

#is it available BOOLean outcome
def available(term):
    try:
        conn = sqlite3.connect(dB.database)
        c = conn.cursor()
        c.execute("SELECT * FROM library WHERE ID=?",(term,))
        result = str(c.fetchall())
        result = dB.convList(result)
    except ValueError as e:
        print(e)
    conn.close()
    
    if result[-1] == '0':
        query = True
    else:
        query = False
    return query

#can it be taken out? BOOLean outcome, using the last 3 functions for its truth table functionality
def parameters(member,book):
    logic1 = memberID(member)
    logic2 = bookID(book)
    logic3 = available(book)

    if logic1 == True and logic2 == True:
        if logic3 == True:
            result = True
        else:
            result = False
    else:
        result = False
    return result

#this function will just run, when a previous condition is satisfied
def updateTables(member,book):
    
    date = dt.datetime.today().strftime("%m/%d/%Y")
    loanHistoryList = [book,date,'-',member]

    try:
        conn = sqlite3.connect(dB.database)
        c = conn.cursor()
        d = conn.cursor()
        c.execute("UPDATE library SET Member_ID=? WHERE ID=? ",(member,book))
        d.execute("INSERT INTO loan_history (BOOK_ID,Checkout_date, Return_date,Member_ID) VALUES(?,?,?,?)",(loanHistoryList[0],loanHistoryList[1],loanHistoryList[2],loanHistoryList[3]))
    except ValueError as e:
        print(e)
    conn.commit()
    conn.close()

#This function is the bulk of this module, message is returned to the label in the gui
def checkingBookOut(member, book):
    good = ['It is has updated']
    bad = ['Unable to update']
    logic = parameters(member,book)
    
    if logic == True:       
        updateTables(member,book)
        result = good
    else:
        result = bad
        
    return result
    
