# System architecture and data model

## Architecture

```mermaid
flowchart TD
  U[Shop user] --> B[Browser: HTML, CSS, Jinja]
  B --> R[Flask routes]
  R --> V[Input validation and session authentication]
  V --> S[Inventory and supply-chain model]
  V --> D[(SQLite database)]
  S --> R
  D --> R
  R --> B
```

## Entity relationship diagram

```mermaid
erDiagram
  USERS {
    int id PK
    string first_name
    string surname
    string email UK
    string phone_number
    string username UK
    string password_hash
    datetime created_at
  }
  PRODUCTS {
    int id PK
    string name
    int quantity
    date expiry_date
    decimal annual_demand
    decimal ordering_cost
    decimal holding_cost
    decimal avg_daily_demand
    decimal lead_time
    decimal demand_std_dev
    string category
    boolean flagged
    string flag_reason
    boolean removed
    datetime created_at
    datetime updated_at
  }
```

Users authenticate to the prototype; product records are currently shared across the application and are not yet linked to an individual user/shop. A production multi-shop version should add a `shops` table and a `shop_id` foreign key on products, with authorization checks on every query.
