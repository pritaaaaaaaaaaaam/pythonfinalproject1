
# Imports 
import sqlite3 
import tkinter as tk

from tkinter import messagebox
import matplotlib.pyplot as plt

# I learned about sqllite3 from SQLite Databases With Python by freeCodeCamp.org . 
#included all the learning materials in the README

# sqlite3.connect("theonedatabase.db") opens a file called " theonedatabase.db " as a database.
# and if that file isnt there yet the  python creates it automatically.
# conn is like a short form for connection and  you have to open it at the start and close it at the end. 
conn = sqlite3.connect("theonedatabase.db")

#as freecodecamp mentions the cursor is the object used to execute commands and fetch results from the database.

#i also found escapeRoomCodings explanation on the sqllite used good and took iam including a few points he mentioned  where he said 
# "A cursor is basically a middleware between your Python code
# and the database. It helps you execute SQL queries and fetch data"
# so basically conn opens the line to the database, but cursor  is the actual thing that writes and reads. 
# Without the cursor you  cannot run any sql commands .

cursor = conn.cursor()

# I learned this CREATE TABLE from escaperoomCoding where i got to know that we use IF NOT EXISTS so the code doesn't crash if the table is
# already there.  meaning if I run the program  second time, it
# wont try to create the table again and cause an error.


# id is integer, primary key , and autoincrement so it's created  automatically when a user adds a new record so user never has to
# type an Id themself the database itself generates it.
# Price is REAL because it is a floating number for obvious reason to perfom calculations 

# i included min_stock as i wanted each product to have its own
# minimum stock level instead of one fixed number for everything . because different product different stock coems in 
cursor.execute("""
    CREATE TABLE IF NOT EXISTS products (
        id        INTEGER PRIMARY KEY AUTOINCREMENT,
        name      TEXT,
        price     REAL,
        quantity  INTEGER,
        min_stock INTEGER
    )
""")

# This sales table I needed somewhere to record every
# sale so I could calculate total revenue and show a sales history.
# product_name tells which product was sold ,  qty_sold  tells  how many units were sold and revenue  is price  * quantity for that sale
cursor.execute("""
    CREATE TABLE IF NOT EXISTS sales (
        id           INTEGER PRIMARY KEY AUTOINCREMENT,
        product_name TEXT,
        qty_sold     INTEGER,
        revenue      REAL
    )
""")


# conn.commit() basically saves everything to the database file on disk.

# Without commit() ,  your changes will only be in the  memory and goesaway
# when the program closes.
conn.commit()


# FUNCTIONS

# The idea of like dividing everything into separate named functions
# came from learning Manav Codaty (dev.to) 's article . In his article he wrote  the skeleton like : 
#  def add product() ,  def delete product() , def get all products() .
#  I learned how to organise an inventory system and I followed that same structure throughout . 

def add_product():

    # .get() basically reads whatever the user has typed into the input box.
    # I learned this from  Coding Lifestyle 4u yt and  renzyCode yt  where both of them used
    # .get() on their input fields to get or lets say retrieve the value the user had typed . Each line stores the typed value into a variable 
    name    = entry_name.get()
    price   = entry_price.get()
    quantity     = entry_qty.get()
    minimum_stock = entry_min_stock.get()

    # This is input validation and I learned this from EscapeRoomCoding yt
    # so in that video the he mentioned that  "Validation avoids errors like negative quantities and
    # empty fields." and i also saw similar practice in my other resource Coding Lifestyle 4u aswell 
   
    #  if name == "" or price == "" or quantity == "" or minimum_stock == "":

    # so this basically  checks if any field is empty , == "" means equals  nothing (empty).
    #  It is okay if one feild is empty because an or operator is been used so the whole condition will eventually be true
    #  We then show an error popup  and "return" which immediately stops the function  and nothing gets saved.

    if name == "" or price == "" or quantity == "" or minimum_stock == "":
        messagebox.showerror("Error", "All fields are required!")
        return

    # INSERT query 
    # i  learned this from Yavuz Ertugrul (gitconnected.com)
    # His exact code was :  INSERT INTO supermarket values(?, ?, ?)
    # and i learned what the symbols ? ? ?  meant . 
    # EscapeRoomCoding explained the ? symbols

    # INSERT INTO basically adds  new row into the products table.
    # The question marks '?'  are like placeholdes as we never put python variables directly inside a SQL string

  # now without if a user typed  
    #                              it could destroy the entire database. placeholders prevent that completely.

    # float(price) converts the text "1.99" into a decimal number 1.99
    # because the database needs  a number  not a string.
    # int is also used for the same reason 
    cursor.execute("INSERT INTO products (name, price, quantity, min_stock) VALUES (?, ?, ?, ?)",
                   (name, float(price), int(quantity), int(minimum_stock)))

    # Save the new record permanently to the database file.
    # used conn.commit() immediately after every INSERT, UPDATE or DELETE.
    conn.commit()   # Without this  the product will apear to have been added but disappears when the terminal closes

    # The following is done to clear the entry boxes after a successful add  so they are empty  for the next product to be entered.
    # delete(0, tk.END) means ,  delete from position 0 which is the start to all the way to tk.END which is the end of what the user has typed 

    entry_name.delete(0, tk.END)
    entry_price.delete(0, tk.END)
    entry_qty.delete(0, tk.END)
    entry_min_stock.delete(0, tk.END)

    # This refresh () reloads the display so the new product comes up on screen ( Stock the white box on my output ) immediately.
    # I learned this from RenzyCode where  he had a show_data() function that he called at the end of every action 
    # (add, delete) so the screen the output always showed what was actually in the database.
    
    refresh()


def update_product():

    # Learned from Yavuz Ertugrul and EscapeRoomCoding.

    # Yavuz used  UPDATE supermarket SET price = ?, quantity = ? WHERE name =  ?
    # EscapeRoomCoding used UPDATE inventory SET name= ? , quantity = ?,
    # price = ? WHERE id = ?

    # I followed EscapeRoomCoding's version because targeting by ID is  more safer as two products could have the same name but never
    # the same ID and it will give my output a more POS style feel and if i want i can add more features with the help of id 
    #more than name ans it makes it easier my user as they dont have to type the name and risk spell error or casings 



    # Read all the values the user typed into the update section
    productid     = entry_upd_id.get()     # ID of the product to find and update
    name    = entry_upd_name.get()   # new name to replace the old one
    price   = entry_upd_price.get()  # new price
    quantity    = entry_upd_qty.get()    # new quantity
    minimum_stock = entry_upd_min.get()    # new minimum stock level

    # Once agian the same thing as done in add_product is done here and this 
    # make sure no field is left blank as 
    # all fields for sure  must be present before we attempt to write to database or else it will
    #crash 

    if productid == "" or name == "" or price == "" or quantity == "" or minimum_stock == "":
        messagebox.showerror("Error", "All fields are required!")
        return
    # return exits the function right here and  Nothing below this line runs.


    # UPDATE query 

    # "SET name= ? and  price= ? and quantity = ? " means which columns to update and to what value to update with
    # "WHERE id = ? " ensures it only changes the row where the id matches 
   
    # int(productid) converts the id from text to a number because the database
#has it stored as an integer and not text

    cursor.execute("UPDATE products SET name = ?, price = ?, quantity = ?, min_stock = ? WHERE id = ?",
                   (name, float(price), int(quantity), int(minimum_stock), int(productid)))
    
    conn.commit() 

    # Clear all five update fields after the update is done
    entry_upd_id.delete(0, tk.END)
    entry_upd_name.delete(0, tk.END)
    entry_upd_price.delete(0, tk.END)
    entry_upd_qty.delete(0, tk.END)
    entry_upd_min.delete(0, tk.END)

    refresh()

    # showinfo shows a popup (not an error) to confirm  the update worked. "f"Product ID { productid } updated successfully!" 
    # is an f-string and it lets you put a variable directly inside a string using curly brackets {}.
    # So f"Product ID {productid } updated" will show the actual ID number.
    messagebox.showinfo("Updated", f"Product ID { productid } updated successfully!")


def delete_product():


    productid = entry_del_id.get()  # This gets the product id  the user has typed in the delete section


    if productid == "":     # If the field is empty show an error and stop
        messagebox.showerror("Error", "Enter a product ID!")
        return

    # delete  query 
    # learned from Yavuz Ertugrul's cite  and EscapeRoomCoding yt 
    # Yavuz used DELETE FROM supermarket WHERE name=? and  EscapeRoomCoding used DELETE FROM inventory WHERE id=?

    # DELETE FROM products  removes a row from the products table
    # WHERE id =  ?  only deletes the specific row where the id matches
    # (productid,) - the comma after productid makes it a tuple. and i leanred this from EscapeRoomCoding  where it said  "In Python, when you give one
    # parameter like this, you need a comma so Python knows it's a tuple
    # and not just brackets around a variable."

    cursor.execute("DELETE FROM products WHERE id = ?", (productid,))
    conn.commit()

    entry_del_id.delete(0, tk.END)
    refresh()


def sell_product():
 # a sell feature. 
    # i built this fuction based on what the sources had taught me ( this is my own addition and thie sources have not covered it but it is done 
    #from the learnings i gained from the sources )

   
    productid = entry_sell_id.get()   # ID of product being sold
    quantity = entry_sell_qty.get()  # how many are being sold

    if productid == "" or quantity == "": # without this empty strings go into integer conversion further and this will lead to crash
        messagebox.showerror("Error", "Enter product ID and quantity!")
        return


  # SELECT * means "fetch all columns". WHERE id=? finds only the row with that specific ID.

    # SELECT with fetchone() and learned directly from EscapeRoomCoding.
    # His exact code is - cursor.execute("SELECT * FROM inventory WHERE id=?", (item_id,))
    #                      item = cursor.fetchone()
    # He explained saying  "We fetch one because we are getting detail based on the ID of the primary key."
    # "SELECT *" means give me all columns for this row.
    # fetchone() returns one single row as a tuple, for ex:
    # (1, "pen", 0.5, 50, 10) where each number is a column value.
    cursor.execute("SELECT * FROM products WHERE id = ?", (productid,))
    row = cursor.fetchone()



    # If fetchone had not got anyhting , the product id  will not be in  the DB.
    # "is None" means nothing was returned baiscally the variable is empty.
    # i also included smhtn extra thats shows an error and stop if the product was not found to make mine robust
    if row is None:
        messagebox.showerror("Error", "Product not found!")
        return

    # row[3] is the quantity column - index 3 because Python counts from 0:

    # row[0]=id ,  row[1]=name , row[2]=price , row[3]=quantity, row[4]=min_stock
    
  
    # this is to check we have enough stock before allowing the sale.
#because for ex if someone tries to sell 50 quantity  while only 10 are in stock 
    #                            quantity would go negative. A product showing -40 in stock is not what we want 
    #                            and breaks the low stock alert logic too.
    if int(quantity) > row[3]:
        messagebox.showerror("Error", f"Not enough stock! Only {row[3]} left.")
        return

    # new_qty = minus how many we are selling from current stock
    # revenue = price * by the quantity sold
    # row[2] is the price column and row[3] is the current quantity
    new_qty = row[3] - int(quantity)
    revenue = row[2] * int(quantity)

    # as usual update the stock after the sale 
    
    cursor.execute("UPDATE products SET quantity = ? WHERE id = ?", (new_qty, productid))

    # INSERT a sale record 
    # row[1] is the product name (second item in the row tuple).
    # This records what was sold, how many, and how much money was made.
    cursor.execute("INSERT INTO sales (product_name, qty_sold, revenue) VALUES (?, ?, ?)",
                   (row[1], int(quantity), revenue))

    # One commit saves both the stock update AND the sale record together
    conn.commit()

    entry_sell_id.delete(0, tk.END)
    entry_sell_qty.delete(0, tk.END)
    refresh()

def refresh():

    # The idea for this function came from me wathcing RenzyCode's youtube video where 
    # He had a show_data() function that he called at the end of  every single action of add, delete, update. 
    # His reason was so the display always matches what is actually in the database.

    # I followed the exact same approach with refresh().

    # refresh() basically redraws all the  display panel using with latest data from the database.
    # It is called after every operation so the screen alway shows whas actually saved.
    # Without this  refresh() being called after operations , the UI gets totally out of sync with the database.
    #                                                 for ex : when you add a product ( wihtout this refresh () being caleld ) it's in the DB but not on screen.
    #                                                  when you  Sell stock the quantity on screen doesn't change.
                                               

    # from the products table. * means all or everything .
    # fetchall() returns all rows at once as a list of tuples.


    cursor.execute("SELECT * FROM products")     # SELECT * FROM products basically gives me every row and every column  from the profucts table 
    rows = cursor.fetchall()

    # config(state=tk.NORMAL)  temporarily unlocks the text box so we
    # can write into it. By default it is disabbled meaning read only so users cannot type or edit on anything inside it 

    stock_text.config(state=tk.NORMAL)

    # delete("1.0", tk.END) clears all existing text before rewriting.
    # "1.0" means line 1, character 0 which is the very beginning of the box.
    # We clear it first so we don't end up with duplicate entries
    # every time refresh() is called.
    
    stock_text.delete("1.0", tk.END)

    # Learned this  from Yavuz Ertugrul,  he used the exact same if/else pattern:
    # if rows: for row in rows: print product details
    # else: print "No products in the supermarket"
    # If rows is empty meaning no products then  show a message. Otherwise loop
    # through each row and display its details.
    if not rows:
        stock_text.insert(tk.END, "No products available.")
    else:
        for row in rows:
            # row [0]= id, row [1] = name , row [2] = price, row [3] = qty, row [4] = min_stock
            # :.2f formats the price to always show 2 decimal places ex 1.50
         
            stock_text.insert(tk.END,
                f"ID: {row[0]} | {row[1]} | £{row[2]:.2f} | Qty: {row[3]} (Min: {row[4]})\n")   # \n moves to a new line after each product

    # Lock the text box again so the user cannot type into it
    stock_text.config(state=tk.DISABLED)

    # Low stock alerts 

    low_text.config(state=tk.NORMAL)
    low_text.delete("1.0", tk.END)

    # This is a list comprehension which is  a short way of filtering a list.
    # It goes through every row and keeps only the ones where the current  quantity
    #  (row [ 3 ] ) is less than or equal to that product's own minimum stock level (row[4]).
    
    # i used one logic here and that is instead of one fixed number for all products,
    # each product compares against its own min_stock value because i beloeve thats how stocks come into shops 
    low_items = [row for row in rows if row[3] <= row[4]]

    if not low_items:
        low_text.insert(tk.END, "All stock levels are fine.")
    else:
        for row in low_items:
            low_text.insert(tk.END,
                f"ALERT: {row[1]} (ID: {row[0]}) is low! {row[3]} left.\n")

    low_text.config(state=tk.DISABLED)

    # Total Revenue 
    # i included this so the user can see how much   transaction hes made totally and
    #  how i did this is simple 
    # SELECT SUM() is a built in SQL function that adds up all the values in a column. 
    # Here it totals all revenue from  every sale made in the sales table.
    # fetchone()[0] gets the single value returned and [0] means the first (and only) item in the result tuple.

   
    cursor.execute("SELECT SUM(revenue) FROM sales")
    total = cursor.fetchone()[0]
    total = total if total else 0.0 # "total if total else 0.0" means if the result is None due to no
    # sales havent  been made yet  use 0.0 instead so we don't get an error.
    lbl_revenue.config(text=f"Total Revenue: £{total:.2f}")



def show_chart():

    # This function builds a bar chart for the top 4 best sellers 
    # SUM(qty_sold) adds up all the units sold ,  GROUP BY product_name groups all the rows with the same
    # product name  so sum  can total them together  , ORDER BY SUM(qty_sold) DESC sorts the results from the highest to lowest so the best #
    # sellers appears first .
    #LIMIT 4 tells how many products we want it to be on the graph , like top how many , in our case its 4 
    cursor.execute("""
        SELECT product_name, SUM(qty_sold)
        FROM sales
        GROUP BY product_name
        ORDER BY SUM(qty_sold) DESC
        LIMIT 4
    """)
    results = cursor.fetchall()

   
    if not results:  # If no sales have been made then obviously theres nothing to draw 
        messagebox.showinfo("Bar graph (Best Selling)", "No sales data yet!") 
        return

    # This basically split the results into two lists , names for the x axis and qtys for the bar heights
    # matplotlib needs them separate to draw the chart 
    names = [r[0] for r in results]
    qtys  = [r[1] for r in results]

    plt.bar(names, qtys, color= 'orange')
    plt.title("Best Selling Products")
    plt.ylabel("Units Sold")
    plt.tight_layout()
    plt.show()


# The GUI

#for this part i used the same resources used above escaperoomcoding yt and renzy code yt  but i also used Tkinter Course -
#Create Graphic User Interfaces in Python Tutorial by freecode camp  and Tkinter tutotial by programming knowldge to help support my understandings 

root = tk.Tk() # tk.Tk() creates and opens the main application window.


root.title("Inventory management system ") # Sets the text shown in the title bar of the window which is my project title 

root.geometry("1440x900") #1440 pixels wide, 900 pixels tall

root.configure(bg="#d0d0d0") # Sets the background colour of the window 

# E and L are dictionaries and they store the style settings for my
# Entry widgets and Label widgets so I don't have to repeat them
# on every single line. "**E" when used in a widget means we don't repeat the same keyword arguments on every single line.

E= {"bg": "#eeeeee" , "fg": "black" , "insertbackground": "black" , "relief": tk.FLAT}
L = {"bg": "white",   "fg": "black", "font": ("Arial", 9)}

# A helper function to create card style white boxes that are Frames.
# tk.Frame creates a rectangular container inside the window.
# .place (x , y , width, height ) positions it at exact pixel coordinates.
# "bg" is the background colour which is white 

def card(x, y , w, h, bg="white" ) :
    f = tk.Frame(root, bg=bg)
    f.place( x=x , y=y , width=w , height=h )
    return f


# Adding product card - this appears on the top left of my output

# tk.Label shows text on screen  ,  just a title or say description to tell the user what goes into the box below it .
# tk.Entry is a text input box where the user types.

# tk.Button runs a function when clicked ,  command = add _ product means clicking this button will call the add_product() function above.
add = card(30, 20, 380, 340 )

tk.Label(add , text="Add Product" , bg="white" , fg="black",
         font=("Arial", 12 , "bold")).place(x= 130 , y = 8 )
tk.Label(add, text="Name",   **L ).place(x=15, y=45)
entry_name = tk.Entry(add,**E); entry_name.place(x=15, y=63 , width=345 , height=25)
tk.Label(add, text="Price (£)", **L).place(x=15, y=95)
entry_price  = tk.Entry(add,**E); entry_price.place(x=15, y=113, width=345 , height = 25)
tk.Label(add, text="Quantity",   **L).place(x=15, y=145)
entry_qty  = tk.Entry(add, **E); entry_qty.place(x=15, y=163, width=345, height=25)
tk.Label(add, text="Min Stock",**L).place(x=15, y=195)
entry_min_stock = tk.Entry(add, **E); entry_min_stock.place(x=15, y=213, width=345, height=25)
tk.Button(add , text="Add to Inventory" ,  command=add_product ,
          bg="#333" , fg="red" ,  relief=tk.FLAT ,
          font=("Arial", 10)).place(x=100 , y=280 , width=180 , height=35 )



# Update product card this sppears in the bottom left on my terminal 

# so 5  fields are neeeded here the id to find the product , then the four
# new values to replace the old ones with.

upd = card(30, 370, 380, 360)

tk.Label(upd , text="Update Product", bg="white", fg="black" ,
         font=("Arial", 12, "bold")).place(x=110, y=8 )
tk.Label(upd, text="Product ID" , **L).place( x=15 , y=45 )
entry_upd_id    = tk.Entry(upd, **E); entry_upd_id.place(x=15, y=63, width=345, height=25)
tk.Label(upd, text="New Name",  **L).place( x= 15 ,  y = 95 )

entry_upd_name  = tk.Entry(upd,  **E); entry_upd_name.place(x = 15, y= 113, width=345, height=25)
tk.Label(upd, text="New Price (£)", **L).place(x=15, y=145)
entry_upd_price = tk.Entry(upd, **E); entry_upd_price.place(x=15, y=163, width=345, height=25)
tk.Label(upd, text="New Quantity",  **L).place(x=15, y=195)
entry_upd_qty   = tk.Entry(upd, **E); entry_upd_qty.place(x=15, y=213, width=345, height=25)
tk.Label(upd, text="New Min Stock", **L).place(x=15, y=245)
entry_upd_min  = tk.Entry(upd , **E ); entry_upd_min.place(x=15 , y=263 , width=345 , height=25)
tk.Button(upd, text="Update Product" , command=update_product ,
          bg="#333", fg="red" , relief=tk.FLAT ,
          font=("Arial", 10)).place(x=100, y=308 , width=180 , height=35)




# this is for the stock display area that appears on the top middile of the output

# tk.Text is a multiline text display area.
# state=tk.DISABLED makes it read only thereofre users cannot type to it or on it 

stk = card(435, 20, 490, 400)
tk.Label(stk, text="Stock" ,  bg="white" ,  fg="black" ,
         font=("Arial", 12  , "bold")).place(x=205, y=8)
stock_text = tk.Text(stk, bg="white" , fg="black" , font=("Courier", 9),
                     relief=tk.FLAT , state=tk.DISABLED)
stock_text.place(x=10, y=35, width=470 , height=355  )


# This is for the Delete by id card ( which is blue in color and below the stock card on the misdle of the screen)


dlte= card(435, 435, 490, 175, bg="#1a3adb")
tk.Label(dlte ,  text="Delete by ID" ,  bg="#1a3adb" , fg="white",
         font=("Arial", 12, "bold")).place(x=160, y=10)
tk.Label(dlte, text="Product ID", bg="#1a3adb", fg="white" ,
         font=("Arial", 9)).place(x=15, y=50 )
entry_del_id = tk.Entry(dlte, **E)
entry_del_id.place(x=15 , y=68 , width=455 , height=25)
tk.Button(dlte , text="Remove Item" , command=delete_product ,
          bg="white", fg="#1a3adb" , relief=tk.FLAT ,
          font=("Arial", 10, "bold")).place( x=170 ,  y=115 ,  width=150 ,  height=35 )



# This is for the toatal revenue card that apears on the bottom middile , below delete by id card 
# lbl_revenue is stored as a variable because we need to update its text every time refresh() runs using lbl_revenue .config 

rev = card(435, 625, 490, 60, bg="#aaee44")
lbl_revenue = tk.Label(rev, text="Total Revenue: £0.00" ,
                        bg="#aaee44" ,  fg="black" , font=("Arial" , 12 , "bold"))
lbl_revenue.place(x = 130, y = 15 )



# This is for the low stock card which is in red and on the top right 
# This is the section that shows the alerts when the products go below their minimum quantity 

low = card(950, 20 , 460 , 430 , bg="#e83030" )
tk.Label(low , text="Low Stock" , bg="#e83030" , fg="white",
         font=("Arial", 12, "bold")).place(x=175, y=10 )
low_text = tk.Text(low, bg="#e83030", fg="white", font=("Courier" , 9 ),
                   relief=tk.FLAT, state=tk.DISABLED)
low_text.place(x=10 , y=45 , width=440 , height= 375 )



# This is for the sell product card which is on the bottom right 

# has 2 input fields ,  the product ID and how many to sell.
# Clicking Complete Sale runs sell_product () which checks stock, records the sale and updates the quantity all in one go.

sel = card(950 , 465 , 460 , 225)
tk.Label(sel , text= "Sell Product" , bg="white" , fg="black" ,
         font=("Arial" , 12 , "bold")).place(x=165 , y=8 )

tk.Label(sel, text="Product ID" ,  **L).place( x=15 , y=50 )
entry_sell_id = tk.Entry(sel, **E)
entry_sell_id.place(x=15, y=68, width=425, height=25 )

tk.Label(sel, text="Quantity",   **L).place(x=15,  y=105 )
entry_sell_qty = tk.Entry(sel, **E)
entry_sell_qty.place(x=15, y=123, width=425, height=25 )
tk.Button(sel , text="Complete Sale" ,  command=sell_product,
          bg="#333" , fg="red", relief=tk.FLAT ,
          font=("Arial", 10)).place( x=150 , y=170 ,  width=160 , height=35 )

# This is for the Best Seller Chart Button which is in the  bottom most middle , below the total revenue card
tk.Button(root, text="Best sellers Chart", command=show_chart,
          bg="#333", fg="red", relief=tk.FLAT,
          font=("Arial", 10)).place(x=435, y=695, width=490, height=35)

refresh()

# root.mainloop() keeps the window open and running.
# It sits in a loop waiting for the user to click buttons or close
# the window. Without this line the window would flash and disappear.
root.mainloop()

# Close the database connection cleanly when the program ends.
conn.close()