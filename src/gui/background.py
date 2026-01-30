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

            def _done_ok(r=result):
                if root.winfo_exists():
                    on_done(True, r)

            root.after(0, _done_ok)
        except Exception as e:
            err = str(e)

            def _done_err(e=err):
                if root.winfo_exists():
                    on_done(False, e)

            root.after(0, _done_err)

    threading.Thread(target=worker, daemon=True).start()
