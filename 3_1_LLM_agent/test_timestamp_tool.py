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
import os

@pytest.mark.skipif(
    os.environ.get("CI") == "true",
    reason="Skipping integration test in CI environment"
)
def test_llm_agent_with_timestamp():
    """Интеграционный тест: LLMAgent использует TimestampTool"""
    try:
        from llm_agent.core_v2 import LLMAgent
        from timestamp_tool import TimestampTool
        
        agent = LLMAgent(local=True, ollama_model="qwen3.5:0.8b")
        
        query = "Какое сегодня число? Напиши только дату в формате ГГГГ-ММ-ДД"
        response = agent.process_query(query)
        
        assert any(char.isdigit() for char in response), "Ответ должен содержать цифры"
        print(f"✅ Тест пройден! Ответ: {response}")
        
    except ImportError as e:
        pytest.skip(f"Модуль не найден: {e}")
