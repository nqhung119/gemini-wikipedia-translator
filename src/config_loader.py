"""
Đọc/ghi cấu hình (API key, model) từ config/config.json.
"""
import json
from pathlib import Path

CONFIG_DEFAULT = {"api_key": "", "model": "gemini-3-flash-preview"}


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
        return {**CONFIG_DEFAULT, **data}
    except Exception:
        return dict(CONFIG_DEFAULT)


def save_config(api_key: str = "", model: str = ""):
    """Ghi api_key và model vào config.json (chỉ ghi field không rỗng)."""
    p = _config_path()
    p.parent.mkdir(parents=True, exist_ok=True)
    current = load_config()
    if api_key is not None:
        current["api_key"] = (api_key or "").strip()
    if model is not None:
        current["model"] = (model or CONFIG_DEFAULT["model"]).strip()
    with open(p, "w", encoding="utf-8") as f:
        json.dump(current, f, indent=2, ensure_ascii=False)
