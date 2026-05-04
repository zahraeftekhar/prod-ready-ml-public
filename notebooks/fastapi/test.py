from unittest import mock

# Uncomment this
from app import Item, app, get_item, items, update_items
from fastapi.testclient import TestClient


# Test the program logic
def test_update_items():
    items.clear()
    item = Item(name="candy", description="nice chocolates", price=5, tax=1)

    res = update_items(item)
    assert res["price_with_tax"] == 6
    assert items["candy"] == res


def test_update_items_without_tax():
    items.clear()
    item = Item(
        name="water",
        description="still water",
        price=2,
    )

    res = update_items(item)
    assert "price_with_tax" not in res
    assert res == {
        "name": "water",
        "description": "still water",
        "price": 2,
        "tax": None,
    }
    assert items["water"] == res


def test_get_item_found():
    items.clear()
    items["foo"] = {"my": "fake item"}

    assert get_item("foo") == {"my": "fake item"}


def test_get_item_missing():
    items.clear()

    assert get_item("missing") is None


# Test the endpoints
client = TestClient(app)


def test_get_item_endoint():
    items.clear()
    items["foo"] = {"my": "fake item"}

    res = client.get("/item/foo")
    assert res.status_code == 200
    assert res.json() == {"my": "fake item"}


def test_create_item_endpoint():
    items.clear()
    res = client.post(
        "/items/",
        json={"name": "snack", "description": "chips", "price": 3, "tax": 0.5},
    )

    assert res.status_code == 200
    assert res.json() == {
        "name": "snack",
        "description": "chips",
        "price": 3,
        "tax": 0.5,
        "price_with_tax": 3.5,
    }
    assert items["snack"]["price_with_tax"] == 3.5


# Test a mocked-up endpoint
def test_get_item_mocked():
    items.clear()
    with mock.patch("app.get_item", return_value={"my": "faked fake item"}):
        res = client.get("/item/foo")
        assert res.status_code == 200
        assert res.json() == {"my": "faked fake item"}
