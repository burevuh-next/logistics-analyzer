#!/usr/bin/env python3
"""
Генератор реалистичных данных по логистике
Создает датасет с 1000+ записей для анализа
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
from faker import Faker
import os

# Инициализация Faker для русских данных
fake = Faker('ru_RU')

def generate_cities_weights():
    """Генерация городов с весами (вероятностью отправки)"""
    cities = {
        'Москва': 0.25,           # 25% всех перевозок
        'Санкт-Петербург': 0.15,  # 15%
        'Екатеринбург': 0.10,
        'Новосибирск': 0.10,
        'Казань': 0.08,
        'Красноярск': 0.07,
        'Нижний Новгород': 0.06,
        'Челябинск': 0.05,
        'Омск': 0.05,
        'Самара': 0.04,
        'Ростов-на-Дону': 0.03,
        'Уфа': 0.02
    }
    return cities

def generate_carriers():
    """Генерация перевозчиков с характеристиками"""
    carriers = [
        {'name': 'Деловые Линии', 'price_factor': 1.0, 'reliability': 0.95},
        {'name': 'ПЭК', 'price_factor': 0.9, 'reliability': 0.92},
        {'name': 'ЖДД', 'price_factor': 0.8, 'reliability': 0.98},
        {'name': 'Грузовоз', 'price_factor': 0.85, 'reliability': 0.90},
        {'name': 'Энергия', 'price_factor': 1.1, 'reliability': 0.96},
        {'name': 'Мэйджор', 'price_factor': 1.2, 'reliability': 0.99},
        {'name': 'Байкал Сервис', 'price_factor': 0.95, 'reliability': 0.93},
        {'name': 'Ратэк', 'price_factor': 0.88, 'reliability': 0.91}
    ]
    return carriers

def generate_cargo_types():
    """Типы грузов с характеристиками"""
    cargo_types = [
        {'type': 'Электроника', 'fragility': 0.8, 'density': 0.3, 'price_factor': 1.5},
        {'type': 'Одежда', 'fragility': 0.2, 'density': 0.4, 'price_factor': 1.0},
        {'type': 'Продукты', 'fragility': 0.6, 'density': 0.7, 'price_factor': 1.2},
        {'type': 'Стройматериалы', 'fragility': 0.1, 'density': 2.5, 'price_factor': 0.8},
        {'type': 'Автозапчасти', 'fragility': 0.4, 'density': 1.2, 'price_factor': 1.1},
        {'type': 'Мебель', 'fragility': 0.5, 'density': 0.9, 'price_factor': 1.3},
        {'type': 'Химия', 'fragility': 0.7, 'density': 1.1, 'price_factor': 1.4},
        {'type': 'Медицина', 'fragility': 0.9, 'density': 0.5, 'price_factor': 1.6},
        {'type': 'Канцелярия', 'fragility': 0.3, 'density': 0.6, 'price_factor': 1.0},
        {'type': 'Игрушки', 'fragility': 0.4, 'density': 0.4, 'price_factor': 1.1}
    ]
    return cargo_types

def get_distance(from_city, to_city):
    """Примерные расстояния между городами (в км)"""
    distances = {
        ('Москва', 'Санкт-Петербург'): 710,
        ('Москва', 'Екатеринбург'): 1800,
        ('Москва', 'Новосибирск'): 2800,
        ('Москва', 'Казань'): 800,
        ('Москва', 'Нижний Новгород'): 400,
        ('Санкт-Петербург', 'Москва'): 710,
        ('Санкт-Петербург', 'Екатеринбург'): 2200,
        ('Екатеринбург', 'Новосибирск'): 1500,
        ('Екатеринбург', 'Москва'): 1800,
        ('Новосибирск', 'Красноярск'): 800,
        ('Казань', 'Москва'): 800,
        ('Казань', 'Санкт-Петербург'): 1500,
        # Добавьте другие расстояния по необходимости
    }
    
    # Если расстояние известно - возвращаем его
    if (from_city, to_city) in distances:
        return distances[(from_city, to_city)]
    else:
        # Иначе генерируем случайное расстояние
        base_distance = random.randint(300, 3000)
        # Добавляем случайное отклонение
        return base_distance + random.randint(-100, 100)

def generate_shipment(shipment_id, cities_weights):
    """Генерация одной записи о перевозке"""
    
    # Выбор городов с учетом весов
    cities = list(cities_weights.keys())
    weights = list(cities_weights.values())
    
    from_city = random.choices(cities, weights=weights)[0]
    
    # Город назначения не должен совпадать с городом отправления
    to_city_options = [c for c in cities if c != from_city]
    to_city = random.choice(to_city_options)
    
    # Расчет расстояния
    distance = get_distance(from_city, to_city)
    
    # Выбор перевозчика
    carriers = generate_carriers()
    carrier = random.choice(carriers)
    
    # Выбор типа груза
    cargo_types = generate_cargo_types()
    cargo = random.choice(cargo_types)
    
    # Вес груза (кг)
    weight = random.randint(50, 5000)
    
    # Объем груза (м³) - зависит от веса и плотности
    volume = weight / 1000 * cargo['density']  # упрощенная формула
    
    # Базовая стоимость (руб/км)
    base_cost_per_km = random.uniform(15, 50)
    
    # Модификаторы стоимости
    distance_modifier = 1.0
    if distance > 2000:
        distance_modifier = 0.9  # скидка на длинные расстояния
    elif distance < 500:
        distance_modifier = 1.2  # надбавка на короткие
    
    # Финальная стоимость
    cost = (
        base_cost_per_km * 
        distance * 
        carrier['price_factor'] * 
        cargo['price_factor'] * 
        distance_modifier * 
        (1 + weight / 10000)  # чем больше вес, тем дороже
    )
    
    # Добавляем случайное отклонение
    cost *= random.uniform(0.9, 1.1)
    cost = round(cost, 2)
    
    # Дата перевозки (за последний год)
    start_date = datetime(2023, 1, 1)
    end_date = datetime(2024, 1, 31)
    random_date = start_date + timedelta(
        days=random.randint(0, (end_date - start_date).days)
    )
    
    # Статус доставки
    status_options = ['Доставлен', 'В пути', 'Ожидает отправки', 'Задержан', 'Отменен']
    status_weights = [0.85, 0.08, 0.04, 0.02, 0.01]
    status = random.choices(status_options, weights=status_weights)[0]
    
    # Время доставки (дни)
    if status == 'Доставлен':
        delivery_days = random.randint(
            max(1, distance // 800),  # минимальное время
            max(3, distance // 400)   # максимальное время
        )
    else:
        delivery_days = None
    
    return {
        'shipment_id': shipment_id,
        'from_city': from_city,
        'to_city': to_city,
        'distance_km': distance,
        'weight_kg': weight,
        'volume_m3': round(volume, 2),
        'cargo_type': cargo['type'],
        'carrier': carrier['name'],
        'cost_rub': cost,
        'base_cost_per_km': round(base_cost_per_km, 2),
        'date': random_date.strftime('%Y-%m-%d'),
        'status': status,
        'delivery_days': delivery_days,
        'carrier_reliability': carrier['reliability'],
        'cargo_fragility': cargo['fragility'],
        'customer_id': fake.random_int(min=1000, max=9999),
        'customer_segment': random.choice(['A', 'B', 'C']),
        'insurance': random.choice([True, False]),
        'insurance_cost': round(cost * 0.02, 2) if random.random() > 0.7 else 0,
        'fuel_surcharge': round(cost * random.uniform(0.05, 0.15), 2),
        'priority': random.choice(['Стандарт', 'Экспресс', 'Супер-экспресс']),
        'payment_method': random.choice(['Предоплата', 'Постоплата', '50/50']),
        'has_return': random.random() > 0.9,  # 10% имеют обратный рейс
        'return_cost': round(cost * 0.8, 2) if random.random() > 0.9 else 0
    }

def main():
    """Основная функция"""
    print("🚚 Генерация реалистичных данных по логистике...")
    
    # Параметры генерации
    NUM_RECORDS = 1500  # Количество записей
    
    # Генерация данных
    cities_weights = generate_cities_weights()
    data = []
    
    for i in range(1, NUM_RECORDS + 1):
        if i % 100 == 0:
            print(f"  Генерация записи {i}/{NUM_RECORDS}...")
        
        shipment = generate_shipment(i, cities_weights)
        data.append(shipment)
    
    # Создание DataFrame
    df = pd.DataFrame(data)
    
    # Сохранение в CSV
    output_path = 'data/shipments_extended.csv'
    df.to_csv(output_path, index=False, encoding='utf-8')
    
    # Статистика
    print(f"\n✅ Данные сохранены в {output_path}")
    print(f"📊 Статистика:")
    print(f"   Всего записей: {len(df)}")
    print(f"   Период данных: {df['date'].min()} - {df['date'].max()}")
    print(f"   Городов отправления: {df['from_city'].nunique()}")
    print(f"   Перевозчиков: {df['carrier'].nunique()}")
    print(f"   Типов грузов: {df['cargo_type'].nunique()}")
    print(f"   Общая стоимость: {df['cost_rub'].sum():,.0f} руб")
    print(f"   Средняя стоимость: {df['cost_rub'].mean():,.0f} руб")
    print(f"   Общий вес: {df['weight_kg'].sum():,.0f} кг")
    
    # Сохранение дополнительной информации
    stats_path = 'data/dataset_statistics.txt'
    with open(stats_path, 'w', encoding='utf-8') as f:
        f.write("Статистика датасета shipments_extended.csv\n")
        f.write("="*50 + "\n\n")
        f.write(f"Всего записей: {len(df)}\n")
        f.write(f"Период: {df['date'].min()} - {df['date'].max()}\n")
        f.write(f"Уникальных городов: {df['from_city'].nunique()}\n")
        f.write(f"Уникальных перевозчиков: {df['carrier'].nunique()}\n\n")
        
        f.write("Топ-5 городов отправления:\n")
        top_cities = df['from_city'].value_counts().head(5)
        for city, count in top_cities.items():
            f.write(f"  {city}: {count} перевозок\n")
        
        f.write("\nТоп-5 перевозчиков:\n")
        top_carriers = df['carrier'].value_counts().head(5)
        for carrier, count in top_carriers.items():
            f.write(f"  {carrier}: {count} перевозок\n")
    
    print(f"\n📋 Подробная статистика сохранена в {stats_path}")
    
    # Также создаем уменьшенную версию для быстрых тестов
    sample_df = df.sample(100, random_state=42)
    sample_path = 'data/shipments_sample.csv'
    sample_df.to_csv(sample_path, index=False, encoding='utf-8')
    print(f"📦 Создан sample файл: {sample_path} (100 записей)")

if __name__ == '__main__':
    # Установите faker если нет: pip install faker
    try:
        from faker import Faker
    except ImportError:
        print("Установите faker: pip install faker")
        exit(1)
    
    main()
