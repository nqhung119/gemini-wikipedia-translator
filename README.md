# Dịch Wikipedia EN → VI

Ứng dụng desktop (Python + tkinter) lấy bài viết Wikipedia tiếng Anh, dịch sang tiếng Việt qua Gemini API và xuất mã nguồn wikitext.

## Cài đặt

```bash
pip install -r requirements.txt
```

Lấy API key Gemini (miễn phí) tại [Google AI Studio](https://aistudio.google.com/apikey), sau đó nhập vào ô "API key" trong ứng dụng.

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

## Cấu trúc (Phase 1–5)

- `src/main.py` — entry point, khởi chạy GUI
- `src/gui/app.py` — cửa sổ chính (fetch + dịch + kiểm tra chạy nền qua `run_background`)
- `src/gui/background.py` — **Phase 4:** `run_background(root, task_fn, on_done)` chạy tác vụ nền, callback trên main thread
- `src/gui/frames.py` — ô link, cấu hình, thanh trạng thái, nút Lấy wikitext / Dịch / **Kiểm tra & Chuẩn hóa**, ô log, wikitext EN/VI, **Kết quả kiểm tra**
- `src/wikipedia/fetch.py` — parse URL → title, GET MediaWiki REST API → wikitext
- `src/translate/gemini_client.py` — dịch wikitext EN → VI qua Gemini API (giữ cú pháp wikitext)
- `src/check/layout.py` — **Phase 5:** kiểm tra bố cục wikitext ([[ ]], {{ }}, \<ref\>, {{reflist}})
- `src/config_loader.py` — đọc/ghi `config/config.json` (API key, model)
- `docs/ke-hoach.md` — kế hoạch triển khai theo phase

## Tài liệu

- [docs/nghien-cuu.md](docs/nghien-cuu.md) — nghiên cứu luồng, API, Gemini
- [docs/ke-hoach.md](docs/ke-hoach.md) — kế hoạch và phân đoạn
- [docs/vi-du.md](docs/vi-du.md) — mẫu wikitext
