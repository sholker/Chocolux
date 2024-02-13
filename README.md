# ChocoLux Project

> Create by Ori Shai, Ilana Jamil and Daniel Machluf

--------



![about-img.png](static%2Fimages%2Fabout-img.png)

ChocoLux is a web application for a chocolate company, allowing users to view and purchase various chocolate items.

## Table of Contents

- [Features](#features)
- [Client's Features](#clients-features)
- [Admin's Features](#admins-features)
- [DB Structure](#db-structure)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [Usage](#usage)
- [Reference](#reference)
- [Login Details](#Login-Details)

## Features
### Client's Features

- View a list of chocolate items with details.
- Add/Remove items to the shopping cart.
- Check out and place orders.

### Admin's Features
- Add new Items to the database.
- Show reports on the order history.

### DB Structure:
![DB_tables](./DB_Structure/EER.png)

* [EER Diagram](DB_Structure/EER.mwb)

* [DB Structure](DB_Structure/structure.mwb)
#### SQL Quiries:
* ####  Tables (like to sql query file):
> 
>* [users](./DB_Structure/chocolatestore_SQL/users.sql) - Stores user information.
>
>* [items](./DB_Structure/chocolatestore_SQL/items.sql) - Stores chocolate items information.
> 
>* [orders](./DB_Structure/chocolatestore_SQL/orders.sql) - Stores orders information.
> 
>* [address_details](./DB_Structure/chocolatestore_SQL/address_deaild.sql)  - Stores address information.
> 
>* [payment_details](./DB_Structure/chocolatestore_SQL/payment_details.sql) - Stores payment information.
> 
>* [shopping_cart](./DB_Structure/chocolatestore_SQL/shopping_cart.sql) - Stores shopping cart information.
> 
>* [shopping_cart_details](./DB_Structure/chocolatestore_SQL/shopping_cart_details.sql) - A view that comabins the shopping cart and the items table.
> 
>* [user_order_total](./DB_Structure/chocolatestore_SQL/user_order_total.sql) - A view that joins all the tables above, 
and shows the total amount of orders per user.

## Getting Started

### Prerequisites

Make sure you have the following installed:

- Python (version 3.11.6)
- Flask (version 3.0.0)
- mySQL (version 8.0.26)



### Installation

1. Clone the repository: https://github.com/sholker/Chocolux.git
2. cd chocolux
3. pip install -r requirements.txt
4. Windows:
    ```bash
   
      set FLASK_APP=app.py
      set FLASK_ENV=development
      flask run
      ```
    Linux:   
    ```bash
       git clone https://github.com/sholker/Chocolux.git
       cd chocolux
        export FLASK_APP=app.py
        export FLASK_ENV=development
    ```
### Usage
- To run the application, run the following command in the terminal:
- ```bash
  flask run
  # then in browser, open
  http://127.0.0.1:5000/
  
  ```
### Reference
##### Frontend
- use this link to see the live demo: https://themewagon.github.io/chocolux/
- use this link for error pages: https://codepen.io/uiswarup/pen/XWdXGGV

### Login Details:

Type | Username  | Password 
--- |-----------| --- |
Client | daredevil | 123       
Client | spiderman | 123   
Client | deadpool |123
Admin | moonknight | admin
Admin | admin     | admin 
