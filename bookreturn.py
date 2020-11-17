import sqlite3
import database as dB
import bookcheckout as bCKO
import datetime as dt

"""Update loan history, with return box being filled with '-'"""
def updateLoanHistoryR(book):
    date = dt.datetime.today().strftime("%m/%d/%Y")
    member = '0'
    returnDate = '-'
    try:
        conn = sqlite3.connect(dB.database)
        c = conn.cursor()
        d = conn.cursor()
        c.execute("UPDATE library SET Member_ID=? WHERE ID=? ",(member,book))
        d.execute("UPDATE loan_history SET Return_date=? WHERE BOOK_ID=? AND Return_date=?",(date,book,returnDate))
    except ValueError as e:
        print(e)
    conn.commit()
    conn.close()

"""Return book"""
def returnBook(book):
    logic = bCKO.bookID(book)
    success = "Book has been returned"
    fail = "Unable to return book"

    if logic == True:
        updateLoanHistoryR(book)
        result = success
    else:
        result = fail
        
    return result
        
