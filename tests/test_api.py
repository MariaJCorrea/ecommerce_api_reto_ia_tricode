import pytest
from sqlalchemy.orm import Session

import database
import models


def insert_product(client, name="Teclado", price=120.0, stock=5):
    # Use the app's dependency override to insert test data into the isolated DB.
    override = client.app.dependency_overrides[database.get_db]
    db_gen = override()
    db = next(db_gen)
    product = models.Product(name=name, price=price, stock=stock)
    db.add(product)
    db.commit()
    db.refresh(product)
    product_id = product.id
    db_gen.close()
    return product_id


def test_create_user_returns_created_user(client):
    response = client.post(
        "/users/",
        json={"name": "Laura", "email": "laura@example.com"},
    )

    assert response.status_code == 200
    assert response.json()["name"] == "Laura"
    assert response.json()["email"] == "laura@example.com"
    assert response.json()["id"] is not None


def test_list_products_returns_products(client):
    product_id = insert_product(client, name="Mouse", price=50, stock=3)

    response = client.get("/products/")

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["id"] == product_id
    assert response.json()[0]["name"] == "Mouse"


def test_process_order_success_applies_existing_discount_and_reduces_stock(
    client, seeded_user
):
    product_id = insert_product(client, price=120, stock=5)

    response = client.post(
        "/orders/",
        json={"user_id": seeded_user["id"], "product_ids": [product_id]},
    )

    assert response.status_code == 200
    assert response.json()["status"] == "ok"
    assert response.json()["total"] == 110

    override = client.app.dependency_overrides[database.get_db]
    db_gen = override()
    db = next(db_gen)
    product = db.query(models.Product).filter_by(id=product_id).first()
    assert product.stock == 4
    db_gen.close()


def test_process_order_uses_full_price_when_price_is_100_or_less(
    client, seeded_user
):
    product_id = insert_product(client, price=80, stock=2)

    response = client.post(
        "/orders/",
        json={"user_id": seeded_user["id"], "product_ids": [product_id]},
    )

    assert response.status_code == 200
    assert response.json()["total"] == 80


def test_process_order_returns_404_when_user_does_not_exist(client):
    product_id = insert_product(client)

    response = client.post(
        "/orders/",
        json={"user_id": 999, "product_ids": [product_id]},
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Usuario no encontrado"


def test_process_order_returns_400_when_product_does_not_exist(
    client, seeded_user
):
    response = client.post(
        "/orders/",
        json={"user_id": seeded_user["id"], "product_ids": [999]},
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Producto 999 no existe"


def test_process_order_with_empty_product_list_creates_zero_total_order(
    client, seeded_user
):
    response = client.post(
        "/orders/",
        json={"user_id": seeded_user["id"], "product_ids": []},
    )

    assert response.status_code == 200
    assert response.json()["total"] == 0


def test_create_user_rejects_invalid_payload(client):
    response = client.post("/users/", json={"name": "Ana"})
    assert response.status_code == 422
