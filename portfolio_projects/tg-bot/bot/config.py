import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
ADMIN_IDS = [int(id.strip()) for id in os.getenv('ADMIN_IDS', '').split(',') if id.strip()]

UNIVERSITY_INFO = {
    "name": "Университет «Синергия»",
    "contacts": {
        "phone": "+7 (800) 100-00-11",
        "secondary_phone": "+7 (495) 800-10-01",
        "email": "synergy@synergy.ru",
        "website": "https://synergy.ru/",
        "admission_site": "https://synergy.ru/abiturientam"
    },
    "working_hours": {
        "weekdays": "9:00-20:00",
        "weekends": "10:00-17:00"
    },
    "campuses": [
        {
            "name": "Корпус на Соколе",
            "address": "Ленинградский проспект, д. 80, корпуса Е, Ж, Г",
            "metro": "Сокол",
            "hours": "Пн-Пт 08:30-22:10, Сб-Вс 10:00-17:00",
            "map": "https://yandex.ru/maps/-/CCUQjXc~gD"
        },
        {
            "name": "Корпус на Семеновской",
            "address": "Измайловский Вал, д. 2",
            "metro": "Семеновская",
            "hours": "Пн-Пт 08:30-22:10, Сб-Вс 10:00-17:00",
            "map": "https://yandex.ru/maps/-/CCUQjXcPSC"
        }
    ],
    "admission": {
        "documents": "паспорт, документ об образовании, фото 3x4",
        "features": [
            "Кредит на образование от 3% годовых",
            "Бюджетные места на некоторых факультетах",
            "Гарантия трудоустройства"
        ]
    },
    "faculties": [
        "Экономика",
        "Менеджмент",
        "Юриспруденция",
        "Информационные технологии",
        "Дизайн",
        "Лингвистика",
        "Психология"
    ]
}