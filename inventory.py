import math
from datetime import datetime, date


# ==========================================
# INVENTORY SUPPLY CHAIN MODEL
# ==========================================

class InventoryItem:

    _next_id = 1

    def __init__(
        self,
        name,
        quantity,
        expiry_date,
        annual_demand,
        ordering_cost,
        holding_cost,
        avg_daily_demand,
        lead_time,
        demand_std_dev,
        category="A"
    ):

        if not name:
            raise ValueError("Product name cannot be empty.")

        if quantity < 0:
            raise ValueError("Quantity cannot be negative.")

        if annual_demand <= 0:
            raise ValueError("Annual demand must be greater than zero.")

        if ordering_cost <= 0:
            raise ValueError("Ordering cost must be greater than zero.")

        if holding_cost <= 0:
            raise ValueError("Holding cost must be greater than zero.")

        if avg_daily_demand < 0:
            raise ValueError("Average daily demand cannot be negative.")

        if lead_time < 0:
            raise ValueError("Lead time cannot be negative.")

        if demand_std_dev < 0:
            raise ValueError("Demand standard deviation cannot be negative.")

        # Unique ID for the product
        self.id = InventoryItem._next_id
        InventoryItem._next_id += 1

        # Basic product information
        self.name = name
        self.quantity = quantity
        self.expiry_date = expiry_date

        # Supply-chain information
        self.annual_demand = annual_demand
        self.ordering_cost = ordering_cost
        self.holding_cost = holding_cost

        self.avg_daily_demand = avg_daily_demand
        self.lead_time = lead_time
        self.demand_std_dev = demand_std_dev

        # Inventory classification
        self.category = category.upper()

        # Product condition
        self.flagged = False
        self.flag_reason = ""

        # Whether product has been removed
        self.removed = False

    # ==========================================
    # EOQ
    # ==========================================

    def calculate_eoq(self):

        return math.sqrt(
            (
                2
                * self.annual_demand
                * self.ordering_cost
            )
            / self.holding_cost
        )

    # ==========================================
    # SAFETY STOCK
    # ==========================================

    def calculate_safety_stock(self, z_score=1.65):

        return (
            z_score
            * self.demand_std_dev
            * math.sqrt(self.lead_time)
        )

    # ==========================================
    # REORDER POINT
    # ==========================================

    def calculate_reorder_point(self):

        safety_stock = self.calculate_safety_stock()

        return (
            self.avg_daily_demand * self.lead_time
            + safety_stock
        )

    # ==========================================
    # DAYS UNTIL EXPIRY
    # ==========================================

    def days_until_expiry(self):

        expiry = datetime.strptime(
            self.expiry_date,
            "%Y-%m-%d"
        ).date()

        return (expiry - date.today()).days

    # ==========================================
    # INVENTORY STATUS
    # ==========================================

    def get_status(self):

        if self.removed:
            return "Removed"

        if self.flagged:
            return "Flagged"

        days_left = self.days_until_expiry()

        if days_left < 0:
            return "Expired"

        elif days_left <= 7:
            return "Expiring Soon"

        else:
            return "Active"

    # ==========================================
    # REORDER ALERT
    # ==========================================

    def reorder_alert(self):

        if self.removed or self.flagged:
            return False

        reorder_point = self.calculate_reorder_point()

        return self.quantity <= reorder_point

    # ==========================================
    # FLAG PRODUCT
    # ==========================================

    def flag_product(self, reason):

        self.flagged = True
        self.flag_reason = reason

    # ==========================================
    # UNFLAG PRODUCT
    # ==========================================

    def unflag_product(self):

        self.flagged = False
        self.flag_reason = ""

    # ==========================================
    # REMOVE PRODUCT
    # ==========================================

    def remove_product(self):

        self.removed = True


# ==========================================
# DUMMY INVENTORY DATA
# ==========================================

inventory = [

    InventoryItem(
        name="Milk",
        quantity=20,
        expiry_date="2026-11-01",
        annual_demand=3000,
        ordering_cost=120,
        holding_cost=6,
        avg_daily_demand=15,
        lead_time=3,
        demand_std_dev=5,
        category="A"
    ),

    InventoryItem(
        name="Bread",
        quantity=12,
        expiry_date="2026-10-28",
        annual_demand=2500,
        ordering_cost=100,
        holding_cost=4,
        avg_daily_demand=20,
        lead_time=2,
        demand_std_dev=4,
        category="A"
    ),

    InventoryItem(
        name="Flour",
        quantity=150,
        expiry_date="2027-02-15",
        annual_demand=1800,
        ordering_cost=150,
        holding_cost=8,
        avg_daily_demand=8,
        lead_time=5,
        demand_std_dev=3,
        category="B"
    )
]


# ==========================================
# TEST / TERMINAL REPORT
# ==========================================

if __name__ == "__main__":

    print("=" * 60)
    print("INVENTORY MONITORING REPORT")
    print("=" * 60)

    for item in inventory:

        print(f"\nProduct: {item.name}")
        print(f"Category: Class {item.category}")
        print(f"Current Stock: {item.quantity}")
        print(f"Expiry Date: {item.expiry_date}")

        print(
            f"EOQ: "
            f"{item.calculate_eoq():.2f}"
        )

        print(
            f"Safety Stock: "
            f"{item.calculate_safety_stock():.2f}"
        )

        print(
            f"Reorder Point: "
            f"{item.calculate_reorder_point():.2f}"
        )

        print(
            f"Days Until Expiry: "
            f"{item.days_until_expiry()}"
        )

        print(
            f"Status: "
            f"{item.get_status()}"
        )

        print(
            f"Reorder Alert: "
            f"{'YES' if item.reorder_alert() else 'NO'}"
        )

    print("\nReport Generated Successfully")