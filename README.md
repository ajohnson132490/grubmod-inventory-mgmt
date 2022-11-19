# Grubmod Inventory Management System
#### Video Demo: https://youtu.be/W1KKj7U-Mww
#### A graphical inventory management designed for tracking the buying and selling of items


# Files

## static/favicon.ico
A basic money bag icon for the tab.

## static/styles.css
This file defines some basic styles for the entirety of the site. From the length of the file
alone, you may be able to tell that I'm not much for graphic design.

## templates/apology.html
This page was built using [C$50 Finance](https://cs50.harvard.edu/x/2022/psets/9/finance/).

## templates/index.html
This is the home page where the user can see their 20 most recent transactions, their current
cash balance, and their current inventory cost.

## templates/inventory.html
This is the dedicated inventory page. It displays the users entire inventory, allowing them to
sort by ID, type, price, or condition of the item.

## templates/layout.html
This page defines the general layout of the site including the nav bar and footer. Built using
[C$50 Finance](https://cs50.harvard.edu/x/2022/psets/9/finance/).

## templates/login.html
A basic login form. Built using
[C$50 Finance](https://cs50.harvard.edu/x/2022/psets/9/finance/).

## templates/purchase.html
This page allows the user to enter in items that they have purchased. It asks for the system type, price, market where the item was bought, and the current condition. The id is assigned automatically.

## templates/register.html
The register page allows new users to create a new account. Asking for a unique username and password, asking them then to confirm their password, then log in.

## templates/sale.html
This page allows the user to enter in items sold. It asks for the item number, how much it was sold for, and on what market it was sold.

## app.py
### after_request(response)
Makes sure input responses aren't cached.
### register()
Confirms data entered is valid, then creates an account in the users table. Afterwards, it reroutes the user to the log in screen.
### login()
Logs out any current user, then allows the user to log in. Confirms data entered is valid, then logs the user in, bringing them to the home page.
### logout()
A basic logout function that forgets the session user id, then reroutes the user to the login form.
### index()
The home page of the site. Gets the 20 most recent transactions, the current cash and portfolio balance, and passes it to index.html.
### inventory()
Gets the current users inventory from the merchandise table, and displays it. By default it sorts by the unit id, but can sort by other variables.
### sale()
Makes sure all data entered into sale.html is valid. Then removes the item from inventory, adds the transaction to the transaction table, and updates the users cash balance. Afterwards it redirects to the home page.
### purchase()
Makes sure all data entered into purchase.html is valid. Then adds the item to the inventory, adds the transaction to the transaction table, and updates the users cash balance. Afterwards it redirects to the home page.

## helpers.py
Built using [C$50 Finance](https://cs50.harvard.edu/x/2022/psets/9/finance/).
### apology(message, code=400)
Displays an error message, as well as an error code over a picture of a grumpy cat. Default error code is 400.
### login_reqired(f)
A decorate route to reqire login.
### usd(value)
Formats a value as USD.

## inventory.db
The local database file, accessable through phpLiteAdmin.

## requirements.txt
A list of all required technologies for use of this program.

# History and Usage
Grubmod was a video game console restoration idea a friend of mine had that we worked on together. We would buy old consoles, repair and refurbish them, then flip the console for profit. We did this for a few months before we eventually abandoned the idea due to the rising price of retro consoles. One issue we ran into was not knowing who had sold what, and when. So this project was designed to keep track of all of that.

Please feel free to use this project however you like for any non-commercial purposes, if you do refrence it, please give credit.