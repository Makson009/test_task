import pytest
from io import StringIO
import builtins
from main import parse_rate, read_employees, payout_report

# Тест парсинга ставки
@pytest.mark.parametrize("data, expected", [
    ({'hourly_rate': '50'}, 50.0),
    ({'rate': '40'}, 40.0),
    ({'salary': '30'}, 30.0),
    ({}, 0.0)
])
def test_parse_rate(data, expected):
    assert parse_rate(data) == expected

# Тест чтения сотрудников из CSV-строки
def test_read_employees(monkeypatch):
    csv = (
        "id,email,name,department,hours_worked,hourly_rate\n"
        "1,test@example.com,Test User,IT,100,50\n"
    )

    def mock_open(*args, **kwargs):
        return StringIO(csv)

    monkeypatch.setattr(builtins, "open", mock_open)
    employees = read_employees("fake.csv")

    assert len(employees) == 1
    emp = employees[0]
    assert emp['name'] == "Test User"
    assert emp['hourly_rate'] == 50.0
    assert emp['hours_worked'] == 100.0

# Тест отчёта payout
def test_payout_report():
    employees = [
        {'name': 'Alice', 'hours_worked': 100, 'hourly_rate': 10},
        {'name': 'Bob', 'hours_worked': 120, 'hourly_rate': 20}
    ]
    result = payout_report(employees)
    assert result['total_payout'] == 100 * 10 + 120 * 20

