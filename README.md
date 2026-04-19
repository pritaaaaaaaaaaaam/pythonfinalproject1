
Project Title : Small Business Inventory and Sales System.
Student Name : Pritam 
Student Number : P499840


I confirm that this assignment is my own work.  Where I have referred to online sources, I have provided comments detailing the reference  and included a link to the source

PROJECT DESCRIPTION

This project is an Inventory Management System developed in Python using the Tkinter module for the graphical user interface and SQLite3  for data storage. The main motive of this program is to allow users, such as small shop owners or say warehouse managers to very easily add, update, delete and sell products while keeping track of stock levels and revenue in real time .
Users can add a new product by entering its name, price, initial quantity and a minimum stock level. Products can be updated by entering the product id  and the new details shown by the label above the input field . user can also delete a product using its ID. When selling a product, the user enters the product ID and quantity sold. 
The program checks if there is enough stock then it  reduces the quantity accordingly and records the sale and calculates the revenue for the transaction and displays how much total revenue has been made throughout . All sales are stored in a separate sales table.
I  included a Best Sellers Chart .  It uses the Matplotlib library and when the user clicks the button it queries the sales table and displays a bar chart showing the top 4 best selling products 
I divided the interface into clear sections. The central white card  displays the full stock list showing each product’s ID, name, price, current quantity and minimum stock level. On the right, a red card shows low stock alerts for any items that went  below their minimum stock . At the bottom centre, the total revenue from all sales is displayed and updates automatically after each sale.  I used different coloured cards to make navigation more user friendly and appealing .
Data is  saved in a local SQLite3 database file “the1database.db”, which is created automatically when the program runs 1st time . Input validation is included to prevent empty fields and negative stock quantities. 

Packages and Libraries Used
tkinter - graphical user interface
sqlite3 - local database storage
matplotlib - bar chart for best selling products

Installation Instructions
Make sure Python 3 is installed on your machine
Install the matplotlib  library needed by running this in your terminal:
 	pip install matplotlib 
Or 
python -m pip install matplotlib

   
How to Run the Program
Open the  terminal or command prompt
Navigate to the folder where the file is saved
Run the command:
       python main.py 
       Or if your system uses python 3 
      
       python3 main.py
The application window will open automatically. The database file theonedatabase.db will be created on its own the first time you run it


OUTPUT 







