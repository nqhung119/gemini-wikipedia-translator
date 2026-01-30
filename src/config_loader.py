"""
Đọc/ghi cấu hình (API key, model) từ config/config.json.
"""
import json
import logging
from pathlib import Path

CONFIG_DEFAULT = {
    "api_key": "",
    "model": "gemini-3-flash-preview",
    "source_lang": "en",
    "target_lang": "vi",
}
_log = logging.getLogger(__name__)


def _config_path():
    base = Path(__file__).resolve().parent.parent
    return base / "config" / "config.json"


def load_config():
    """Trả về dict với api_key, model. Nếu không có file thì trả về mặc định."""
    p = _config_path()
    if not p.exists():
        return dict(CONFIG_DEFAULT)
    try:
        with open(p, "r", encoding="utf-8") as f:
            data = json.load(f)
        if not isinstance(data, dict):
            _log.warning("config.json không phải object, dùng mặc định")
            return dict(CONFIG_DEFAULT)
        return {**CONFIG_DEFAULT, **data}
    except json.JSONDecodeError as e:
        _log.warning("config.json lỗi JSON: %s", e)
        return dict(CONFIG_DEFAULT)
    except OSError as e:
        _log.warning("Không đọc được config: %s", e)
        return dict(CONFIG_DEFAULT)


def save_config(
    api_key: str = "",
    model: str = "",
    source_lang: str = "",
    target_lang: str = "",
):
    """Ghi api_key, model, source_lang, target_lang vào config.json (chỉ ghi field không rỗng).
    Trả về True nếu ghi thành công, False nếu lỗi."""
    p = _config_path()
    try:
        p.parent.mkdir(parents=True, exist_ok=True)
        current = load_config()
        if api_key is not None:
            current["api_key"] = (api_key or "").strip()
        if model is not None:
            current["model"] = (model or CONFIG_DEFAULT["model"]).strip()
        if source_lang is not None and (source_lang or "").strip():
            current["source_lang"] = (source_lang or "").strip().lower()
        if target_lang is not None and (target_lang or "").strip():
            current["target_lang"] = (target_lang or "").strip().lower()
        with open(p, "w", encoding="utf-8") as f:
            json.dump(current, f, indent=2, ensure_ascii=False)
        return True
    except OSError as e:
        _log.warning("Không ghi được config: %s", e)
        return False
