"""Hộp thoại: cài đặt API key, thông báo lỗi (Phase 1: minimal)."""
import tkinter as tk
from tkinter import messagebox


def show_error(parent, title, message):
    """Hiển thị hộp thoại lỗi."""
    messagebox.showerror(title, message, parent=parent)


def show_info(parent, title, message):
    """Hiển thị hộp thoại thông tin."""
    messagebox.showinfo(title, message, parent=parent)
