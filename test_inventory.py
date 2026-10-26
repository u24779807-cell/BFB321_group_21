import unittest

from inventory import InventoryItem


class TestInventoryItem(unittest.TestCase):

    def setUp(self):

        self.product = InventoryItem(

            name="Test Product",

            quantity=20,

            expiry_date="2030-01-01",

            annual_demand=3000,

            ordering_cost=120,

            holding_cost=6,

            avg_daily_demand=15,

            lead_time=3,

            demand_std_dev=5,

            category="A"
        )


    def test_eoq(self):

        eoq = self.product.calculate_eoq()

        expected = (
            (2 * 3000 * 120 / 6)
            ** 0.5
        )

        self.assertAlmostEqual(
            eoq,
            expected
        )


    def test_safety_stock(self):

        safety_stock = (
            self.product.calculate_safety_stock()
        )

        self.assertGreater(
            safety_stock,
            0
        )


    def test_reorder_point(self):

        reorder_point = (
            self.product.calculate_reorder_point()
        )

        expected = (
            15 * 3
            + self.product.calculate_safety_stock()
        )

        self.assertAlmostEqual(
            reorder_point,
            expected
        )


    def test_active_status(self):

        self.assertEqual(
            self.product.get_status(),
            "Active"
        )


    def test_reorder_alert(self):

        self.product.quantity = 1

        self.assertTrue(
            self.product.reorder_alert()
        )


    def test_flag_product(self):

        self.product.flag_product(
            "Spoiled"
        )

        self.assertEqual(
            self.product.get_status(),
            "Flagged"
        )

        self.assertEqual(
            self.product.flag_reason,
            "Spoiled"
        )


    def test_unflag_product(self):

        self.product.flag_product(
            "Damaged"
        )

        self.product.unflag_product()

        self.assertFalse(
            self.product.flagged
        )


if __name__ == "__main__":

    unittest.main()