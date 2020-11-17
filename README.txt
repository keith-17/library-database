This is the read me document for the COP501 homework

My implementation:

This program uses an initial example list for book data and loan history data.

Button 1 allows you to search for a book based on its title

Button 2 allows the librarian to check out a book only if the member exists in loan history and the book is valid

Button 3 allows the librarian to return a single book

Button 4 allows the librarian to get a list of the most popular books, display it as a bar graph, then generate a new formatted text file of bookdata and loan history.

Initialising the database restarts the entire process and clears it of new contents

BUGS:

-The list books functionality only works on initial loan history data
-It is unable to read new return dates from the databases
-It works up to the point of a book being checked out
-Initialising the database works by deleting the database file, I was unable to implement a unique constrain identifier
-When generating a graph, a key of book ID and their names are meant to come up in the previous window. as demonstrated before

MODULES AND FILES:

The following modules are used:
bookcheckout, booklist, bookreturn, booksearch,database,GUI

The following files are used inititaly:
README, loan_historyExample, libraryBooks

The following files are GENERATED/INITIALISED:
library.db,loan_history.txt,Book_info.txt
