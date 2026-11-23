# BFB321_group_21
Members:
- KL Mohale - 23792788
- MG Nsibande - 21565326
- NL Sethole - 24779807
- NV Vilakati - 22911996
## Project Title: Smart Spaza Food Network 
### 1. project description (B4)
Small food vendors often lack a simple and reliable system for tracking stock and monitoring expiry dates. This can lead to food waste and loss of sales. Therefore, this project focuses on creating an expiry date and stock monitoring system for small food vendors/Tuckshops. The project uses html,css,flask and python with MySQL database for storing and managing information.

### 2. Main Features (B4)
- Account registration, password hashing, login and logout.
- **User Guide:** helps users navigate and use the system.
- **Class A Inventory:** Displays products classified under Class A inventory.
- **Class B Inventory:** Displays products classified under Class B inventory.
- **Add Products:** Allows users to add new products and their relevant stock information.
- **Support:** Provides users with access to support information.
- **Expiry-Date Monitoring:** Helps users identify products approaching or past their expiry dates.
- **Supply Chain Model:** The inventory management model is implemented in `Inventory.py`.
-  Manual product flagging for spoiled, damaged, packaging problems, uncertain expiry dates or other concerns.
- EOQ, safety stock, reorder point and estimated orders-per-year calculations.
- Dashboard KPIs and a list of products requiring attention.
- JSON endpoints for product and dashboard data.
- Persistent local SQLite database, MySQL 8 schema for deployment, and automated tests.
  
### 3. Technologies Used (B4)
 HTML 
 CSS
 jinja templates and Bootstrap 5 stylesheet
 Python 
 Flask
 SQLite for zero-setup local development
 MySQL 

 **Database note:** the current Flask application connects to SQLite so that the project can be run immediately without installing or configuring a database server. `database/schema.sql` provides the corresponding MySQL tables and indexes for a MySQL deployment. The Flask data-access layer would need to be switched to a MySQL driver before the application itself connects to that server; the included SQL file alone does not make the running app MySQL-backed.

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

### 7. Database Backup (B4)
The MySQL database can be backed up using MySQL Workbench:

1. Open MySQL Workbench and connect to the database server.
2. Navigate to Server → Data Export.
3. Select the `smart_spaza_shop` database.
4. Choose Dump Structure and Data.
5. Select Export to Self-Contained File.
6. Choose a destination and save the backup as `backup.sql`.
7. Click Start Export.

### 8. Database Restoration (B4)
To restore a database backup:

1. Open MySQL Workbench.
2. Navigate to Server → Data Import.
3. Select Import from Self-Contained File.
4. Browse for the saved `backup.sql` file.
5. Select the target schema, `smart_spaza_shop`.
6. Start the import.

### 9. Rollback Procedure (B4)
If a database modification causes errors or unexpected results:

1. Stop the application to prevent further database changes.
2. Identify the most recent valid database backup.
3. Restore the backup using MySQL Workbench.
4. Check that the database tables and records have been restored.
5. Restart the Flask application and confirm that the system works correctly.

### 10. Configuration
Copy `.env.example` to `.env` and configure the equivalent environment variables in your terminal or hosting platform. The application reads environment variables directly; install a dotenv loader if you want `.env` files to be loaded automatically.

- `SECRET_KEY`: set a long, random secret before deployment.
- `SMART_SPAZA_DATABASE`: optional SQLite database path.
- `FLASK_DEBUG`: set to `1` only for local development.
- `PORT`: optional server port (default 5000).

Do not commit real passwords, secret keys or database credentials.

### 11. Supply-chain model and assumptions
The calculations are kept in `inventory.py`, independent of Flask and the database.

| Measure | Formula | Interpretation |
|---|---|---|
| Economic Order Quantity | \(EOQ=\sqrt{\frac{2DS}{H}}\) | Order size that balances ordering and annual holding costs under the basic EOQ assumptions. |
| Safety stock | \(SS=z\sigma_d\sqrt{L}\) | Buffer stock for demand uncertainty during lead time. |
| Reorder point | \(ROP=\bar dL+SS\) | Stock level at which replenishment should be considered. |
| Orders per year | \(D/EOQ\) | Approximate annual order frequency. |

Where `D` is annual demand (units/year), `S` is ordering cost per order, `H` is annual holding cost per unit per year, `z` is the service-level factor (default 1.65), `σd` is daily demand standard deviation, `L` is lead time in days, and `d̄` is average daily demand.

**Assumptions:** demand and lead time are treated as stable for these introductory calculations; the safety-stock formula assumes independent daily demand variation and a fixed lead time; costs must use consistent currency/time units. The default `z=1.65` is an approximate 95% one-sided service factor. EOQ is a planning estimate and does not account for supplier minimum order quantities, quantity discounts, perishability, shelf capacity or cash constraints. For perishable products, expiry and storage constraints should override an otherwise calculated order quantity.

### 12. Application routes

| Route | Method | Purpose |
|---|---|---|
| `/register` | GET, POST | Create an account |
| `/login` | GET, POST | Authenticate a user |
| `/logout` | POST | End the session |
| `/` | GET | Dashboard and KPI summary |
| `/inventory/A` or `/inventory/B` | GET | View a product class |
| `/add-product` | GET, POST | Add a product |
| `/product/<id>` | GET | Product details and calculations |
| `/product/<id>/edit` | GET, POST | Update a product |
| `/product/<id>/flag` | POST | Flag product condition |
| `/product/<id>/unflag` | POST | Clear product flag |
| `/product/<id>/remove` | POST | Soft-remove product from active stock |
| `/user-guide` | GET | User instructions |
| `/support` | GET | Support information |
| `/api/products` | GET, POST | List or create products (authenticated) |
| `/api/dashboard` | GET | Return KPI data (authenticated) |

All inventory and API routes require a logged-in account. Registration and login are public.
### 13. Data model

`users` stores account identity and a Werkzeug password hash; passwords are never stored in plain text. `products` stores stock, expiry, supply-chain inputs, category, flag information, removal state and timestamps. Product records are soft-removed so historical records are not immediately deleted.

The SQLite schema is created by `init_db()` in `app.py`. The MySQL 8 DDL equivalent is in `database/schema.sql`.

### 14. Testing

Run the tests from the project root:

```bash
python -m pytest -q
```

The tests cover EOQ, safety stock, reorder point, orders per year, expiry classification, product flagging, validation, registration/login, product CRUD/flagging/removal, dashboard rendering and JSON API responses. Tests use a temporary SQLite database and do not modify the normal development inventory.

### 15. Three end-to-end workflows

1. **Create product:** register/log in → Add Product → validate submitted fields → insert the product into SQLite → redirect to its details page.
2. **Expiry and condition monitoring:** open a class inventory or dashboard → calculate expiry status from today's date → flag damaged/spoiled goods → save the flag and reason → dashboard and details reflect the change.
3. **Replenishment:** open product details → calculate EOQ, safety stock and ROP → compare on-hand quantity with ROP → display a low-stock alert when quantity is at or below ROP.

### 16. Deployment and operational notes

- Use a production WSGI server (for example Gunicorn) rather than Flask's development server.
- Set a unique `SECRET_KEY`, disable debug mode and use HTTPS.
- Use MySQL 8 in a hosted deployment by applying `database/schema.sql` and replacing the SQLite connection adapter in `app.py` with a configured MySQL connection pool/driver.
- Back up the database regularly. For SQLite, stop writes and copy the `.db` file or use SQLite's backup API. For MySQL, use `mysqldump` and test restoration.
- Add CSRF protection (for example Flask-WTF), rate limiting and stricter account verification before public production use.
- Keep supplier-specific order decisions, stock adjustments and disposal records auditable as the system is extended.

### 17. Limitations and future improvements

The supplied project is a working academic prototype. It currently uses a single shared inventory rather than tenant-separated shop accounts, and it does not yet implement supplier orders, stock receiving, audit history, barcode scanning, email alerts or a live MySQL adapter. The local prototype stores all product rows in one SQLite database. Those capabilities should be implemented and tested before commercial deployment.




