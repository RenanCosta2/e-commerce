from faker import Faker

fake = Faker('pt_BR')

class ItemCartFactory:

    @staticmethod
    def create(product, quantity=fake.random_int(min=1, max=10)):

        new_item_cart_data = {
            'product': product.id,
            'quantity': quantity
        }

        return new_item_cart_data