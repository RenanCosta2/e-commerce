from faker import Faker
from django.contrib.auth.hashers import make_password

fake = Faker('pt_BR')

class UserFactory:

    @staticmethod
    def cpf_generator():
        cpf = [fake.random_int(min=0, max=9) for _ in range(9)]
        return f"{cpf[0]}{cpf[1]}{cpf[2]}.{cpf[3]}{cpf[4]}{cpf[5]}.{cpf[6]}{cpf[7]}{cpf[8]}-{fake.random_int(10, 99)}"

    @staticmethod
    def create(staff=False):
        password = fake.password(length=8, special_chars=True, upper_case=True, digits=True)

        new_user_data = {
            'username': fake.user_name(),
            'first_name': fake.first_name(),
            'last_name': fake.last_name(),
            'cpf': UserFactory.cpf_generator(),
            'email': fake.email(),
            'password': make_password(password),
            'is_staff': staff
        }

        return new_user_data
    
class AddressFactory:

    @staticmethod
    def create(user):

        new_address_data = {
            'user': user, 
            'street': fake.street_address(),
            'city': fake.city(),
            'state': fake.state(),
            'zip_code': fake.postcode(),
            'country': 'Brazil'
        }

        return new_address_data