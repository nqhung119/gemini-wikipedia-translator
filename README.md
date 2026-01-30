# Dịch Wikipedia EN → VI

Ứng dụng desktop (Python + tkinter) lấy bài viết Wikipedia tiếng Anh, dịch sang tiếng Việt qua Gemini API và xuất mã nguồn wikitext.

## Cài đặt

```bash
pip install -r requirements.txt
```

## Chạy ứng dụng (Phase 1)

Từ thư mục gốc dự án:

```bash
python -m src.main
```

Hoặc:

```bash
python src/main.py
```

*(Nếu báo lỗi import, chạy từ thư mục gốc và dùng `python -m src.main`.)*

## Cấu trúc (Phase 1 + 2)

- `src/main.py` — entry point, khởi chạy GUI
- `src/gui/app.py` — cửa sổ chính (fetch chạy nền, cập nhật wikitext EN)
- `src/gui/frames.py` — ô link, nút "Lấy wikitext", ô log, ô wikitext EN
- `src/wikipedia/fetch.py` — parse URL → title, GET MediaWiki REST API → wikitext
- `docs/ke-hoach.md` — kế hoạch triển khai theo phase

## Tài liệu

- [docs/nghien-cuu.md](docs/nghien-cuu.md) — nghiên cứu luồng, API, Gemini
- [docs/ke-hoach.md](docs/ke-hoach.md) — kế hoạch và phân đoạn
- [docs/vi-du.md](docs/vi-du.md) — mẫu wikitext
