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

## Cấu trúc (Phase 1–8)

- `src/main.py` — entry point, khởi chạy GUI
- `src/gui/app.py` — cửa sổ chính (fetch + dịch + kiểm tra chạy nền), menu File/Help, Copy / Lưu file
- `src/gui/background.py` — **Phase 4:** `run_background(root, task_fn, on_done)` chạy tác vụ nền
- `src/gui/frames.py` — ô link, cấu hình (model: **gemini-1.5 / 2.0 / 2.5 / 3**), thanh trạng thái, nút, ô log, wikitext EN/VI, frame Xuất, Kết quả kiểm tra, Áp dụng chuẩn hóa
- `src/gui/dialogs.py` — show_error, show_info, add_tooltip
- `src/wikipedia/fetch.py` — parse URL → title, GET MediaWiki REST API → wikitext
- `src/translate/gemini_client.py` — dịch wikitext EN → VI (**translate_wikitext_chunked** cho bài dài, Phase 8)
- `src/translate/chunker.py` — **Phase 8:** tách wikitext theo section (==...==) hoặc max_chars để dịch từng phần
- `src/check/layout.py` — **Phase 5:** kiểm tra bố cục wikitext
- `src/check/content.py` — **Phase 6:** so sánh EN vs VI
- `src/check/normalize.py` — **Phase 6:** chuẩn hóa thuật ngữ, gợi ý link; `config/glossary.txt` (tùy chọn)
- `src/config_loader.py` — đọc/ghi `config/config.json` (API key, model)
- `docs/ke-hoach.md` — kế hoạch triển khai theo phase

## Tài liệu

- [docs/nghien-cuu.md](docs/nghien-cuu.md) — nghiên cứu luồng, API, Gemini
- [docs/ke-hoach.md](docs/ke-hoach.md) — kế hoạch và phân đoạn
- [docs/vi-du.md](docs/vi-du.md) — mẫu wikitext
