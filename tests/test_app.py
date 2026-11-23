import app as application


def setup_client(tmp_path, monkeypatch):
    monkeypatch.setattr(application, "DATABASE", tmp_path / "test.db")
    application.init_db()
    application.app.config.update(TESTING=True, SECRET_KEY="test-secret")
    client = application.app.test_client()
    client.post("/register", data={
        "first_name": "Test", "surname": "User", "email": "test@example.com",
        "phone_number": "000", "username": "tester", "password": "password123",
        "confirm_password": "password123"
    })
    client.post("/login", data={"username": "tester", "password": "password123"})
    return client


def product_form(name="Test maize"):
    return {"name": name, "quantity": "100", "expiry_date": "2030-01-01", "annual_demand": "1000",
            "ordering_cost": "50", "holding_cost": "5", "avg_daily_demand": "3",
            "lead_time": "4", "demand_std_dev": "2", "category": "A"}


def test_login_required_and_registration(tmp_path, monkeypatch):
    monkeypatch.setattr(application, "DATABASE", tmp_path / "test.db")
    application.init_db()
    application.app.config.update(TESTING=True)
    client = application.app.test_client()
    assert client.get("/").status_code == 302
    response = client.post("/register", data={"first_name":"T", "surname":"U", "email":"t@x.com",
        "username":"user1", "password":"password123", "confirm_password":"password123"}, follow_redirects=True)
    assert b"Please log in" in response.data or b"Log In" in response.data
    assert client.post("/login", data={"username":"user1", "password":"password123"}).status_code == 302


def test_add_edit_flag_remove_flow(tmp_path, monkeypatch):
    client = setup_client(tmp_path, monkeypatch)
    response = client.post("/add-product", data=product_form())
    assert response.status_code == 302
    with application.get_db() as conn:
        product_id = conn.execute("SELECT id FROM products WHERE name='Test maize'").fetchone()[0]
    assert client.get(f"/product/{product_id}").status_code == 200
    assert client.post(f"/product/{product_id}/flag", data={"reason":"Damaged"}).status_code == 302
    assert client.get(f"/product/{product_id}").status_code == 200
    assert client.post(f"/product/{product_id}/unflag").status_code == 302
    assert client.post(f"/product/{product_id}/remove").status_code == 302
    assert client.get("/inventory/A").status_code == 200


def test_dashboard_and_json_api(tmp_path, monkeypatch):
    client = setup_client(tmp_path, monkeypatch)
    assert client.get("/").status_code == 200
    assert client.get("/api/dashboard").status_code == 200
    assert client.get("/api/products").status_code == 200
    response = client.post("/api/products", json=product_form("API oats"))
    assert response.status_code == 201


def test_product_edit_persists_changes(tmp_path, monkeypatch):
    client = setup_client(tmp_path, monkeypatch)
    client.post("/add-product", data=product_form("Before edit"))
    with application.get_db() as conn:
        product_id = conn.execute("SELECT id FROM products WHERE name='Before edit'").fetchone()[0]
    changed = product_form("After edit")
    changed["quantity"] = "55"
    assert client.post(f"/product/{product_id}/edit", data=changed).status_code == 302
    updated = application.find_product(product_id)
    assert updated.name == "After edit"
    assert updated.quantity == 55
