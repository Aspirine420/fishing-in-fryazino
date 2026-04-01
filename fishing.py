import tkinter as tk
from tkinter import ttk, messagebox
import datetime
import calendar

# Словарь с периодами нереста рыб для Московской области
SPAWNING_PERIODS = {
    "Щука": {"start": (3, 15), "end": (4, 30)},      # 15 марта - 30 апреля
    "Окунь": {"start": (4, 1), "end": (5, 15)},      # 1 апреля - 15 мая
    "Плотва": {"start": (4, 15), "end": (5, 31)},    # 15 апреля - 31 мая
    "Лещ": {"start": (4, 20), "end": (6, 5)},        # 20 апреля - 5 июня
    "Судак": {"start": (4, 25), "end": (6, 10)},     # 25 апреля - 10 июня
    "Карась": {"start": (5, 1), "end": (6, 15)},     # 1 мая - 15 июня
    "Карп": {"start": (5, 15), "end": (6, 30)},      # 15 мая - 30 июня
    "Сом": {"start": (5, 20), "end": (7, 10)},       # 20 мая - 10 июля
    "Налим": {"start": (12, 1), "end": (1, 31)},     # 1 декабря - 31 января
    "Красноперка": {"start": (5, 1), "end": (6, 15)}, # 1 мая - 15 июня
    "Линь": {"start": (5, 15), "end": (6, 30)},      # 15 мая - 30 июня
    "Ротан": {"start": (4, 20), "end": (6, 10)},     # 20 апреля - 10 июня
    "Голавль": {"start": (4, 15), "end": (5, 31)},   # 15 апреля - 31 мая
    "Елец": {"start": (4, 1), "end": (5, 15)},       # 1 апреля - 15 мая
}

# Сезонные ограничения (запретные сроки)
SEASONAL_RESTRICTIONS = {
    "spring_ban": {"start": (4, 1), "end": (6, 10)},  # Весенний запрет с 1 апреля по 10 июня
}

# Рыбы, которые водятся во Фрязино и окрестностях
FISH_SPECIES = {
    "Щука": {"активность": "утро, вечер", "наживка": "живец, блесна, воблер", "места": "заросли, ямы, коряжник", "размер": "до 5-7 кг"},
    "Окунь": {"активность": "весь день", "наживка": "червь, мормышка, твистер", "места": "прибрежная зона, заросли", "размер": "до 300-400 гр"},
    "Плотва": {"активность": "утро, вечер", "наживка": "опарыш, хлеб, манка", "места": "тихие заводи, мелководье", "размер": "до 200-300 гр"},
    "Лещ": {"активность": "ночь, утро", "наживка": "опарыш, каша, червь", "места": "глубокие ямы, бровки", "размер": "до 1-2 кг"},
    "Карась": {"активность": "утро, вечер", "наживка": "червь, хлеб, опарыш", "места": "илистое дно, заросли", "размер": "до 500-800 гр"},
    "Карп": {"активность": "утро, вечер", "наживка": "кукуруза, бойлы, картофель", "места": "ямы, глубокие участки", "размер": "до 3-5 кг"},
    "Красноперка": {"активность": "день", "наживка": "опарыш, муха, стрекоза", "места": "заросли кувшинок, трава", "размер": "до 150-200 гр"},
    "Линь": {"активность": "ночь, утро", "наживка": "червь, опарыш", "места": "заросли, илистое дно", "размер": "до 400-600 гр"},
    "Ротан": {"активность": "весь день", "наживка": "червь, кусочек рыбы", "места": "заросли, мелководье", "размер": "до 100-150 гр"},
    "Верховка": {"активность": "день", "наживка": "муха, мотыль", "места": "поверхность воды", "размер": "до 10-15 гр"},
    "Пескарь": {"активность": "день", "наживка": "червь, опарыш", "места": "песчаное дно, перекаты", "размер": "до 50-80 гр"},
    "Голавль": {"активность": "утро, вечер", "наживка": "жук, кузнечик, опарыш", "места": "перекаты, стремнина", "размер": "до 1-2 кг"},
    "Елец": {"активность": "день", "наживка": "мотыль, опарыш, червь", "места": "быстрое течение, перекаты", "размер": "до 100-150 гр"},
}

# Информация о водоемах (актуальные для Фрязино)
WATER_BODIES = {
    "Барский пруд (Гребнево)": {
        "описание": "Живописный пруд на территории усадьбы Гребнево, популярное место рыбалки",
        "рыбы": ["Щука", "Окунь", "Плотва", "Карась", "Красноперка", "Линь", "Карп", "Ротан", "Верховка"],
        "особенности": "Глубины до 3-4 метров, есть заросли кувшинок, удобные подходы к воде, дно илистое с участками песка",
        "координаты": "55.9286° с.ш., 38.0784° в.д.",
        "доступ": "Свободный, с берега"
    },
    "Озеро за станцией Фрязино-Товарная": {
        "описание": "Большое озеро за железнодорожной станцией Фрязино-Товарная, популярное среди местных рыбаков",
        "рыбы": ["Щука", "Окунь", "Плотва", "Карась", "Красноперка", "Линь", "Ротан", "Верховка", "Карп"],
        "особенности": "Глубины до 2-4 метров, много водной растительности, есть заливные участки, дно преимущественно илистое",
        "координаты": "55.9547° с.ш., 38.0521° в.д.",
        "доступ": "Свободный, с берега, есть удобные подходы"
    },
    "Здеховский пруд (река Гречушка)": {
        "описание": "Живописный пруд с впадающей рекой Гречушкой, популярное место для рыбалки и отдыха",
        "рыбы": ["Щука", "Окунь", "Плотва", "Карась", "Красноперка", "Линь", "Ротан", "Лещ", "Голавль", "Елец", "Пескарь"],
        "особенности": "Пруд с медленным течением, глубины до 2-3 метров, есть заливные участки, впадающая река создает перепады глубин, донный рельеф разнообразный",
        "координаты": "55.9312° с.ш., 38.0956° в.д.",
        "доступ": "Свободный, с берега, есть удобные подходы"
    },
    "Река Любосеевка": {
        "описание": "Малая река, протекающая через Фрязино, приток реки Вори. Имеет очень слабое течение",
        "рыбы": ["Плотва", "Окунь", "Лещ", "Карась", "Пескарь", "Верховка", "Ротан", "Голавль", "Елец"],
        "особенности": "Течение очень слабое, местами практически стоячая вода, глубины 0.5-1.5 метра, много заросших участков, дно илистое",
        "координаты": "55.9569° с.ш., 38.0456° в.д.",
        "доступ": "Свободный, вдоль всего русла, есть места с удобными подходами"
    }
}

class FishingAdvisor:
    def __init__(self, root):
        self.root = root
        self.root.title("Рыболовный календарь - Фрязино")
        self.root.geometry("850x900")
        self.root.resizable(True, True)
        
        # Основной контейнер
        main_frame = ttk.Frame(root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Заголовок
        title_label = ttk.Label(main_frame, text="🐟 Рыболовный календарь Фрязино 🎣", 
                                font=("Arial", 18, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=10)
        
        location_label = ttk.Label(main_frame, text="Московская область, город Фрязино",
                                   font=("Arial", 11))
        location_label.grid(row=1, column=0, columnspan=2, pady=(0, 15))
        
        # Выбор водоема
        water_frame = ttk.LabelFrame(main_frame, text="🏞️ Выбор водоема", padding="10")
        water_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        ttk.Label(water_frame, text="Водоем:", font=("Arial", 10, "bold")).grid(row=0, column=0, padx=5, sticky=tk.W)
        self.water_var = tk.StringVar(value="Барский пруд (Гребнево)")
        self.water_combo = ttk.Combobox(water_frame, textvariable=self.water_var,
                                       values=list(WATER_BODIES.keys()),
                                       width=50, state="readonly", font=("Arial", 10))
        self.water_combo.grid(row=0, column=1, padx=5, sticky=(tk.W, tk.E))
        self.water_combo.bind('<<ComboboxSelected>>', self.on_water_change)
        
        # Информация о водоеме
        self.water_info_label = ttk.Label(water_frame, text="", foreground="gray", wraplength=700)
        self.water_info_label.grid(row=1, column=0, columnspan=2, pady=5, sticky=(tk.W, tk.E))
        
        # Полный список рыб в водоеме
        self.fish_list_label = ttk.Label(water_frame, text="", foreground="blue", wraplength=700)
        self.fish_list_label.grid(row=2, column=0, columnspan=2, pady=5, sticky=(tk.W, tk.E))
        
        # Выбор режима
        mode_frame = ttk.LabelFrame(main_frame, text="⏰ Выбор режима", padding="10")
        mode_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        self.mode_var = tk.StringVar(value="current")
        ttk.Radiobutton(mode_frame, text="Текущее время", variable=self.mode_var, 
                       value="current", command=self.on_mode_change).grid(row=0, column=0, padx=10)
        ttk.Radiobutton(mode_frame, text="Выбрать дату и время", variable=self.mode_var, 
                       value="custom", command=self.on_mode_change).grid(row=0, column=1, padx=10)
        
        # Блок для выбора даты (по умолчанию скрыт)
        self.custom_frame = ttk.LabelFrame(main_frame, text="📅 Выберите дату и время", padding="10")
        
        # Выбор даты
        date_frame = ttk.Frame(self.custom_frame)
        date_frame.grid(row=0, column=0, columnspan=3, pady=5)
        
        ttk.Label(date_frame, text="День:", font=("Arial", 10)).grid(row=0, column=0, padx=5)
        self.day_var = tk.StringVar()
        self.day_spinbox = ttk.Spinbox(date_frame, from_=1, to=31, width=5, 
                                       textvariable=self.day_var, font=("Arial", 10))
        self.day_spinbox.grid(row=0, column=1, padx=5)
        
        ttk.Label(date_frame, text="Месяц:", font=("Arial", 10)).grid(row=0, column=2, padx=5)
        self.month_var = tk.StringVar()
        self.month_spinbox = ttk.Spinbox(date_frame, from_=1, to=12, width=5,
                                         textvariable=self.month_var, font=("Arial", 10))
        self.month_spinbox.grid(row=0, column=3, padx=5)
        
        ttk.Label(date_frame, text="Год:", font=("Arial", 10)).grid(row=0, column=4, padx=5)
        self.year_var = tk.StringVar(value=str(datetime.datetime.now().year))
        self.year_spinbox = ttk.Spinbox(date_frame, from_=2024, to=2030, width=6,
                                        textvariable=self.year_var, font=("Arial", 10))
        self.year_spinbox.grid(row=0, column=5, padx=5)
        
        # Выбор времени
        time_frame = ttk.Frame(self.custom_frame)
        time_frame.grid(row=1, column=0, columnspan=3, pady=10)
        
        ttk.Label(time_frame, text="Время дня:", font=("Arial", 10, "bold")).grid(row=0, column=0, padx=5)
        self.time_var = tk.StringVar(value="утро")
        self.time_combo = ttk.Combobox(time_frame, textvariable=self.time_var,
                                       values=["утро (6-9)", "день (10-16)", "вечер (17-20)", "ночь (21-5)"],
                                       width=20, state="readonly", font=("Arial", 10))
        self.time_combo.grid(row=0, column=1, padx=5)
        
        # Кнопка анализа
        self.analyze_btn = ttk.Button(main_frame, text="🔍 Проверить возможность ловли", 
                                      command=self.analyze, width=30)
        self.analyze_btn.grid(row=4, column=0, columnspan=2, pady=20)
        
        # Результаты
        results_frame = ttk.LabelFrame(main_frame, text="📊 Результат проверки", padding="10")
        results_frame.grid(row=5, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)
        
        # Создаем текстовое поле с прокруткой
        text_frame = ttk.Frame(results_frame)
        text_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.result_text = tk.Text(text_frame, height=32, width=90, wrap=tk.WORD, 
                                   font=("Courier", 10))
        scrollbar = ttk.Scrollbar(text_frame, orient="vertical", command=self.result_text.yview)
        self.result_text.configure(yscrollcommand=scrollbar.set)
        
        self.result_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # Конфигурация веса для растягивания
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(5, weight=1)
        results_frame.columnconfigure(0, weight=1)
        results_frame.rowconfigure(0, weight=1)
        text_frame.columnconfigure(0, weight=1)
        text_frame.rowconfigure(0, weight=1)
        water_frame.columnconfigure(1, weight=1)
        
        # Инициализация значений по умолчанию
        current = datetime.datetime.now()
        self.day_var.set(str(current.day))
        self.month_var.set(str(current.month))
        self.on_mode_change()
        self.on_water_change()
        
    def on_mode_change(self):
        """Обработка изменения режима"""
        if self.mode_var.get() == "custom":
            self.custom_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        else:
            self.custom_frame.grid_forget()
    
    def on_water_change(self, event=None):
        """Обработка изменения водоема - выводит полный список рыб"""
        water = self.water_var.get()
        if water in WATER_BODIES:
            info = WATER_BODIES[water]
            # Полный список рыб без сокращений
            fish_list_full = ', '.join(info['рыбы'])
            self.water_info_label.config(text=f"📍 {info['описание']}")
            self.fish_list_label.config(text=f"🐟 Обитающие виды рыб ({len(info['рыбы'])}): {fish_list_full}")
    
    def is_in_spawning_period(self, date, species):
        """Проверка, находится ли рыба в период нереста"""
        if species not in SPAWNING_PERIODS:
            return False
        
        period = SPAWNING_PERIODS[species]
        period_start = period["start"]
        period_end = period["end"]
        
        # Обработка периода, переходящего через новый год (налим)
        if period_start[0] > period_end[0]:
            if date.month >= period_start[0] or date.month <= period_end[0]:
                if date.month == period_start[0] and date.day < period_start[1]:
                    return False
                if date.month == period_end[0] and date.day > period_end[1]:
                    return False
                return True
        else:
            if period_start[0] <= date.month <= period_end[0]:
                if date.month == period_start[0] and date.day < period_start[1]:
                    return False
                if date.month == period_end[0] and date.day > period_end[1]:
                    return False
                return True
        return False
    
    def is_fishing_allowed(self, date):
        """Проверка, разрешена ли ловля в данный период"""
        # Весенний запрет
        spring_ban = SEASONAL_RESTRICTIONS["spring_ban"]
        if spring_ban["start"][0] <= date.month <= spring_ban["end"][0]:
            if date.month == spring_ban["start"][0] and date.day < spring_ban["start"][1]:
                return True
            if date.month == spring_ban["end"][0] and date.day > spring_ban["end"][1]:
                return True
            if spring_ban["start"][0] < date.month < spring_ban["end"][0]:
                return False
            if date.month == spring_ban["start"][0] and date.day >= spring_ban["start"][1]:
                return False
            if date.month == spring_ban["end"][0] and date.day <= spring_ban["end"][1]:
                return False
        return True
    
    def get_time_of_day(self, time_str):
        """Определение времени суток по строке"""
        time_map = {
            "утро (6-9)": "утро",
            "день (10-16)": "день",
            "вечер (17-20)": "вечер",
            "ночь (21-5)": "ночь"
        }
        return time_map.get(time_str, time_str)
    
    def get_fish_for_time(self, time_of_day, water_body):
        """Получить рыбу, активную в данное время суток и обитающую в выбранном водоеме"""
        if water_body in WATER_BODIES:
            water_fish = set(WATER_BODIES[water_body]["рыбы"])
        else:
            water_fish = set(FISH_SPECIES.keys())
        
        active_fish = []
        for fish in water_fish:
            if fish in FISH_SPECIES and time_of_day in FISH_SPECIES[fish]["активность"]:
                active_fish.append(fish)
        return active_fish
    
    def get_season_advice(self, date):
        """Получить сезонные рекомендации"""
        month = date.month
        if month in [12, 1, 2]:
            return "❄️ Зимний сезон: Используйте зимние снасти, ищите рыбу на глубине, мормышка с мотылем - отличный выбор"
        elif month in [3, 4, 5]:
            return "🌸 Весенний сезон: Рыба активна после нереста, хорошо работает червь и опарыш, рыба подходит к берегу"
        elif month in [6, 7, 8]:
            return "☀️ Летний сезон: Рыба уходит на глубину в жару, эффективна ловля ранним утром и вечером, используйте растительные насадки"
        else:
            return "🍂 Осенний сезон: Рыба нагуливает жир перед зимой, активный жор, хорошо работают животные насадки"
    
    def analyze(self):
        """Основная функция анализа"""
        # Определение даты и времени
        if self.mode_var.get() == "current":
            current_time = datetime.datetime.now()
            date = current_time.date()
            hour = current_time.hour
            
            # Определение времени суток
            if 6 <= hour <= 9:
                time_of_day = "утро"
            elif 10 <= hour <= 16:
                time_of_day = "день"
            elif 17 <= hour <= 20:
                time_of_day = "вечер"
            else:
                time_of_day = "ночь"
        else:
            # Сбор пользовательских данных
            try:
                day = int(self.day_var.get())
                month = int(self.month_var.get())
                year = int(self.year_var.get())
                
                # Проверка корректности даты
                if month < 1 or month > 12 or day < 1 or day > calendar.monthrange(year, month)[1]:
                    messagebox.showerror("Ошибка", "Некорректная дата!")
                    return
                
                date = datetime.date(year, month, day)
                time_of_day = self.get_time_of_day(self.time_var.get())
            except ValueError:
                messagebox.showerror("Ошибка", "Пожалуйста, введите корректные значения!")
                return
        
        water_body = self.water_var.get()
        
        # Очистка текстового поля
        self.result_text.delete(1.0, tk.END)
        
        # Заголовок
        self.result_text.insert(tk.END, "="*80 + "\n")
        self.result_text.insert(tk.END, f"🐟 РЫБОЛОВНЫЙ ПРОГНОЗ - Г. ФРЯЗИНО\n")
        self.result_text.insert(tk.END, "="*80 + "\n\n")
        
        self.result_text.insert(tk.END, f"📅 Дата: {date.strftime('%d.%m.%Y')} ({self.get_weekday_name(date)})\n")
        self.result_text.insert(tk.END, f"⏰ Время суток: {time_of_day.upper()}\n")
        self.result_text.insert(tk.END, f"📍 Город: Фрязино, Московская область\n")
        self.result_text.insert(tk.END, f"💧 Водоем: {water_body}\n")
        
        if water_body in WATER_BODIES:
            self.result_text.insert(tk.END, f"   {WATER_BODIES[water_body]['описание']}\n")
            # Выводим полный список рыб водоема
            fish_list = ', '.join(WATER_BODIES[water_body]['рыбы'])
            self.result_text.insert(tk.END, f"   🐟 Всего видов: {len(WATER_BODIES[water_body]['рыбы'])} - {fish_list}\n")
        
        self.result_text.insert(tk.END, "\n" + "-"*80 + "\n\n")
        
        # Сезонные рекомендации
        self.result_text.insert(tk.END, f"🍂 Сезонная рекомендация:\n")
        self.result_text.insert(tk.END, f"   {self.get_season_advice(date)}\n\n")
        
        # Проверка сезонных ограничений
        fishing_allowed = self.is_fishing_allowed(date)
        
        if not fishing_allowed:
            self.result_text.insert(tk.END, "⚠️⚠️⚠️ ВНИМАНИЕ ⚠️⚠️⚠️\n")
            self.result_text.insert(tk.END, f"С {SEASONAL_RESTRICTIONS['spring_ban']['start'][1]}.{SEASONAL_RESTRICTIONS['spring_ban']['start'][0]} "
                                            f"по {SEASONAL_RESTRICTIONS['spring_ban']['end'][1]}.{SEASONAL_RESTRICTIONS['spring_ban']['end'][0]} "
                                            f"действует ВЕСЕННИЙ ЗАПРЕТ на ловлю рыбы!\n")
            self.result_text.insert(tk.END, "Разрешена только рыбалка с берега одной поплавочной удочкой (до 2 крючков) вне мест нереста.\n")
            self.result_text.insert(tk.END, "Штраф за нарушение: от 2000 до 5000 рублей.\n\n")
        else:
            self.result_text.insert(tk.END, "✅ Сезонные ограничения не нарушены. Рыбалка разрешена.\n\n")
        
        # Получение рыбы для данного времени суток и водоема
        time_active_fish = self.get_fish_for_time(time_of_day, water_body)
        
        # Проверка нереста и формирование списка разрешенной рыбы
        allowed_fish = []
        spawning_fish = []
        
        for fish in time_active_fish:
            if self.is_in_spawning_period(date, fish):
                spawning_fish.append(fish)
            else:
                allowed_fish.append(fish)
        
        # Отображение результатов
        self.result_text.insert(tk.END, "🐟 РЕКОМЕНДАЦИИ ПО ЛОВЛЕ:\n")
        self.result_text.insert(tk.END, "-"*80 + "\n")
        
        if allowed_fish:
            self.result_text.insert(tk.END, f"\n🎯 Целевые виды рыб ({len(allowed_fish)}):\n\n")
            for fish in allowed_fish:
                info = FISH_SPECIES[fish]
                self.result_text.insert(tk.END, f"   🎣 {fish}:\n")
                self.result_text.insert(tk.END, f"      • Наживка: {info['наживка']}\n")
                self.result_text.insert(tk.END, f"      • Места: {info['места']}\n")
                self.result_text.insert(tk.END, f"      • Размер: {info['размер']}\n")
                self.result_text.insert(tk.END, f"      • Активность: {info['активность']}\n\n")
        else:
            self.result_text.insert(tk.END, "⚠️ К сожалению, в это время активной рыбы нет.\n")
            self.result_text.insert(tk.END, "Совет: попробуйте другое время суток или используйте пассивные снасти (донки, фидер).\n\n")
        
        if spawning_fish:
            self.result_text.insert(tk.END, "❌ ЗАПРЕЩЕНЫ К ВЫЛОВУ (период нереста):\n")
            for fish in spawning_fish:
                period = SPAWNING_PERIODS[fish]
                self.result_text.insert(tk.END, f"   • {fish} (нерестится с {period['start'][1]}.{period['start'][0]} "
                                               f"по {period['end'][1]}.{period['end'][0]})\n")
            self.result_text.insert(tk.END, f"\n❗ Ловля этих видов в период нереста карается штрафом до 5000 руб!\n\n")
        
        # Информация о водоеме
        if water_body in WATER_BODIES:
            self.result_text.insert(tk.END, "-"*80 + "\n")
            self.result_text.insert(tk.END, f"ℹ️ ПОДРОБНЕЕ О ВОДОЕМЕ:\n")
            self.result_text.insert(tk.END, f"   • {WATER_BODIES[water_body]['особенности']}\n")
            self.result_text.insert(tk.END, f"   • Доступ: {WATER_BODIES[water_body]['доступ']}\n")
            if 'координаты' in WATER_BODIES[water_body]:
                self.result_text.insert(tk.END, f"   • Координаты: {WATER_BODIES[water_body]['координаты']}\n")
        
        # Правила рыболовства
        self.result_text.insert(tk.END, "\n" + "="*80 + "\n")
        self.result_text.insert(tk.END, "📜 ПРАВИЛА РЫБОЛОВСТВА В МОСКОВСКОЙ ОБЛАСТИ:\n")
        self.result_text.insert(tk.END, "• Суточная норма вылова: 5 кг (одна особь свыше нормы, но не более 2 шт)\n")
        self.result_text.insert(tk.END, "• Минимальный размер вылавливаемой рыбы:\n")
        self.result_text.insert(tk.END, "  - Щука: 32 см, Судак: 40 см, Лещ: 25 см, Сом: 90 см\n")
        self.result_text.insert(tk.END, "  - Сазан/Карп: 35 см, Жерех: 35 см, Голавль: 20 см\n")
        self.result_text.insert(tk.END, "• Запрещенные снасти: сети, электроудочки, колющие орудия\n")
        self.result_text.insert(tk.END, "• Количество крючков: не более 5 на человека\n")
        self.result_text.insert(tk.END, "\n🎣 Удачной рыбалки и соблюдайте правила!\n")
    
    def get_weekday_name(self, date):
        """Получить название дня недели"""
        weekdays = ['понедельник', 'вторник', 'среда', 'четверг', 'пятница', 'суббота', 'воскресенье']
        return weekdays[date.weekday()]

def main():
    root = tk.Tk()
    app = FishingAdvisor(root)
    root.mainloop()

if __name__ == "__main__":
    main()