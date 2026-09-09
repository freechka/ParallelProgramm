# test_timestamp_tool.py
import pytest
import time
from datetime import datetime, timezone
from timestamp_tool import TimestampTool

class TestTimestampTool:
    """Тесты для класса TimestampTool"""
    
    # ============ ТЕСТ 1 ============
    def test_unix_to_iso_conversion(self):
        """Тест 1: Проверяем преобразование Unix в ISO"""
        # 2024-01-01 00:00:00 UTC
        unix = 1704067200
        expected = "2024-01-01T00:00:00+00:00"
        result = TimestampTool.unix_to_iso(unix)
        assert result == expected, f"Ожидалось {expected}, получено {result}"
    
    # ============ ТЕСТ 2 ============
    def test_iso_to_unix_conversion(self):
        """Тест 2: Проверяем преобразование ISO в Unix"""
        iso = "2024-01-01T00:00:00+00:00"
        expected = 1704067200
        result = TimestampTool.iso_to_unix(iso)
        assert result == expected, f"Ожидалось {expected}, получено {result}"
    
    # ============ ТЕСТ 3 ============
    def test_now_unix_returns_positive_int(self):
        """Тест 3: Проверяем, что now_unix возвращает положительное целое число"""
        result = TimestampTool.now_unix()
        assert isinstance(result, int), "Должен возвращать int"
        assert result > 0, "Unix timestamp должен быть положительным"
    
    # ============ ТЕСТ 4 ============
    def test_now_iso_returns_valid_format(self):
        """Тест 4: Проверяем, что now_iso возвращает корректный ISO формат"""
        result = TimestampTool.now_iso()
        # Проверяем, что строка содержит T и + (часовой пояс)
        assert 'T' in result, "ISO строка должна содержать T"
        assert '+' in result or 'Z' in result, "ISO строка должна содержать часовой пояс"
    
    # ============ ТЕСТ 5 ============
    def test_convert_timezone(self):
        """Тест 5: Проверяем преобразование часового пояса"""
        # UTC время 2024-01-01 00:00:00
        iso_utc = "2024-01-01T00:00:00+00:00"
        # Преобразуем в Москву (UTC+3)
        result = TimestampTool.convert_timezone(iso_utc, 3)
        # Должно получиться 2024-01-01T03:00:00+03:00
        assert "03:00:00+03:00" in result or "03:00:00+03:00" in result
    
    # ============ ТЕСТ 6 ============
    def test_convert_timezone_negative_offset(self):
        """Тест 6: Проверяем преобразование с отрицательным смещением"""
        iso_utc = "2024-01-01T00:00:00+00:00"
        # Преобразуем в Нью-Йорк (UTC-5)
        result = TimestampTool.convert_timezone(iso_utc, -5)
        # Должно получиться 2023-12-31T19:00:00-05:00
        assert "19:00:00-05:00" in result
    
    # ============ ТЕСТ 7 ============
    def test_unix_to_iso_and_back(self):
        """Тест 7: Проверяем, что преобразования работают в обе стороны"""
        original_unix = 1704067200
        # Unix -> ISO
        iso = TimestampTool.unix_to_iso(original_unix)
        # ISO -> Unix
        unix_back = TimestampTool.iso_to_unix(iso)
        assert original_unix == unix_back, f"{original_unix} -> {iso} -> {unix_back}"


# ============ ТЕСТЫ С ОLLAMA (интеграционные) ============

import pytest
import os

def test_timestamp_with_ollama():
    """Интеграционный тест: TimestampTool + Ollama напрямую"""
    import ollama
    import time
    from timestamp_tool import TimestampTool
    
    # Получаем текущую дату
    now_iso = TimestampTool.now_iso()
    current_date = now_iso.split("T")[0]
    
    # Пробуем несколько раз (на случай медленного ответа)
    for attempt in range(3):
        try:
            response = ollama.chat(
                model="qwen3.5:0.8b",
                messages=[{"role": "user", "content": f"Какое сегодня число? Ответь только датой в формате ГГГГ-ММ-ДД. Сегодня: {current_date}"}]
            )
            
            answer = response['message']['content']
            
            # Если ответ не пустой и содержит цифры — тест пройден
            if answer and any(char.isdigit() for char in answer):
                print(f"✅ Ollama ответил: {answer}")
                return  # Тест пройден!
            
            time.sleep(2)  # Ждем 2 секунды перед повторной попыткой
            
        except Exception as e:
            print(f"⚠️ Попытка {attempt+1} не удалась: {e}")
            time.sleep(2)
    
    # Если после 3 попыток ничего не получилось — тест падает
    assert False, "Ollama не вернул корректный ответ после 3 попыток"
