# Smart Spaza API Contract

All endpoints below require an authenticated browser session. Responses use JSON.

## `GET /api/products`
Returns an array containing `id`, `name`, `quantity`, `expiry_date`, `category`, `status`, `eoq`, `safety_stock`, `reorder_point` and `reorder_alert`.

## `POST /api/products`
Creates a product. Send `Content-Type: application/json` with:

```json
{
  "name": "Rice",
  "quantity": 40,
  "expiry_date": "2027-05-30",
  "annual_demand": 1200,
  "ordering_cost": 80,
  "holding_cost": 4,
  "avg_daily_demand": 4,
  "lead_time": 5,
  "demand_std_dev": 1.2,
  "category": "B"
}
```

Returns HTTP `201` and `{ "id": 4, "message": "Product created" }`. Invalid input returns HTTP `400` and an `error` message.

## `GET /api/dashboard`
Returns the KPI object: `total_products`, `expiring_soon`, `expired`, `flagged`, `low_stock`, and `total_units`.

## Error behaviour
- `400`: invalid request data.
- `404`: unknown route or product.
- Unauthenticated browser/API requests are redirected to the login page.
