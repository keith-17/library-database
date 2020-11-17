from tkinter import *
from tkinter import Tk
import database as dB
import booksearch as bQ
import bookcheckout as bCKO
import bookreturn as bR
import booklist as bL
from matplotlib.figure import Figure
from PIL import ImageTk, Image

#first window
def create_window1(root):
    window1 = Toplevel(root)
    window1.title("Book Search by Title")
    labelSearch = Label(window1, text = "Search Query: ")
    labelSearch.grid(row=0,column=0)
    titleEntry = Entry(window1)
    titleEntry.grid(row=0,column=1)
    label_2 = Label(window1, text = "Results")
    label_2.grid(row=1,columnspan=2)
    searchList=Listbox(window1,height = 6, width =35)
    searchList.grid(row=2,columnspan=2)

    button_1 = Button(window1,text = "Search", command= lambda: querySearch(titleEntry,searchList))   
    button_1.grid(row=3,columnspan=2)

"""Allows users input to insert results to box"""
def querySearch(titleEntry,searchList):
    titleSearch = titleEntry.get()
    titleResult = bQ.bookQuery(titleSearch)

    for item in titleResult:
        searchList.insert(END,item)

"""Second window"""
def create_window2(root):
    window2 = Toplevel(root)
    window2.title("Loan History")
    
    memberIDlbl = Label(window2, text ="Member ID: ")
    memberIDlbl.grid(row=0,column=0)
    
    bookIDlbl = Label(window2, text = "Book ID: ")
    bookIDlbl.grid(row=1,column=0)
    
    memberEntry = Entry(window2)
    memberEntry.grid(row=0,column=1)
    
    bookEntry = Entry(window2)   
    bookEntry.grid(row=1,column=1)

    label_3 = Label(window2, text = "Result")
    label_3.grid(row=2,columnspan=2)
    
    resBox = Listbox(window2,height = 6, width =35)
    resBox.grid(row=3,columnspan=2)
    
    checkOutBtn = Button(window2, text = "Check Out Book", command=lambda:checkOutBooks(memberEntry,bookEntry,label_3,resBox))
    checkOutBtn.grid(row=4,columnspan=2)   

"""Allows two inputs from the GUI"""
def checkOutBooks(memberEntry, bookEntry,label_3,resBox):
    memberSearch = memberEntry.get()
    bookSearch = bookEntry.get()

    message = bCKO.checkingBookOut(memberSearch,bookSearch)
    label_3["text"]=message

    resList = dB.loanHistoryObject()

    for item in resList:
        resBox.insert(END,item)

"""third window"""
def create_window3(root):
    window3 = Toplevel(root)
    window3.title("Return Books")

    bookIDlbl = Label(window3, text="Book ID:")
    bookIDlbl.grid(row=0,column=0)
    bookEntry = Entry(window3)
    bookEntry.grid(row=0,column=1)

    label_2 = Label(window3,text="Result")
    label_2.grid(row=1,columnspan=2)
    
    label_3 = Label(window3,text="Loan History")
    label_3.grid(row=2,columnspan=2)

    resBox = Listbox(window3,height = 6, width =35)
    resBox.grid(row=3,columnspan=2)
    
    checkOutBtn = Button(window3, text = "Return Book", command=lambda:returnBooks(bookEntry,label_2,resBox))
    checkOutBtn.grid(row=4,columnspan=2)

"""Insertslists into the gui, also shows the succss of the operation in the GUI"""
def returnBooks(bookEntry,label_2,resBox):
    bookSearch = bookEntry.get()
    message = bR.returnBook(bookSearch)

    label_2["text"]=message

    resList = dB.loanHistoryObject()

    for item in resList:
        resBox.insert(END,item)
        
"""fourth window"""
def create_window4(root):
    window4 = Toplevel(root)
    window4.title("Book Listing Popularity")

    label = Label(window4, text = "How many results?:")
    label.grid(row=0,column=0)

    numberEntry = Entry(window4)
    numberEntry.grid(row=0,column=1)

    titleList=Listbox(window4,height = 12,width=35)
    titleList.grid(row=1,column=0)

    titleDataList = Listbox(window4,height=12,width=35)
    titleDataList.grid(row=1,column=1)
    
    loanBtn = Button(window4, text = "List popularity (days)", command=lambda:popularityBooksListing(titleList,titleDataList, numberEntry))
    loanBtn.grid(row=2,column=0)

    generateBtn = Button(window4, text = "Generate text files", command = lambda:bL.generateTextFiles())
    generateBtn.grid(row=2,column=1)

    graphBtn = Button(window4, text = "Show Graph", command=lambda:bL.graph())
    graphBtn.grid(row=3,column=0)

    keyBtn = Button(window4, text = "Show key", command=lambda:keyWindow(titleDataList))
    keyBtn.grid(row=3,column=1)

"""Displays graph of popular book, reusing modules"""
def keyWindow(titleDataList):   
    keyList = bL.graphKey()

    for item in keyList:
        titleDataList.insert(END,item)
    

"""INserts two lists into GUI"""
def popularityBooksListing(titleList,titleDataList, numberEntry):
    var = int(numberEntry.get())

    list1,list2 = bL.popList(var)

    for item in list1:
        titleList.insert(END,item)

    for item in list2:
        titleDataList.insert(END,item)


###############################
####------MAIN----------#######
###############################

def main():
    root = Tk()

    my_menu = Menu(root)
    root.config(menu=my_menu)

    #create a menu item

    file_menu = Menu(my_menu)
    my_menu.add_cascade(label="File",menu=file_menu)
    file_menu.add_command(label="Initialise DB",command = lambda:dB.initialiseDB())
    file_menu.add_separator()
    file_menu.add_command(label="Exit",command = root.quit)

    #setting attributes of the window
    root.title("Library Data Base")
    root.geometry('450x410')

    img = ImageTk.PhotoImage(Image.open("libraryPic.jpg"))

    imgLabel = Label(image=img)
    imgLabel.pack(fill=X)

    #binding event handler to clicked function
    btn_1 = Button(root, text="Search books", command = lambda:[create_window1(root)])
    btn_2 = Button(root, text = "Check Out Books", command = lambda:[create_window2(root)])
    btn_3 = Button(root, text = "Return Books", command = lambda:[create_window3(root)])
    btn_4 = Button(root, text = "List Books", command = lambda:[create_window4(root)])

#packing buttons
    btn_1.pack(fill=X)
    btn_2.pack(fill=X)
    btn_3.pack(fill=X)
    btn_4.pack(fill=X)

    root.mainloop()

if __name__=='__main__':
    main()

#dB.restart()
