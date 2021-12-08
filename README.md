# INFSCI 2710 project: E-Commerce System
Group Member: Zimo Zhang, Peilin He, Xiaozheng Wang

## functions
Here is a google doc link for project functions descriptions(with screen shots):  
https://docs.google.com/document/d/1ty2Y96h4nB4CQXE8EaRePOmGiKblpwyCEMFR1YiQk9U/edit?usp=sharing

## How to run locally
1. install python
2. install Django
3. pip install django-filter
4. `cd wms`
5. `python3 manage.py makemigrations`
6. `python3 manage.py migrate`
7. `python3 manage.py runserver`

## Accounts for testing purpose
1. admin account for entering into order management system (http://127.0.0.1:8000/)  
username: zimo  
password: zimo
2. customer account for entring into e-commerce shopping site(http://127.0.0.1:8000/store_list)  
Note: This can not be used into access order management system. We've created a page to deal with this situation.  

username: testregister
password: testaccount


## Update since demo on 12.7
After the demo on 12.7, an important upgrade has been made on our E-Commerce System. The details are listed below:
1. The system now support user access management. By providing two user groups “admin” and “customer”. New registered user will be automatically assigned in customer group with no access to order management platform. Customer user can only edit their account information, select sales, browse products, buy product and view their order history. Admin user can not be registered via register page. A new admin user can only be created with the “python3 manage.py createsuperuser” command in the terminal. When an admin user 
logging, he/she will be redirected to the order management system.
2.  The E-Commerce System are now online and connected to the database of the Order Management System. Here is a brief guidance of how to use the E-Commerce System. 
    1. Register a new account, now the account only have access to E-Commerce System and if the user try to access Order Management System, the request will be denied.
    2. Before go to shopping, the user has to select his/her sales from different store.
    3. After selecting the sales, the user will be able to view the products in the specific store and add them to cart. Mention: The user can only view one stores product in one time. If the user want to view a different store’s product, he/she has to go back to step 2.
    4. After selecting the products, the user should click the shop cart icon at the upper-right of navigation bar. Then the user could edit the product number in the cart. If the number of products that the user want to purchase exceeds the product’s inventory. A pop-up window will appear to remind the user the remaining number of the inventory. Then click checkout. A pop-up window will appear once the purchase is finish.
    5. By clicking on the order history, the user could view and search his/her history orders.
3. Fix the pop-up error message when a admin user want to delete data which is a foreign key in other data.

