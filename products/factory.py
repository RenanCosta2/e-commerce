from faker import Faker

fake = Faker('pt_BR')

class ProductFactory:

    @staticmethod
    def create():

        new_product_data = {
            'name': fake.random_element(elements=[
                "Smartphone XYZ 5G", 
                "Notebook Alpha Pro", 
                "Fone de Ouvido Zeta", 
                "Smartwatch Omega", 
                "Câmera Digital Sigma"
            ]),
            'category': fake.random_element(elements=[
                "Electronics", 
                "Appliances", 
                "Furniture", 
                "Toys & Games", 
                "Fashion"
            ]),
            'description': fake.text(max_nb_chars=60),
            'value': round(fake.random_number(digits=4) / 100, 2),
            'storage': fake.random_int(min=1, max=500)
        }

        return new_product_data