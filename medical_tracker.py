# dog_medical_tracker.py - С транспонированной таблицей
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
import os

plt.rcParams['font.family'] = 'DejaVu Sans'

class DogMedicalTracker:
    def __init__(self, data_file='dog_medical_data.xlsx'):
        self.data_file = data_file
        
        # Референсные значения для СОБАК с учетом ХБП 3 стадии
        self.reference_ranges = {
            # 🩺 КРОВЬ - основные показатели
            'WBC': (6.0, 17.0),           # Лейкоциты
            'RBC': (5.5, 8.5),            # Эритроциты  
            'Hb': (120, 180),             # Гемоглобин
            'HCT': (37, 55),              # Гематокрит
            'PLT': (200, 500),            # Тромбоциты
            
            # 🧪 БИОХИМИЯ - почечные показатели (ключевые для ХБП)
            'Urea': (3.5, 10.0),          # Мочевина
            'Creatinine_blood': (60, 140), # Креатинин крови
            'SDMA': (0, 14),              # SDMA
            'Phosphorus': (0.8, 2.0),     # Фосфор
            
            # 🧪 ЭЛЕКТРОЛИТЫ
            'Potassium': (3.5, 5.5),      # Калий
            'Sodium': (140, 155),         # Натрий
            'Chloride': (105, 120),       # Хлориды
            'iCalcium': (1.1, 1.4),       # Ионизированный кальций
            
            # 🧪 ПЕЧЕНЬ/ПОДЖЕЛУДОЧНАЯ
            'ALT': (10, 125),             # АЛТ
            'Lipase': (0, 250),           # Панкреатическая липаза
            'Amylase': (300, 2000),       # Амилаза
            'Albumin': (25, 40),          # Альбумин
            'Total_protein': (55, 75),    # Общий белок
            
            # ❤️ СЕРДЕЧНЫЕ МАРКЕРЫ
            'Troponin': (0, 0.2),         # Тропонин
            
            # 💧 МОЧА - ключевые при ХБП
            'USG': (1.015, 1.045),        # Удельный вес мочи
            'Protein_urine': (0, 30),     # Белок в моче - мг/дл
            'Creatinine_urine': (50, 250), # Креатинин мочи - мг/дл
            'UPC_ratio': (0.0, 0.5),      # Соотношение белок/креатинин
            'Leukocytes_urine': (0, 5),   # Лейкоциты в моче
            'Glucose_urine': (0, 0),      # Глюкоза в моче
            'Casts': (0, 0),              # Цилиндры
        }
        
        self.upc_classification = {
            'норма': (0.0, 0.5),
            'пограничная': (0.5, 1.0),
            'proteinuria': (1.0, 2.0),
            'тяжелая proteinuria': (2.0, float('inf'))
        }
        
        self.load_data()
    
    def load_data(self):
        if os.path.exists(self.data_file):
            self.df = pd.read_excel(self.data_file)
            self.df['date'] = pd.to_datetime(self.df['date'])
            print("✅ Данные загружены из файла")
            print(f"📊 Записей в базе: {len(self.df)}")
        else:
            columns = ['date'] + list(self.reference_ranges.keys())
            self.df = pd.DataFrame(columns=columns)
            print("📁 Создан новый файл для данных собаки")
    
    def save_data(self):
        self.df.to_excel(self.data_file, index=False)
        print("💾 Данные сохранены")
    
    def input_float(self, prompt):
        try:
            value = input(prompt)
            return float(value) if value else np.nan
        except ValueError:
            return np.nan
    
    def calculate_upc_ratio(self, protein_mgDL, creatinine_mgDL):
        """Расчет UPC соотношения в мг/дл"""
        if pd.isna(protein_mgDL) or pd.isna(creatinine_mgDL) or creatinine_mgDL == 0:
            return np.nan
        return protein_mgDL / creatinine_mgDL
    
    def add_measurement(self):
        print("\n🐕 ДОБАВЛЕНИЕ ПОКАЗАТЕЛЕЙ СОБАКИ")
        print("=" * 50)
        
        new_data = {'date': input("Дата измерения (ГГГГ-ММ-ДД): ")}
        
        print("\n🩺 ОБЩИЙ АНАЛИЗ КРОВИ:")
        new_data['WBC'] = self.input_float("Лейкоциты (WBC, ×10⁹/л): ")
        new_data['RBC'] = self.input_float("Эритроциты (RBC, ×10¹²/л): ")
        new_data['Hb'] = self.input_float("Гемоглобин (Hb, г/л): ")
        new_data['HCT'] = self.input_float("Гематокрит (HCT, %): ")
        new_data['PLT'] = self.input_float("Тромбоциты (PLT, ×10⁹/л): ")
        
        print("\n🧪 БИОХИМИЯ - ПОЧЕЧНЫЕ ПОКАЗАТЕЛИ (ХБП):")
        new_data['Urea'] = self.input_float("Мочевина (Urea, ммоль/л): ")
        new_data['Creatinine_blood'] = self.input_float("Креатинин КРОВИ (Creatinine, мкмоль/л): ")
        new_data['SDMA'] = self.input_float("SDMA (мкг/дл): ")
        new_data['Phosphorus'] = self.input_float("Фосфор (Phosphorus, ммоль/л): ")
        
        print("\n🧪 ЭЛЕКТРОЛИТЫ:")
        new_data['Potassium'] = self.input_float("Калий (K+, ммоль/л): ")
        new_data['Sodium'] = self.input_float("Натрий (Na+, ммоль/л): ")
        new_data['Chloride'] = self.input_float("Хлориды (Cl-, ммоль/л): ")
        new_data['iCalcium'] = self.input_float("Ионизированный кальций (iCa, ммоль/л): ")
        
        print("\n🧪 ПЕЧЕНЬ И ПОДЖЕЛУДОЧНАЯ:")
        new_data['ALT'] = self.input_float("АЛТ (ALT, Ед/л): ")
        new_data['Lipase'] = self.input_float("Панкреатическая липаза (Lipase, Ед/л): ")
        new_data['Amylase'] = self.input_float("Амилаза (Amylase, Ед/л): ")
        new_data['Albumin'] = self.input_float("Альбумин (Albumin, г/л): ")
        new_data['Total_protein'] = self.input_float("Общий белок (Total Protein, г/л): ")
        
        print("\n❤️ СЕРДЕЧНЫЕ МАРКЕРЫ:")
        new_data['Troponin'] = self.input_float("Тропонин (Troponin, нг/мл): ")
        
        print("\n💧 АНАЛИЗ МОЧИ:")
        new_data['USG'] = self.input_float("Удельный вес мочи (USG): ")
        new_data['Protein_urine'] = self.input_float("Белок в моче (мг/дл): ")
        new_data['Creatinine_urine'] = self.input_float("Креатинин МОЧИ (мг/дл): ")
        
        # АВТОМАТИЧЕСКИЙ РАСЧЕТ UPC
        new_data['UPC_ratio'] = self.calculate_upc_ratio(
            new_data['Protein_urine'], 
            new_data['Creatinine_urine']
        )
        
        print(f"📊 Автоматически рассчитано UPC: {new_data['UPC_ratio']:.2f}")
        
        new_data['Leukocytes_urine'] = self.input_float("Лейкоциты в моче (в поле зрения): ")
        new_data['Glucose_urine'] = self.input_float("Глюкоза в моче: ")
        new_data['Casts'] = self.input_float("Цилиндры (в поле зрения): ")
        
        # Добавляем в DataFrame
        self.df = pd.concat([self.df, pd.DataFrame([new_data])], ignore_index=True)
        self.df['date'] = pd.to_datetime(self.df['date'])
        self.df = self.df.sort_values('date')
        self.save_data()
        print("✅ Показатели успешно добавлены!")
    
    def get_units(self, metric):
        units = {
            'WBC': '×10⁹/л', 'RBC': '×10¹²/л', 'Hb': 'г/л', 'HCT': '%', 'PLT': '×10⁹/л',
            'Urea': 'ммоль/л', 'Creatinine_blood': 'мкмоль/л', 'SDMA': 'мкг/дл', 'Phosphorus': 'ммоль/л',
            'Potassium': 'ммоль/л', 'Sodium': 'ммоль/л', 'Chloride': 'ммоль/л', 'iCalcium': 'ммоль/л',
            'ALT': 'Ед/л', 'Lipase': 'Ед/л', 'Amylase': 'Ед/л', 'Albumin': 'г/л', 'Total_protein': 'г/л',
            'Troponin': 'нг/мл', 'USG': '', 
            'Protein_urine': 'мг/дл',
            'Creatinine_urine': 'мг/дл',
            'UPC_ratio': 'UPC', 
            'Leukocytes_urine': 'в п/з', 'Glucose_urine': '', 'Casts': 'в п/з'
        }
        return units.get(metric, '')
    
    def get_metric_name(self, metric):
        """Получить читаемое название показателя"""
        names = {
            'WBC': 'Лейкоциты', 'RBC': 'Эритроциты', 'Hb': 'Гемоглобин', 
            'HCT': 'Гематокрит', 'PLT': 'Тромбоциты', 'Urea': 'Мочевина',
            'Creatinine_blood': 'Креатинин крови', 'SDMA': 'SDMA', 
            'Phosphorus': 'Фосфор', 'Potassium': 'Калий', 'Sodium': 'Натрий',
            'Chloride': 'Хлориды', 'iCalcium': 'Ионизир. кальций', 'ALT': 'АЛТ',
            'Lipase': 'Панкреат. липаза', 'Amylase': 'Амилаза', 'Albumin': 'Альбумин',
            'Total_protein': 'Общий белок', 'Troponin': 'Тропонин', 'USG': 'Уд. вес мочи',
            'Protein_urine': 'Белок мочи', 'Creatinine_urine': 'Креатинин мочи',
            'UPC_ratio': 'Соотн. Б/К (UPC)', 'Leukocytes_urine': 'Лейкоциты мочи',
            'Glucose_urine': 'Глюкоза мочи', 'Casts': 'Цилиндры'
        }
        return names.get(metric, metric)
    
    def show_transposed_table(self):
        """Показать таблицу: показатели → строки, даты → столбцы"""
        if len(self.df) == 0:
            print("📭 Нет данных для отображения")
            return
        
        print("\n📊 ТАБЛИЦА ПОКАЗАТЕЛЕЙ (по датам)")
        print("=" * 100)
        
        # Создаем транспонированную таблицу
        transposed_df = self.df.set_index('date').T
        
        # Форматируем даты в названиях столбцов
        transposed_df.columns = [col.strftime('%d.%m.%Y') for col in transposed_df.columns]
        
        # Добавляем единицы измерения к названиям строк
        transposed_df.index = [f"{self.get_metric_name(idx)} ({self.get_units(idx)})" 
                             for idx in transposed_df.index]
        
        # Округляем значения
        transposed_df = transposed_df.round(3)
        
        # Заменяем NaN на прочерки
        transposed_df = transposed_df.fillna('-')
        
        # Выводим таблицу
        pd.set_option('display.max_rows', None)
        pd.set_option('display.width', 1000)
        
        print(transposed_df)
        
        print(f"\n📈 Всего измерений: {len(self.df)}")
        print(f"📅 Период: {self.df['date'].min().strftime('%d.%m.%Y')} - {self.df['date'].max().strftime('%d.%m.%Y')}")
    
    def show_key_metrics_table(self):
        """Показать таблицу только ключевых показателей"""
        if len(self.df) == 0:
            print("📭 Нет данных для отображения")
            return
        
        print("\n🎯 КЛЮЧЕВЫЕ ПОКАЗАТЕЛИ ХБП И ПАНКРЕАТИТА")
        print("=" * 100)
        
        # Ключевые показатели для мониторинга
        key_metrics = [
            'Creatinine_blood', 'Urea', 'Phosphorus', 'SDMA',  # Почки
            'Protein_urine', 'UPC_ratio', 'Creatinine_urine', 'USG',  # Моча
            'Lipase', 'ALT', 'Albumin',  # Поджелудочная/печень
            'Potassium', 'iCalcium'  # Электролиты
        ]
        
        # Фильтруем только существующие показатели
        existing_metrics = [m for m in key_metrics if m in self.df.columns]
        
        if not existing_metrics:
            print("❌ Нет данных по ключевым показателям")
            return
        
        # Создаем таблицу только с ключевыми показателями
        key_df = self.df[['date'] + existing_metrics].set_index('date').T
        
        # Форматируем даты
        key_df.columns = [col.strftime('%d.%m.%Y') for col in key_df.columns]
        
        # Добавляем названия и единицы измерений
        key_df.index = [f"{self.get_metric_name(idx)} ({self.get_units(idx)})" 
                       for idx in key_df.index]
        
        # Округляем и заменяем NaN
        key_df = key_df.round(3).fillna('-')
        
        # Выводим таблицу
        pd.set_option('display.max_rows', None)
        print(key_df)
    
    def plot_proteinuria_dashboard(self):
        """Дашборд для мониторинга proteinuria"""
        if len(self.df) < 1:
            print("❌ Нет данных для построения графиков")
            return
        
        fig, axes = plt.subplots(2, 2, figsize=(15, 10))
        
        # 1. Соотношение UPC
        if 'UPC_ratio' in self.df.columns:
            ax = axes[0, 0]
            upc_values = self.df['UPC_ratio'].dropna()
            if len(upc_values) > 0:
                ax.plot(self.df['date'], self.df['UPC_ratio'], 
                       marker='o', linewidth=3, color='red', label='UPC')
                
                # Зоны UPC
                ax.axhspan(0, 0.5, alpha=0.3, color='green', label='Норма (0-0.5)')
                ax.axhspan(0.5, 1.0, alpha=0.3, color='yellow', label='Пограничная (0.5-1.0)')
                ax.axhspan(1.0, 2.0, alpha=0.3, color='orange', label='Proteinuria (1.0-2.0)')
                ax.axhspan(2.0, max(upc_values.max()*1.1, 3.0), alpha=0.3, color='red', label='Тяжелая (>2.0)')
                
                ax.set_title('📊 Соотношение БЕЛОК/КРЕАТИНИН (UPC)')
                ax.set_ylabel('UPC ratio')
                ax.legend()
                ax.grid(True, alpha=0.3)
                ax.tick_params(axis='x', rotation=45)
        
        # 2. Белок мочи в мг/дл
        if 'Protein_urine' in self.df.columns:
            ax = axes[0, 1]
            protein_values = self.df['Protein_urine'].dropna()
            if len(protein_values) > 0:
                ax.plot(self.df['date'], self.df['Protein_urine'], 
                       marker='D', linewidth=2, color='purple', label='Белок мочи')
                ax.axhspan(0, 30, alpha=0.3, color='green', label='Норма (0-30 мг/дл)')
                ax.set_title('💧 Белок в моче')
                ax.set_ylabel('мг/дл')
                ax.legend()
                ax.grid(True, alpha=0.3)
                ax.tick_params(axis='x', rotation=45)
        
        # 3. Креатинин мочи в мг/дл
        if 'Creatinine_urine' in self.df.columns:
            ax = axes[1, 0]
            creat_values = self.df['Creatinine_urine'].dropna()
            if len(creat_values) > 0:
                ax.plot(self.df['date'], self.df['Creatinine_urine'], 
                       marker='^', linewidth=2, color='green', label='Креатинин мочи')
                ax.axhspan(50, 250, alpha=0.3, color='green', label='Норма (50-250 мг/дл)')
                ax.set_title('💧 Креатинин мочи')
                ax.set_ylabel('мг/дл')
                ax.legend()
                ax.grid(True, alpha=0.3)
                ax.tick_params(axis='x', rotation=45)
        
        # 4. Удельный вес мочи
        if 'USG' in self.df.columns:
            ax = axes[1, 1]
            ax.plot(self.df['date'], self.df['USG'], 
                   marker='v', linewidth=2, color='brown', label='Удельный вес')
            ax.axhspan(1.015, 1.045, alpha=0.3, color='green', label='Норма (1.015-1.045)')
            ax.set_title('💧 Удельный вес мочи (USG)')
            ax.set_ylabel('USG')
            ax.legend()
            ax.grid(True, alpha=0.3)
            ax.tick_params(axis='x', rotation=45)
        
        plt.suptitle('🐕 МОНИТОРИНГ ПОЧЕЧНОЙ ФУНКЦИИ', fontsize=16)
        plt.tight_layout()
        plt.show()

    def show_proteinuria_analysis(self):
        """Детальный анализ proteinuria"""
        if len(self.df) == 0:
            print("❌ Нет данных для анализа")
            return
        
        latest = self.df.iloc[-1]
        
        print("\n🔍 ДЕТАЛЬНЫЙ АНАЛИЗ PROTEINURIA")
        print("=" * 60)
        
        if 'UPC_ratio' in latest and not pd.isna(latest['UPC_ratio']):
            upc = latest['UPC_ratio']
            
            if upc < 0.5:
                stage = "НОРМА"
                recommendation = "✅ Отличный показатель!"
            elif upc < 1.0:
                stage = "ПОГРАНИЧНАЯ"
                recommendation = "⚠️ Требуется наблюдение, возможно назначение ИАПФ"
            elif upc < 2.0:
                stage = "PROTEINURIA" 
                recommendation = "🚨 Рекомендованы ИАПФ, контроль каждые 2-4 недели"
            else:
                stage = "ТЯЖЕЛАЯ PROTEINURIA"
                recommendation = "🚨 СРОЧНАЯ КОНСУЛЬТАЦИЯ ВЕТЕРИНАРА!"
            
            print(f"📊 Соотношение БЕЛОК/КРЕАТИНИН (UPC): {upc:.2f}")
            print(f"🎯 Стадия: {stage}")
            print(f"💡 Рекомендация: {recommendation}")
            print()
        
        # Дополнительная информация
        urine_metrics = ['Protein_urine', 'Creatinine_urine', 'USG']
        for metric in urine_metrics:
            if metric in latest and not pd.isna(latest[metric]):
                value = latest[metric]
                low, high = self.reference_ranges[metric]
                status = "✅ В норме" if low <= value <= high else "❌ Отклонение"
                print(f"{metric}: {value:.1f} {self.get_units(metric)} (норма: {low}-{high}) - {status}")

    def show_ckd_analysis(self):
        """Специальный анализ для ХБП 3 стадии"""
        if len(self.df) == 0:
            print("❌ Нет данных для анализа")
            return
        
        latest = self.df.iloc[-1]
        
        print("\n🔍 АНАЛИЗ ХБП 3 СТАДИИ")
        print("=" * 60)
        
        ckd_metrics = {
            'Creatinine_blood': (180, 440),
            'Urea': (10, 25),
            'Phosphorus': (1.6, 3.0),
            'SDMA': (18, 35)
        }
        
        for metric, (stage_min, stage_max) in ckd_metrics.items():
            if metric in latest and not pd.isna(latest[metric]):
                value = latest[metric]
                
                if value < stage_min:
                    status = "⬇️  Ниже диапазона 3 стадии"
                elif value <= stage_max:
                    status = "🎯 В диапазоне 3 стадии"
                else:
                    status = "⬆️  Выше диапазона 3 стадии"
                
                print(f"{metric}: {value:.1f} {self.get_units(metric)} - {status}")

    def show_all_data(self):
        """Показать все данные в разных форматах"""
        if len(self.df) == 0:
            print("📭 Нет данных")
            return
        
        print("\n📋 ВЫБЕРИТЕ ФОРМАТ ОТОБРАЖЕНИЯ:")
        print("1. 📊 Обычная таблица (даты → строки)")
        print("2. 🔄 Транспонированная таблица (показатели → строки)")
        print("3. 🎯 Только ключевые показатели")
        
        choice = input("\nВаш выбор (1-3): ")
        
        if choice == '1':
            print("\n📊 ОБЫЧНАЯ ТАБЛИЦА (даты → строки):")
            print("=" * 80)
            pd.set_option('display.max_columns', None)
            pd.set_option('display.width', 1000)
            display_df = self.df.copy()
            display_df['date'] = display_df['date'].dt.strftime('%Y-%m-%d')
            numeric_columns = display_df.select_dtypes(include=[np.number]).columns
            display_df[numeric_columns] = display_df[numeric_columns].round(3)
            print(display_df)
            
        elif choice == '2':
            self.show_transposed_table()
            
        elif choice == '3':
            self.show_key_metrics_table()
            
        else:
            print("❌ Неверный выбор")

    def show_main_menu(self):
        """Главное меню системы"""
        while True:
            print("\n" + "="*60)
            print("🐕 СИСТЕМА МОНИТОРИНГА СОБАКИ: ХБП 3 СТАДИИ + ПАНКРЕАТИТ")
            print("="*60)
            print("1. 📊 Добавить новые показатели")
            print("2. 📈 Дашборд PROTEINURIA (графики)")
            print("3. 🔍 Анализ ХБП 3 стадии") 
            print("4. 📋 Анализ PROTEINURIA")
            print("5. 📄 Показать все данные (таблицы)")
            print("6. 🚪 Выход")
            
            choice = input("\nВаш выбор (1-6): ")
            
            if choice == '1':
                self.add_measurement()
            elif choice == '2':
                self.plot_proteinuria_dashboard()
            elif choice == '3':
                self.show_ckd_analysis()
            elif choice == '4':
                self.show_proteinuria_analysis()
            elif choice == '5':
                self.show_all_data()
            elif choice == '6':
                print("💝 Забота о питомце - это важно! Данные сохранены.")
                break
            else:
                print("❌ Неверный выбор. Попробуйте снова.")

# Запуск системы
if __name__ == "__main__":
    print("🐕 Запуск системы мониторинга для собаки с ХБП и панкреатитом...")
    tracker = DogMedicalTracker()
    tracker.show_main_menu()