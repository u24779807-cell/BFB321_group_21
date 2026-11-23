import os
from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    session,
)

from inventory import InventoryItem, inventory
from config import get_db_connection
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash



# ==========================================
# FLASK APPLICATION
# ==========================================

app = Flask(
    __name__,
    static_folder="Static",
    static_url_path="/static"
)

# Load environment-specific configuration
environment = os.getenv("FLASK_ENV", "development")

configurations = {
    "development": "config.DevelopmentConfig",
    "testing": "config.TestingConfig",
    "production": "config.ProductionConfig"
}

if environment not in configurations:
    raise ValuError("Invalid FLASK_ENV setting.")

app.config.from_object(configurations[environment])

if environment == "production":
    app.config["ENV"]="production"
    config.Production.validate()




# ==========================================
# HELPER FUNCTIONS
# ==========================================

def get_active_inventory():

    return [
        item
        for item in inventory
        if not item.removed
    ]


def get_inventory_statistics():

    active_items = get_active_inventory()

    total_products = len(active_items)

    expiring_soon = sum(
        1
        for item in active_items
        if item.get_status() == "Expiring Soon"
    )

    expired = sum(
        1
        for item in active_items
        if item.get_status() == "Expired"
    )

    flagged = sum(
        1
        for item in active_items
        if item.get_status() == "Flagged"
    )

    low_stock = sum(
        1
        for item in active_items
        if item.reorder_alert()
    )

    return {
        "total_products": total_products,
        "expiring_soon": expiring_soon,
        "expired": expired,
        "flagged": flagged,
        "low_stock": low_stock
    }


def find_product(product_id):

    for item in inventory:

        if item.id == product_id:
            return item

    return None


# ==========================================
# HOME / DASHBOARD
# ==========================================

@app.route("/")
def home():

    statistics = get_inventory_statistics()

    attention_products = [

        item
        for item in get_active_inventory()

        if (
            item.get_status()
            in ["Expired", "Expiring Soon", "Flagged"]
            or item.reorder_alert()
        )

    ]

    return render_template(
        "index.html",
        statistics=statistics,
        attention_products=attention_products
    )


# ==========================================
# LOGIN
# ==========================================


@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        if not username or not password:
            flash("Please enter your username and password.", "error")
            return render_template("login.html")

        connection = None
        cursor = None

        try:
            connection = get_db_connection()
            cursor = connection.cursor(dictionary=True)

            cursor.execute(
                """
                SELECT user_id, username, password_hash
                FROM users
                WHERE username = %s
                """,
                (username,)
            )

            user = cursor.fetchone()

            if user and check_password_hash(user["password_hash"], password):

                session["user_id"] = user["user_id"]
                session["username"] = user["username"]

                flash("Login successful!", "success")
                return redirect(url_for("home"))

            else:
                flash("Invalid username or password.", "error")

        except Exception as error:
            print("Login error:", error)
            flash("Something went wrong. Please try again.", "error")

        finally:
            if cursor:
                cursor.close()

            if connection and connection.is_connected():
                connection.close()

    return render_template("login.html")


# ==========================================
# INVENTORY
# ==========================================

@app.route("/inventory/<category>")
def inventory_page(category):

    category = category.upper()

    if category not in ["A", "B"]:
        return "Invalid inventory category.", 404

    connection = None
    cursor = None

    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)

        cursor.execute(
            """
            SELECT *
            FROM products
            WHERE user_id = %s
            AND category = %s
            AND removed = 0
            """,
            (session["user_id"], category)
        )

        rows = cursor.fetchall()

        products = []

        for row in rows:

            expiry_date = row["expiry_date"]

            if hasattr(expiry_date, "strftime"):
                expiry_date = expiry_date.strftime("%Y-%m-%d")

            item = InventoryItem(
                name=row["name"],
                quantity=row["quantity"],
                expiry_date=expiry_date,
                annual_demand=float(row["annual_demand"]),
                ordering_cost=float(row["ordering_cost"]),
                holding_cost=float(row["holding_cost"]),
                avg_daily_demand=float(row["avg_daily_demand"]),
                lead_time=int(row["lead_time"]),
                demand_std_dev=float(row["demand_std_dev"]),
                category=row["category"]
            )

        
            item.id = row["product_id"]
            item.flagged = bool(row["flagged"])
            item.flag_reason = row["flag_reason"] or ""
            item.removed = bool(row["removed"])

            products.append(item)

    except Exception as error:
        print("Inventory retrieval error:", error)
        return "Could not load inventory.", 500

    finally:
        if cursor:
            cursor.close()

        if connection and connection.is_connected():
            connection.close()

    return render_template(
        "inventory.html",
        products=products,
        category=category
    )

# ==========================================
# PRODUCT DETAILS
# ==========================================

@app.route(
    "/product/<int:product_id>"
)
def product_detail(product_id):

    product = find_product(product_id)

    if product is None:

        return "Product not found.", 404

    return render_template(
        "product_detail.html",
        product=product
    )


# ==========================================
# ADD PRODUCT
# ========================================

@app.route("/add-product", methods=["GET", "POST"])
def add_product():

    if request.method == "POST":

        connection = None
        cursor = None

        try:
            name = request.form["name"].strip()
            quantity = int(request.form["quantity"])
            expiry_date = request.form["expiry_date"]
            annual_demand = float(request.form["annual_demand"])
            ordering_cost = float(request.form["ordering_cost"])
            holding_cost = float(request.form["holding_cost"])
            avg_daily_demand = float(request.form["avg_daily_demand"])
            lead_time = int(request.form["lead_time"])
            demand_std_dev = float(request.form["demand_std_dev"])
            category = request.form["category"]

            new_product = InventoryItem(
                name=name,
                quantity=quantity,
                expiry_date=expiry_date,
                annual_demand=annual_demand,
                ordering_cost=ordering_cost,
                holding_cost=holding_cost,
                avg_daily_demand=avg_daily_demand,
                lead_time=lead_time,
                demand_std_dev=demand_std_dev,
                category=category
            )

            connection = get_db_connection()
            cursor = connection.cursor()

            cursor.execute(
                """
                INSERT INTO products
                (user_id, name, quantity, expiry_date,
                 annual_demand, ordering_cost, holding_cost,
                 avg_daily_demand, lead_time, demand_std_dev, category)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """,
                (
                    session["user_id"],
                    name,
                    quantity,
                    expiry_date,
                    annual_demand,
                    ordering_cost,
                    holding_cost,
                    avg_daily_demand,
                    lead_time,
                    demand_std_dev,
                    category
                )
            )

            connection.commit()

            inventory.append(new_product)

            flash(f"{name} was added successfully.", "success")

            return redirect(
                url_for("inventory_page", category=category)
            )

        except (ValueError, KeyError) as error:
            flash(f"Could not add product: {error}", "error")

        except Exception as error:
            if connection:
                connection.rollback()

            print("Product insertion error:", error)
            flash("Could not save product. Please try again.", "error")

        finally:
            if cursor:
                cursor.close()

            if connection and connection.is_connected():
                connection.close()

    return render_template("add_product.html")

# ==========================================
# EDIT PRODUCT
# ==========================================

@app.route(
    "/product/<int:product_id>/edit",
    methods=["GET", "POST"]
)
def edit_product(product_id):

    product = find_product(product_id)

    if product is None:

        return "Product not found.", 404


    if request.method == "POST":

        try:

            product.name = request.form[
                "name"
            ].strip()

            product.quantity = int(
                request.form[
                    "quantity"
                ]
            )

            product.expiry_date = request.form[
                "expiry_date"
            ]

            product.annual_demand = float(
                request.form[
                    "annual_demand"
                ]
            )

            product.ordering_cost = float(
                request.form[
                    "ordering_cost"
                ]
            )

            product.holding_cost = float(
                request.form[
                    "holding_cost"
                ]
            )

            product.avg_daily_demand = float(
                request.form[
                    "avg_daily_demand"
                ]
            )

            product.lead_time = float(
                request.form[
                    "lead_time"
                ]
            )

            product.demand_std_dev = float(
                request.form[
                    "demand_std_dev"
                ]
            )

            product.category = request.form[
                "category"
            ]


            flash(
                "Product updated successfully.",
                "success"
            )


            return redirect(
                url_for(
                    "product_detail",
                    product_id=product.id
                )
            )


        except (
            ValueError,
            KeyError
        ) as error:

            flash(
                f"Could not update product: {error}",
                "error"
            )


    return render_template(
        "edit_product.html",
        product=product
    )


# ==========================================
# FLAG PRODUCT
# ==========================================

@app.route(
    "/product/<int:product_id>/flag",
    methods=["POST"]
)
def flag_product(product_id):

    product = find_product(product_id)

    if product is None:

        return "Product not found.", 404


    reason = request.form.get(
        "reason",
        "Other"
    )


    product.flag_product(
        reason
    )


    flash(
        f"{product.name} has been flagged.",
        "success"
    )


    return redirect(
        url_for(
            "product_detail",
            product_id=product.id
        )
    )


# ==========================================
# UNFLAG PRODUCT
# ==========================================

@app.route(
    "/product/<int:product_id>/unflag",
    methods=["POST"]
)
def unflag_product(product_id):

    product = find_product(product_id)

    if product is None:

        return "Product not found.", 404


    product.unflag_product()


    flash(
        f"{product.name} is no longer flagged.",
        "success"
    )


    return redirect(
        url_for(
            "product_detail",
            product_id=product.id
        )
    )


# ==========================================
# REMOVE PRODUCT
# ==========================================

@app.route(
    "/product/<int:product_id>/remove",
    methods=["POST"]
)
def remove_product(product_id):

    product = find_product(product_id)

    if product is None:

        return "Product not found.", 404


    product.remove_product()


    flash(
        f"{product.name} was removed from active inventory.",
        "success"
    )


    return redirect(
        url_for(
            "inventory_page",
            category=product.category
        )
    )


# ==========================================
# USER GUIDE
# ==========================================

@app.route("/user-guide")
def user_guide():

    return render_template(
        "USER GUIDE.html"
    )


# ==========================================
# SUPPORT
# ==========================================

@app.route("/support")
def support():

    return render_template(
        "SUPPORT.html"
    )

#=======================================
# User registration
#=======================================

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":

        first_name = request.form.get("first_name", "").strip()
        surname = request.form.get("surname", "").strip()
        email = request.form.get("email", "").strip()
        phone_number = request.form.get("phone_number", "").strip()
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        confirm_password = request.form.get("confirm_password", "")

        # Check that all fields have been completed
        if not all([first_name, surname, email, phone_number,
                    username, password, confirm_password]):
            flash("Please complete all fields.", "error")
            return render_template("register.html")

        # Check password length
        if len(password) < 8:
            flash("Password must contain at least 8 characters.", "error")
            return render_template("register.html")

        # Check that passwords match
        if password != confirm_password:
            flash("Passwords do not match.", "error")
            return render_template("register.html")

        connection = None
        cursor = None

        try:
            connection = get_db_connection()
            cursor = connection.cursor()

            # Check whether email or username already exists
            cursor.execute(
                """
                SELECT user_id FROM users
                WHERE email = %s OR username = %s
                """,
                (email, username)
            )

            existing_user = cursor.fetchone()

            if existing_user:
                flash("Email or username already exists.", "error")
                return render_template("register.html")

            # Hash the password before storing it
            password_hash = generate_password_hash(password)

            # Save the new user in MySQL
            cursor.execute(
                """
                INSERT INTO users
                (first_name, surname, email, phone_number,
                 username, password_hash)
                VALUES (%s, %s, %s, %s, %s, %s)
                """,
                (first_name, surname, email, phone_number,
                 username, password_hash)
            )

            connection.commit()

            flash("Registration successful! You can now log in.", "success")
            return redirect(url_for("login"))

        except Exception as error:
            if connection:
                connection.rollback()

            print("Registration error:", error)
            flash("Something went wrong during registration. Please try again.", "error")

        finally:
            if cursor:
                cursor.close()
            if connection and connection.is_connected():
                connection.close()

    return render_template("register.html")


# ==========================================
# RUN APPLICATION
# ==========================================

if __name__ == "__main__":

    app.run(
        debug=True
    )