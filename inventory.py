import math
from datetime import datetime

# ==========================================
# INVENTORY SUPPLY CHAIN MODEL
# ==========================================

class InventoryItem:

    def __init__(self, name, quantity, expiry_date,
                 annual_demand, ordering_cost,
                 holding_cost, avg_daily_demand,
                 lead_time, demand_std_dev):

        self.name = name
        self.quantity = quantity
        self.expiry_date = expiry_date

        self.annual_demand = annual_demand
        self.ordering_cost = ordering_cost
        self.holding_cost = holding_cost

        self.avg_daily_demand = avg_daily_demand
        self.lead_time = lead_time
        self.demand_std_dev = demand_std_dev

    # EOQ Calculation
    def calculate_eoq(self):
        return math.sqrt(
            (2 * self.annual_demand * self.ordering_cost)
            / self.holding_cost
        )

    # Safety Stock Calculation
    def calculate_safety_stock(self, z_score=1.65):
        return (
            z_score *
            self.demand_std_dev *
            math.sqrt(self.lead_time)
        )

    # Reorder Point Calculation
    def calculate_reorder_point(self):
        safety_stock = self.calculate_safety_stock()

        return (
            self.avg_daily_demand *
            self.lead_time +
            safety_stock
        )

    # Days Until Expiry
    def days_until_expiry(self):
        expiry = datetime.strptime(
            self.expiry_date,
            "%Y-%m-%d"
        )

        return (expiry - datetime.now()).days

    # Inventory Status
    def get_status(self):

        days_left = self.days_until_expiry()

        if days_left < 0:
            return "Expired"

        elif days_left <= 7:
            return "Expiring Soon"

        else:
            return "Active"

    # Reorder Alert
    def reorder_alert(self):

        reorder_point = self.calculate_reorder_point()

        return self.quantity <= reorder_point


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
        demand_std_dev=5
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
        demand_std_dev=4
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
        demand_std_dev=3
    )
]


# ==========================================
# DISPLAY RESULTS
# ==========================================

print("=" * 60)
print("INVENTORY MONITORING REPORT")
print("=" * 60)

for item in inventory:

    eoq = item.calculate_eoq()
    ss = item.calculate_safety_stock()
    rop = item.calculate_reorder_point()
    status = item.get_status()
    reorder = item.reorder_alert()

    print(f"\nProduct: {item.name}")
    print(f"Current Stock: {item.quantity}")
    print(f"Expiry Date: {item.expiry_date}")

    print(f"EOQ: {eoq:.2f}")
    print(f"Safety Stock: {ss:.2f}")
    print(f"Reorder Point: {rop:.2f}")

    print(f"Status: {status}")

    if reorder:
        print("REORDER ALERT: YES")
    else:
        print("REORDER ALERT: NO")

print("\nReport Generated Successfully")