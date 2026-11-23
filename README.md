# BFB321_group_21
Members:
KL Mohale - 23792788
MG Nsibande - 21565326
NL Sethole - 24779807
NV Vilakati - 22911996
## Project Title: Smart Spaza Food Network 
### 1. project description (B4)
Small food vendors often lack a simple and reliable system for tracking stock and monitoring expiry dates. This can lead to food waste and loss of sales. Therefore, this project focuses on creating an expiry date and stock monitoring system for small food vendors/Tuckshops. The project uses html,css,flask and python with MySQL database for storing and managing information.

### 2. Main Features (B4)
- **User Guide:** helps users navigate and use the system.
- **Class A Inventory:** Displays products classified under Class A inventory.
- **Class B Inventory:** Displays products classified under Class B inventory.
- **Add Products:** Allows users to add new products and their relevant stock information.
- **Support:** Provides users with access to support information.
- **Expiry-Date Monitoring:** Helps users identify products approaching or past their expiry dates.
- **Supply Chain Model:** The inventory management model is implemented in `Inventory.py`.
  
### 3. Technologies Used (B4)
 HTML 
 CSS
 Python 
 Flask 
 MySQL 
### 4. Project Structure (B4)
- **app.py**– Main Flask application.
- **Inventory.py**– Supply chain and inventory management model.
- **config.py** – Database connection configuration.
- **schema.sql** – Database table definitions.
- **seed.sql** – Sample database data.
- **templates/** – HTML templates used by the website. These templates are titled Support, user guide, add_product,base,edit_product, index,inventory, login,product_details, register 
- **static/**– contains the css file.

### 5. How to run the website (B4) 
1. Clone the project repository.
2. Open the project folder in Visual Studio Code.
3. Create and activate a Python virtual environment.
4. Install flask, mysql-connector-python, and python-dotnenv.
5. Create the MySQL database.
6. Run the database schema and sample data scripts.
7. Configure the database connection using the `.env` file.
8. Run `app.py` to launch the Flask application.
9. Open the local website address in your browser.

### 6. API Endpoints
1. POST /api/login - User authentication
2. GET /api/inventory - Get all inventory items
3. POST /api/inventory - Add new product
4. PUT /api/inventory/<id> - Update product
5. GET /api/stats - Get dashboard statistics
