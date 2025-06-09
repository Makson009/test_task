import argparse
import json
from collections import defaultdict
from typing import List, Dict, Any


# --- Ваши существующие функции parse_csv_line, parse_rate, read_employees остаются без изменений ---

def parse_csv_line(line: str) -> List[str]:
    """Разделяет строку CSV на список значений."""
    return line.strip().split(',')


def parse_rate(data: Dict[str, str]) -> float:
    """Извлекает ставку из словаря, пробуя разные ключи."""
    for key in ['hourly_rate', 'rate', 'salary']:
        if key in data:
            return float(data[key])
    return 0.0


def read_employees(file_path: str) -> List[Dict[str, Any]]:
    """Читает данные сотрудников из одного CSV файла."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except FileNotFoundError:
        print(f"[ERROR] Файл не найден: {file_path}")
        return []

    if not lines:
        return []

    headers = parse_csv_line(lines[0])
    employees = []

    for i, line in enumerate(lines[1:], start=2):
        values = parse_csv_line(line)
        if len(values) != len(headers):
            print(f"[WARN] Строка {i} в файле {file_path} пропущена (неверное количество полей)")
            continue

        data = dict(zip(headers, values))
        try:
            employee = {
                'name': data.get('name', 'N/A'),
                'department': data.get('department', 'Unknown'),
                'hours_worked': float(data.get('hours_worked', 0)),
                'hourly_rate': parse_rate(data)
            }
            employees.append(employee)
        except (ValueError, TypeError) as e:
            print(f"[ERROR] Ошибка обработки строки {i} в файле {file_path}: {e}")

    return employees


# --- НОВАЯ ВЕРСИЯ ФУНКЦИИ payout_report ---

def payout_report(employees: List[Dict[str, Any]]):
    """
    Генерирует и выводит в консоль текстовый отчет по зарплатам,
    сгруппированный по отделам.
    """
    # 1. Группируем сотрудников по отделам
    departments = defaultdict(list)
    for emp in employees:
        departments[emp['department']].append(emp)

    # 2. Выводим шапку отчета
    print(f"{'name':<30} {'hours':>10} {'rate':>10} {'payout':>10}")
    print("-" * 64)

    # 3. Итерируемся по отделам и выводим данные
    for department_name, staff in departments.items():
        print(f"\n{department_name}")

        dept_total_hours = 0
        dept_total_payout = 0

        for emp in staff:
            payout = emp['hours_worked'] * emp['hourly_rate']
            dept_total_hours += emp['hours_worked']
            dept_total_payout += payout

            # Форматируем строку для каждого сотрудника
            name = f"---------- {emp['name']}"
            hours_str = str(int(emp['hours_worked']))
            rate_str = str(int(emp['hourly_rate']))
            payout_str = f"${int(payout)}"

            print(f"{name:<30} {hours_str:>10} {rate_str:>10} {payout_str:>10}")

        # Выводим итоги по отделу
        total_hours_str = str(int(dept_total_hours))
        total_payout_str = f"${int(dept_total_payout)}"
        print(f"{'':<30} {total_hours_str:>10} {'':>10} {total_payout_str:>10}")


# --- ОБНОВЛЕННАЯ ФУНКЦИЯ main ---

def main():
    parser = argparse.ArgumentParser(description="Employee salary report generator")
    parser.add_argument('files', nargs='+', help='CSV файлы с данными сотрудников')
    parser.add_argument('--report', required=True, choices=['payout'],
                        help='Тип отчёта (поддерживается только "payout")')
    args = parser.parse_args()

    employees = []
    for file in args.files:
        employees.extend(read_employees(file))

    if not employees:
        print("[WARN] Нет данных для формирования отчета.")
        return

    if args.report in REPORTS:
        print("[INFO] Генерация отчёта payout...\n")
        REPORTS[args.report](employees)  # Функция теперь сама печатает отчет
        print("\n[INFO] Отчёт готов.")
    else:
        # Эта ветка сейчас недостижима из-за `choices` в argparse, но полезна для расширяемости
        print(f"[ERROR] Отчёт '{args.report}' не поддерживается.")


REPORTS = {'payout': payout_report}

if __name__ == '__main__':
    main()