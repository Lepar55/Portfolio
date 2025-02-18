import os
from sqlalchemy import create_engine, Column, Integer, String, Date, Numeric
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Вкажіть шлях до вашої папки, де ви хочете зберігати базу даних
folder_path = r"G:/all/programs/univer/web/instance"  # Вказати шлях до потрібної папки
database_path = os.path.join(folder_path, 'database.db')  # Шлях до файлу бази даних

# Перевірка, чи існує папка, якщо ні, то створюємо її
if not os.path.exists(folder_path):
    os.makedirs(folder_path)

# Підключення до SQLite бази даних в зазначеній папці
DATABASE_URI = f'sqlite:///{database_path}'  # Підключення до SQLite бази даних у вашій папці
engine = create_engine(DATABASE_URI, echo=True)

# Створення бази даних та таблиці
Base = declarative_base()

class Kit(Base):
    __tablename__ = 'kits'

    id = Column(Integer, primary_key=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    fathers_name = Column(String(100))
    birth_date = Column(Date)
    depart = Column(String(100), nullable=False)
    position = Column(String(100), nullable=False)
    rate = Column(Numeric(3, 2))
    rtck = Column(String(100))
    main_parttime = Column(String(100))

# Створення таблиць у базі даних
Base.metadata.create_all(engine)

# Створення сесії для роботи з даними
Session = sessionmaker(bind=engine)
session = Session()

# Вставка даних
new_kit = Kit(
    first_name='Іван',
    last_name='Петренко',
    fathers_name='Олегович',
    birth_date='1999-09-26',
    depart='КІТ',
    position='Фахівець відділу КІТ',
    rate=4891.51,
    rtck='Львівський ОРТЦК та СП',
    main_parttime='Основна'
)

session.add(new_kit)


# Перевірка даних
kits = session.query(Kit).all()
for kit in kits:
    print(f"{kit.id}: {kit.first_name} {kit.last_name}, {kit.position}")

# Закриття сесії
session.close()
