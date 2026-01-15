#!/usr/bin/env python3
"""
Анализ расширенного датасета
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

class ExtendedLogisticsAnalyzer:
    def __init__(self, data_path):
        self.df = pd.read_csv(data_path)
        print(f"📁 Загружено {len(self.df)} записей из {data_path}")
        
    def basic_analysis(self):
        """Базовый анализ"""
        print("\n" + "="*60)
        print("📊 БАЗОВЫЙ АНАЛИЗ ДАННЫХ")
        print("="*60)
        
        # Основные статистики
        print(f"\n📈 Основные показатели:")
        print(f"   Всего перевозок: {len(self.df):,}")
        print(f"   Период данных: {self.df['date'].min()} - {self.df['date'].max()}")
        print(f"   Уникальных городов отправления: {self.df['from_city'].nunique()}")
        print(f"   Уникальных перевозчиков: {self.df['carrier'].nunique()}")
        
        # Финансы
        total_cost = self.df['cost_rub'].sum()
        avg_cost = self.df['cost_rub'].mean()
        print(f"\n💰 Финансовые показатели:")
        print(f"   Общая стоимость: {total_cost:,.0f} руб")
        print(f"   Средняя стоимость: {avg_cost:,.0f} руб")
        print(f"   Медианная стоимость: {self.df['cost_rub'].median():,.0f} руб")
        
        # Вес и расстояние
        total_weight = self.df['weight_kg'].sum()
        total_distance = self.df['distance_km'].sum()
        print(f"\n⚖️  Физические показатели:")
        print(f"   Общий вес: {total_weight:,.0f} кг")
        print(f"   Общее расстояние: {total_distance:,.0f} км")
        print(f"   Средняя стоимость за км: {(total_cost/total_distance):.2f} руб/км")
        print(f"   Средняя стоимость за кг: {(total_cost/total_weight):.2f} руб/кг")
    
    def carrier_analysis(self):
        """Анализ перевозчиков"""
        print("\n" + "="*60)
        print("🚚 АНАЛИЗ ПЕРЕВОЗЧИКОВ")
        print("="*60)
        
        carrier_stats = self.df.groupby('carrier').agg({
            'shipment_id': 'count',
            'cost_rub': ['sum', 'mean', 'median'],
            'distance_km': 'mean',
            'weight_kg': 'mean'
        }).round(2)
        
        carrier_stats.columns = ['Кол-во', 'Сумма_руб', 'Среднее_руб', 'Медиана_руб', 'Ср_расстояние_км', 'Ср_вес_кг']
        
        print("\n📋 Статистика по перевозчикам:")
        print(carrier_stats.sort_values('Кол-во', ascending=False))
        
        # Эффективность перевозчиков
        self.df['cost_per_km'] = self.df['cost_rub'] / self.df['distance_km']
        carrier_efficiency = self.df.groupby('carrier')['cost_per_km'].mean().sort_values()
        
        print(f"\n🏆 Самые выгодные перевозчики (низкая стоимость за км):")
        for carrier, cost in carrier_efficiency.head(5).items():
            print(f"   {carrier}: {cost:.2f} руб/км")
    
    def route_analysis(self):
        """Анализ маршрутов"""
        print("\n" + "="*60)
        print("🛣️  АНАЛИЗ МАРШРУТОВ")
        print("="*60)
        
        # Самые популярные маршруты
        routes = self.df.groupby(['from_city', 'to_city']).agg({
            'shipment_id': 'count',
            'cost_rub': 'mean',
            'distance_km': 'mean'
        }).round(2)
        
        routes.columns = ['Кол-во', 'Ср_стоимость', 'Ср_расстояние']
        routes = routes.sort_values('Кол-во', ascending=False)
        
        print("\n🔥 Топ-10 самых популярных маршрутов:")
        print(routes.head(10))
        
        # Самые дорогие маршруты
        self.df['route'] = self.df['from_city'] + ' → ' + self.df['to_city']
        route_cost = self.df.groupby('route')['cost_per_km'].mean().sort_values(ascending=False)
        
        print(f"\n💸 Топ-5 самых дорогих маршрутов (за км):")
        for route, cost in route_cost.head(5).items():
            print(f"   {route}: {cost:.2f} руб/км")
    
    def seasonal_analysis(self):
        """Анализ сезонности"""
        if 'month' in self.df.columns:
            print("\n" + "="*60)
            print("🌦️  АНАЛИЗ СЕЗОННОСТИ")
            print("="*60)
            
            monthly_stats = self.df.groupby('month').agg({
                'shipment_id': 'count',
                'cost_rub': 'sum',
                'weight_kg': 'sum'
            })
            
            monthly_stats.columns = ['Кол-во_перевозок', 'Общая_стоимость', 'Общий_вес']
            
            print("\n📅 Статистика по месяцам:")
            print(monthly_stats)
            
            # Самый загруженный месяц
            busiest_month = monthly_stats['Кол-во_перевозок'].idxmax()
            print(f"\n📊 Самый загруженный месяц: {busiest_month}")
            print(f"   Перевозок: {monthly_stats.loc[busiest_month, 'Кол-во_перевозок']}")
    
    def generate_report(self, output_file=None):
        """Генерация полного отчета"""
        print("\n" + "="*60)
        print("📄 ГЕНЕРАЦИЯ ОТЧЕТА")
        print("="*60)
        
        self.basic_analysis()
        self.carrier_analysis()
        self.route_analysis()
        self.seasonal_analysis()
        
        # Сохранение отчета
        if output_file:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write("ОТЧЕТ ПО АНАЛИЗУ ЛОГИСТИЧЕСКИХ ДАННЫХ\n")
                f.write("="*60 + "\n\n")
                
                # Базовые показатели
                f.write("Базовые показатели:\n")
                f.write(f"  Всего перевозок: {len(self.df):,}\n")
                f.write(f"  Общая стоимость: {self.df['cost_rub'].sum():,.0f} руб\n")
                f.write(f"  Общий вес: {self.df['weight_kg'].sum():,.0f} кг\n\n")
                
                # Топ перевозчиков
                f.write("Топ-5 перевозчиков по количеству:\n")
                top_carriers = self.df['carrier'].value_counts().head(5)
                for carrier, count in top_carriers.items():
                    f.write(f"  {carrier}: {count} перевозок\n")
                
                # Топ маршрутов
                f.write("\nТоп-5 маршрутов:\n")
                top_routes = self.df.groupby(['from_city', 'to_city']).size().sort_values(ascending=False).head(5)
                for (from_city, to_city), count in top_routes.items():
                    f.write(f"  {from_city} → {to_city}: {count} перевозок\n")
            
            print(f"\n✅ Отчет сохранен в {output_file}")

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='Анализ расширенного датасета логистики')
    parser.add_argument('input', help='Входной CSV файл')
    parser.add_argument('-o', '--output', help='Выходной файл отчета')
    
    args = parser.parse_args()
    
    # Проверка файла
    if not Path(args.input).exists():
        print(f"❌ Файл {args.input} не найден")
        return
    
    # Запуск анализа
    analyzer = ExtendedLogisticsAnalyzer(args.input)
    analyzer.generate_report(args.output)

if __name__ == '__main__':
    main()
