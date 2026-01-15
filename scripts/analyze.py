#!/usr/bin/env python3
"""
Анализатор логистических данных
Автор: [Ваше Имя]
Дата: [Сегодняшняя дата]
"""

import csv
import statistics
from datetime import datetime
from pathlib import Path
from collections import defaultdict


class LogisticsAnalyzer:
    """Класс для анализа логистических данных"""
    
    def __init__(self, data_path):
        self.data_path = Path(data_path)
        self.shipments = []
        self.load_data()
    
    def load_data(self):
        """Загрузка данных из CSV файла"""
        if not self.data_path.exists():
            raise FileNotFoundError(f"Файл {self.data_path} не найден")
        
        with open(self.data_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                # Преобразование типов данных
                row['distance_km'] = int(row['distance_km'])
                row['weight_kg'] = int(row['weight_kg'])
                row['cost_rub'] = float(row['cost_rub'])
                row['date'] = datetime.strptime(row['date'], '%Y-%m-%d')
                self.shipments.append(row)
        
        print(f"✅ Загружено {len(self.shipments)} записей")
    
    def calculate_kpis(self):
        """Расчет ключевых показателей эффективности"""
        if not self.shipments:
            return {}
        
        # Базовые метрики
        total_cost = sum(s['cost_rub'] for s in self.shipments)
        total_distance = sum(s['distance_km'] for s in self.shipments)
        total_weight = sum(s['weight_kg'] for s in self.shipments)
        
        # Стоимость за км и за кг
        cost_per_km = [s['cost_rub'] / s['distance_km'] for s in self.shipments if s['distance_km'] > 0]
        cost_per_kg = [s['cost_rub'] / s['weight_kg'] for s in self.shipments if s['weight_kg'] > 0]
        
        kpis = {
            'total_shipments': len(self.shipments),
            'total_cost': total_cost,
            'total_distance': total_distance,
            'total_weight': total_weight,
            'avg_cost_per_km': statistics.mean(cost_per_km) if cost_per_km else 0,
            'avg_cost_per_kg': statistics.mean(cost_per_kg) if cost_per_kg else 0,
            'avg_distance': total_distance / len(self.shipments),
            'avg_weight': total_weight / len(self.shipments),
        }
        
        return kpis
    
    def analyze_by_carrier(self):
        """Анализ по перевозчикам"""
        carrier_stats = defaultdict(lambda: {
            'count': 0, 'total_cost': 0, 'total_distance': 0, 'total_weight': 0
        })
        
        for shipment in self.shipments:
            carrier = shipment['carrier']
            stats = carrier_stats[carrier]
            stats['count'] += 1
            stats['total_cost'] += shipment['cost_rub']
            stats['total_distance'] += shipment['distance_km']
            stats['total_weight'] += shipment['weight_kg']
        
        # Рассчитываем средние значения для каждого перевозчика
        for carrier, stats in carrier_stats.items():
            stats['avg_cost_per_shipment'] = stats['total_cost'] / stats['count']
            stats['avg_cost_per_km'] = stats['total_cost'] / stats['total_distance']
            stats['avg_cost_per_kg'] = stats['total_cost'] / stats['total_weight']
        
        return dict(carrier_stats)
    
    def find_most_profitable_routes(self, top_n=3):
        """Поиск самых выгодных маршрутов (мин стоимость за км)"""
        routes = {}
        
        for shipment in self.shipments:
            route_key = f"{shipment['from_city']} → {shipment['to_city']}"
            cost_per_km = shipment['cost_rub'] / shipment['distance_km']
            
            if route_key not in routes or cost_per_km < routes[route_key]['cost_per_km']:
                routes[route_key] = {
                    'cost_per_km': cost_per_km,
                    'carrier': shipment['carrier'],
                    'distance': shipment['distance_km'],
                    'cost': shipment['cost_rub']
                }
        
        # Сортируем по стоимости за км (самые выгодные первые)
        sorted_routes = sorted(routes.items(), key=lambda x: x[1]['cost_per_km'])
        return sorted_routes[:top_n]
    
    def generate_report(self):
        """Генерация полного отчета"""
        print("\n" + "="*60)
        print("📊 ОТЧЕТ ПО ЛОГИСТИЧЕСКИМ ДАННЫМ")
        print("="*60)
        
        # 1. Общие KPI
        kpis = self.calculate_kpis()
        print("\n1. КЛЮЧЕВЫЕ ПОКАЗАТЕЛИ:")
        print(f"   • Всего перевозок: {kpis['total_shipments']}")
        print(f"   • Общая стоимость: {kpis['total_cost']:,} руб")
        print(f"   • Общее расстояние: {kpis['total_distance']:,} км")
        print(f"   • Общий вес: {kpis['total_weight']:,} кг")
        print(f"   • Средняя стоимость за км: {kpis['avg_cost_per_km']:.2f} руб/км")
        print(f"   • Средняя стоимость за кг: {kpis['avg_cost_per_kg']:.2f} руб/кг")
        
        # 2. Анализ по перевозчикам
        print("\n2. АНАЛИЗ ПО ПЕРЕВОЗЧИКАМ:")
        carrier_stats = self.analyze_by_carrier()
        for carrier, stats in carrier_stats.items():
            print(f"   📦 {carrier}:")
            print(f"      Перевозок: {stats['count']}")
            print(f"      Средняя стоимость за перевозку: {stats['avg_cost_per_shipment']:,.0f} руб")
            print(f"      Средняя стоимость за км: {stats['avg_cost_per_km']:.2f} руб/км")
        
        # 3. Самые выгодные маршруты
        print("\n3. САМЫЕ ВЫГОДНЫЕ МАРШРУТЫ (низкая стоимость за км):")
        best_routes = self.find_most_profitable_routes()
        for i, (route, data) in enumerate(best_routes, 1):
            print(f"   {i}. {route}")
            print(f"      Перевозчик: {data['carrier']}")
            print(f"      Стоимость за км: {data['cost_per_km']:.2f} руб/км")
            print(f"      Общая стоимость: {data['cost']:,} руб")
        
        print("\n" + "="*60)
        print("✅ Отчет сгенерирован успешно!")


def main():
    """Основная функция"""
    try:
        # Создаем анализатор
        analyzer = LogisticsAnalyzer('data/shipments_extended.csv')
        
        # Генерируем отчет
        analyzer.generate_report()
        
        # Дополнительно: сохраняем KPI в файл
        kpis = analyzer.calculate_kpis()
        with open('data/kpi_report.txt', 'w', encoding='utf-8') as f:
            f.write("Отчет KPI\n")
            f.write("="*40 + "\n")
            for key, value in kpis.items():
                f.write(f"{key}: {value}\n")
        
        print("\n📁 Отчет KPI сохранен в data/kpi_report.txt")
        
    except FileNotFoundError as e:
        print(f"❌ Ошибка: {e}")
        print("Создайте файл data/shipments.csv с данными")
    except Exception as e:
        print(f"❌ Неожиданная ошибка: {e}")


if __name__ == "__main__":
    main()