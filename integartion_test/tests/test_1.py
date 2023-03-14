from models.product import Product


def test_1(db_session, initial_data, billing_client):
    product, movies = initial_data
    print(product.id)
    assert billing_client.create_test_user(), billing_client.last_error
    print(billing_client.get_test_user_token())
    return
