import os
import django
from django.contrib.auth.models import User
from core.models import Realtor, Property

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'real_estate_agency.settings')
django.setup()

# Создание суперпользователя
try:
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
    print("Суперпользователь создан")
except:
    print("Суперпользователь уже существует")

# Создание пользователей-риелторов
realtors_data = [
    {
        'username': 'ivanov',
        'email': 'ivanov@elite-realty.ru',
        'password': 'realtor123',
        'first_name': 'Иван',
        'last_name': 'Иванов',
        'phone': '+7 (495) 123-45-67',
        'bio': 'Опытный риелтор с 10-летним стажем. Специализируюсь на элитной недвижимости в центре Москвы.',
        'experience_years': 10,
        'commission_rate': 2.5
    },
    {
        'username': 'petrova',
        'email': 'petrova@elite-realty.ru',
        'password': 'realtor123',
        'first_name': 'Мария',
        'last_name': 'Петрова',
        'phone': '+7 (495) 234-56-78',
        'bio': 'Эксперт по загородной недвижимости. Помогу найти дом вашей мечты в Подмосковье.',
        'experience_years': 8,
        'commission_rate': 3.0
    },
    {
        'username': 'sidorov',
        'email': 'sidorov@elite-realty.ru',
        'password': 'realtor123',
        'first_name': 'Алексей',
        'last_name': 'Сидоров',
        'phone': '+7 (495) 345-67-89',
        'bio': 'Специалист по коммерческой недвижимости. Помогу с выбором офисов и складов.',
        'experience_years': 12,
        'commission_rate': 2.0
    }
]

for realtor_data in realtors_data:
    try:
        # Создание пользователя
        user = User.objects.create_user(
            username=realtor_data['username'],
            email=realtor_data['email'],
            password=realtor_data['password'],
            first_name=realtor_data['first_name'],
            last_name=realtor_data['last_name']
        )
        
        # Создание риелтора
        realtor = Realtor.objects.create(
            user=user,
            first_name=realtor_data['first_name'],
            last_name=realtor_data['last_name'],
            phone=realtor_data['phone'],
            email=realtor_data['email'],
            bio=realtor_data['bio'],
            experience_years=realtor_data['experience_years'],
            commission_rate=realtor_data['commission_rate']
        )
        
        print(f"Риелтор {realtor.first_name} {realtor.last_name} создан")
        
        # Создание объектов недвижимости для каждого риелтора
        properties_data = [
            {
                'title': f'Элитная квартира в центре Москвы - {realtor.first_name}',
                'description': 'Просторная квартира с дизайнерским ремонтом в престижном районе. Все удобства, развитая инфраструктура.',
                'property_type': 'apartment',
                'price': 15000000,
                'address': 'ул. Тверская, 1',
                'area': 85.5,
                'rooms': 3,
                'bathrooms': 2,
                'year_built': 2018
            },
            {
                'title': f'Загородный дом в Подмосковье - {realtor.first_name}',
                'description': 'Современный дом с ландшафтным дизайном. Удобный доступ к городу, экологически чистый район.',
                'property_type': 'house',
                'price': 25000000,
                'address': 'Кировоградская обл., пос. Элитный, ул. Центральная, 15',
                'area': 250.0,
                'rooms': 5,
                'bathrooms': 3,
                'year_built': 2020
            },
            {
                'title': f'Коммерческое помещение - {realtor.first_name}',
                'description': 'Идеальное пространство для офиса или магазина. Удобное расположение, хороший трафик.',
                'property_type': 'commercial',
                'price': 8000000,
                'address': 'Ленинский проспект, 100',
                'area': 120.0,
                'rooms': None,
                'bathrooms': 2,
                'year_built': 2015
            }
        ]
        
        for prop_data in properties_data:
            Property.objects.create(realtor=realtor, **prop_data)
        
        print(f"Объекты недвижимости для {realtor.first_name} созданы")
        
    except Exception as e:
        print(f"Ошибка при создании риелтора {realtor_data['first_name']}: {e}")

print("База данных успешно заполнена!")
