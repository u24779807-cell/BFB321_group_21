
from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    flash
)

from inventory import InventoryItem, inventory


# ==========================================
# FLASK APPLICATION
# ==========================================

app = Flask(
    __name__,
    static_folder="Static",
    static_url_path="/static"
)

# Needed for flash messages
app.secret_key = "smart-spaza-development-key"


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

@app.route(
    "/login",
    methods=["GET", "POST"]
)
def login():

    if request.method == "POST":

        username = request.form.get(
            "username",
            ""
        ).strip()

        password = request.form.get(
            "password",
            ""
        ).strip()

        if username and password:

            return redirect(
                url_for("home")
            )

        flash(
            "Please enter your username and password.",
            "error"
        )

    return render_template(
        "login.html"
    )


# ==========================================
# INVENTORY
# ==========================================

@app.route("/inventory/<category>")
def inventory_page(category):

    category = category.upper()

    if category not in ["A", "B"]:

        return "Invalid inventory category.", 404

    products = [

        item

        for item in get_active_inventory()

        if item.category == category

    ]

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
# ==========================================

@app.route(
    "/add-product",
    methods=["GET", "POST"]
)
def add_product():

    if request.method == "POST":

        try:

            name = request.form[
                "name"
            ].strip()

            quantity = int(
                request.form[
                    "quantity"
                ]
            )

            expiry_date = request.form[
                "expiry_date"
            ]

            annual_demand = float(
                request.form[
                    "annual_demand"
                ]
            )

            ordering_cost = float(
                request.form[
                    "ordering_cost"
                ]
            )

            holding_cost = float(
                request.form[
                    "holding_cost"
                ]
            )

            avg_daily_demand = float(
                request.form[
                    "avg_daily_demand"
                ]
            )

            lead_time = float(
                request.form[
                    "lead_time"
                ]
            )

            demand_std_dev = float(
                request.form[
                    "demand_std_dev"
                ]
            )

            category = request.form[
                "category"
            ]


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


            inventory.append(
                new_product
            )


            flash(
                f"{name} was added successfully.",
                "success"
            )


            return redirect(
                url_for(
                    "inventory_page",
                    category=category
                )
            )


        except (
            ValueError,
            KeyError
        ) as error:

            flash(
                f"Could not add product: {error}",
                "error"
            )


    return render_template(
        "add_product.html"
    )


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
@ app.route("/register",methods=["GET","POST"])
def register():
    if request.method == "POST":
        first_name = request.form.get("first_name", "").strip()
        surname = request.form.get("surname", "").strip()
        email = request.form.get("email", "").strip()
        phone_number = request.form.get("phone_number", "").strip()
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        confirm_password = request.form.get("confirm_password", "")

        if password != confirm_password:
            flash("Passwords do not match.", "error")
            return render_template("register.html")

        flash("Registration submitted successfully! Database storage is not enabled yet.", "success")
        return redirect(url_for("login"))

    return render_template("register.html")


# ==========================================
# RUN APPLICATION
# ==========================================

if __name__ == "__main__":

    app.run(
        debug=True
    )