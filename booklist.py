import sqlite3
import database as dB
from datetime import datetime
from itertools import groupby
import matplotlib.pyplot as plt

"""Gets a loan history list, works out the days taken out for each book occurance"""
def cumalativeTimeList(newList):
    length = len(newList)
    i = 0
    dataList = []

    """loops through loan history list, works out dates difference, stops at a null return date"""
    while i < length:
        trial = newList[i]
        firstDate = str(trial[2])
        secondDate = str(trial[3])
        
        if secondDate == '-':
            break
        else:
            #print(secondDate)
            my_date = datetime.strptime(firstDate,"%d/%m/%Y")
            my_date2 = datetime.strptime(secondDate,"%d/%m/%Y")

            delta = my_date2 - my_date
            delta = int(delta.days)
            i+=1
            value = (int(trial[1]),delta)
            dataList.append(value)

    f = lambda x: x[0]
    """Taken from stack overflow! Sorts and zips together list"""
    dataList = sorted([(k, sum(x[1] for x in g)) for k, g in groupby(sorted(dataList, key=f), key=f)], key=lambda x: x[1], reverse=True)
    result = sorted(dataList, key=lambda x:x[0])
    
    return result

"""Organises each distint book in the library by its total time taken by a member"""
def scoreTuples():    
    oldList = dB.loanHistoryObject()

    trialList = dB.convLoanHistory(oldList)

    result = cumalativeTimeList(trialList)

    return result

#counts occurances of each book
def occurancesTuple():
    conn = sqlite3.connect(dB.database)
    c = conn.cursor()
    c.execute("SELECT BOOK_ID, count(BOOK_ID) FROM loan_history GROUP by BOOK_ID ORDER BY BOOK_ID ASC")
    countList = c.fetchall()
    conn.close()

    return countList
"""gets a list of tiles in unassorted order"""
def getTitles():
    try:
        conn = sqlite3.connect(dB.database)
        c = conn.cursor()
        c.execute("SELECT Title FROM library")
        titleList = c.fetchall()
    except ValueError as e:
        print(e)
    conn.close()

    return titleList

#gives weighted average for the popularity of a distinct book
def popularity():
    cumalativeScores = scoreTuples()
    numerator = [x[1] for x in cumalativeScores]
    index = [x[0] for x in cumalativeScores]
    divisor = occurancesTuple()
    divisor = [x[1] for x in divisor]
    output = [i/j for i, j in zip(numerator,divisor)]
    #output = ["%.2f" % x for x in output]
    final = [(index[i],output[i]) for i in range(0, len(index))]

    return final

"""Uses matplot lib library to generate graph of most popular books"""
def graph():
    plt.xlabel("Book ID")
    plt.ylabel("Length of time taken - Days")
    plt.title("Popularity of Books: Weighted Average")
    listTuples = popularity()
    plt.bar(range(len(listTuples)), [val[1] for val in listTuples], align = 'center')
    plt.xticks(range(len(listTuples)),[val[0] for val in listTuples])
    plt.xticks(rotation=70)
    plt.show()

"""This function is used to list the most popular books in descending order, prepared for two lists in the gui"""
def popularityList():
    titles2 = popularity()
    titles1 = getTitles()
    listTuples = [(i,j[1]) for i, j in zip(titles1,titles2)]
    listTuples = sorted(listTuples, key = lambda x:x[1], reverse = True)
    list1, list2 = zip(*listTuples)
    list1 = str(list1)
    list1 = list1[1:-1]
    list1 = list1.replace("'","")
    list1 = list1.replace(",)","")
    list1 = list1.replace("(","")
    list1 = "[" + list1 + "]"
    list1 = list1.strip('][').split(',')
    list2 = list(list2)
    list2 = ["%.1f" % x for x in list2]

    return list1, list2

"""lets the user only see the top n books in the library"""
def popList(n):
    x,y = popularityList()
    var = 'all'
    varUpper = 'All'

    if n == var or n == varUpper:
        pass
    else:
        a = len(x)-n
        x = x[:-a]
        b = len(y)-n
        y = y[:-b]

    return x,y

"""This functionality generates the loan history text file according to the specification"""
def generateLoanText():
    file = r"C:\Users\maran\OneDrive - Loughborough University\COP501\coursework\loan_history.txt"

    oldList = dB.loanHistoryObject()
    trialList = dB.convLoanHistory(oldList)
    i = 0
    length = len(trialList)
    with open(file,'w') as f:
        f.write("Transaction ID | Book ID | Checkout Date | Return Date | Member ID \n")
        while i < length:
            trialList[i] = str(trialList[i])
            trialList[i] = trialList[i].replace("'","")
            trialList[i] = trialList[i].replace("[","")
            trialList[i] = trialList[i].replace("]","")
            f.write("%s \n"%trialList[i])
            i+=1

"""This functionality genereates book info text file"""
def generateBookInfoText():
    file = r"C:\Users\maran\OneDrive - Loughborough University\COP501\coursework\Book_Info.txt"
    oldList = dB.bookCollectionObject()
    length = len(oldList)
    i = 0
    with open(file,'w') as f:
        f.write("ID | ISBN | Title | Author | Purchase Date | Member ID \n")
        while i < length:
            oldList[i] = str(oldList[i])
            oldList[i] = oldList[i].replace("'","")
            oldList[i] = oldList[i].replace("(","")
            oldList[i] = oldList[i].replace(")","")
            f.write("%s \n"%oldList[i])
            i+=1
"""this combines the two text generator files for use in the gui"""
def generateTextFiles():
    try:
        generateLoanText()
        generateBookInfoText()
    except ValueError as e:
        print(e)

def graphKey():
    newList = []
    x,y = popularityList()
    length = len(x)
    i = 0
    j = 1
    while i < length:
        var = "{}:{}".format(j,x[i])
        newList.append(var)
        i+=1
        j+=1

    return newList






