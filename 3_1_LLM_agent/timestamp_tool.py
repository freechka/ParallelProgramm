# timestamp_tool.py
from datetime import datetime, timezone, timedelta
import time

class TimestampTool:
    """Класс для работы с временными метками"""
    
    @staticmethod
    def unix_to_iso(unix_timestamp: int) -> str:
        """Преобразует Unix timestamp в ISO 8601 строку (UTC)"""
        dt = datetime.fromtimestamp(unix_timestamp, tz=timezone.utc)
        return dt.isoformat()
    
    @staticmethod
    def iso_to_unix(iso_string: str) -> int:
        """Преобразует ISO 8601 строку в Unix timestamp"""
        # Убираем Z если есть
        if iso_string.endswith('Z'):
            iso_string = iso_string.replace('Z', '+00:00')
        dt = datetime.fromisoformat(iso_string)
        return int(dt.timestamp())
    
    @staticmethod
    def now_unix() -> int:
        """Возвращает текущий Unix timestamp"""
        return int(time.time())
    
    @staticmethod
    def now_iso() -> str:
        """Возвращает текущее время в ISO 8601 формате (UTC)"""
        return datetime.now(timezone.utc).isoformat()
    
    @staticmethod
    def convert_timezone(iso_string: str, target_tz_offset: int) -> str:
        """
        Преобразует время из UTC в указанный часовой пояс.
        target_tz_offset: смещение в часах (например, 3 для Москвы)
        """
        dt = datetime.fromisoformat(iso_string.replace('Z', '+00:00'))
        target_tz = timezone(timedelta(hours=target_tz_offset))
        dt_target = dt.astimezone(target_tz)
        return dt_target.isoformat()
