"""
Chạy tác vụ nền (threading) và gọi callback trên main thread (tkinter).
Tham chiếu: docs/ke-hoach.md § 4.4.
"""
import threading
import tkinter as tk
from typing import Callable, Any


def run_background(
    root: tk.Tk,
    task_fn: Callable[[], Any],
    on_done: Callable[[bool, Any], None],
) -> None:
    """
    Chạy task_fn() trong thread phụ; khi xong (hoặc lỗi) gọi on_done trên main thread.

    - task_fn(): không tham số; return giá trị (thành công) hoặc raise Exception (thất bại).
    - on_done(success: bool, data: Any): gọi trên main thread;
      success=True và data=giá trị trả về của task_fn;
      success=False và data=str(exception).

    Tránh block GUI: worker chạy trong threading.Thread(daemon=True),
    on_done được lên lịch bằng root.after(0, ...).
    """
    def worker():
        try:
            result = task_fn()
            root.after(0, lambda r=result: on_done(True, r))
        except Exception as e:
            err = str(e)
            root.after(0, lambda e=err: on_done(False, e))

    threading.Thread(target=worker, daemon=True).start()
