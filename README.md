# Wikipedia EN → VI Translator

Ứng dụng desktop dịch bài viết Wikipedia tiếng Anh sang tiếng Việt qua Gemini API, xuất mã nguồn wikitext sẵn sàng cho source editing trên Wikipedia tiếng Việt.

---

## Tính năng

- **Lấy wikitext** — Nhập link bài Wikipedia tiếng Anh, lấy mã nguồn wikitext qua MediaWiki REST API.
- **Dịch bằng Gemini** — Dịch sang tiếng Việt, giữ cú pháp wikitext (template, link, ref, bảng, tiêu đề).
- **Chunker cho bài dài** — Tự động chia theo section hoặc kích thước, dịch từng phần rồi nối.
- **Kiểm tra & chuẩn hóa** — Kiểm tra bố cục ([[ ]], {{ }}, \<ref\>, {{reflist}}); so sánh EN/VI (section, độ dài); chuẩn hóa thuật ngữ (glossary); gợi ý link nội bộ.
- **Xuất** — Copy wikitext VI vào clipboard hoặc lưu ra file (.wiki / .txt).
- **GUI** — tkinter, menu File/Help, tooltip, chạy tác vụ nền (không đơ giao diện).

---

## Yêu cầu

- **Python** 3.10 trở lên
- **Hệ điều hành** Windows / macOS / Linux (tkinter thường đi kèm Python; Linux có thể cần `python3-tk`)
- **API key** Gemini (miễn phí tại [Google AI Studio](https://aistudio.google.com/apikey))

---

## Cài đặt

1. Clone hoặc tải repository về máy.

2. Tạo môi trường ảo (khuyến nghị):

   ```bash
   python -m venv .venv
   .venv\Scripts\activate   # Windows
   # source .venv/bin/activate   # macOS / Linux
   ```

3. Cài đặt phụ thuộc:

   ```bash
   pip install -r requirements.txt
   ```

---

## Cấu hình

- **API key Gemini** — Nhập vào ô "API key" trong ứng dụng; có thể lưu vào `config/config.json` (tự lưu khi dịch). Không commit file này (đã có trong `.gitignore`).
- **Model** — Chọn trong combobox: `gemini-1.5-flash`, `gemini-1.5-pro`, `gemini-2.0-flash`, `gemini-2.5-flash`, `gemini-2.5-pro`, `gemini-3-flash`, `gemini-3-pro` (tùy API hỗ trợ).
- **Glossary** (tùy chọn) — Thêm file `config/glossary.txt`, mỗi dòng: `EN\tVI` hoặc `EN=VI` để chuẩn hóa thuật ngữ khi bấm "Kiểm tra & Chuẩn hóa".

---

## Chạy ứng dụng

Từ thư mục gốc dự án:

```bash
python -m src.main
```

Hoặc:

```bash
python src/main.py
```

Nếu báo lỗi import, đảm bảo chạy từ thư mục gốc và dùng `python -m src.main`.

---

## Quy trình sử dụng

1. Nhập **link** bài Wikipedia tiếng Anh (ví dụ: `https://en.wikipedia.org/wiki/Front-side_bus`).
2. Bấm **Lấy wikitext** — wikitext EN hiển thị ở ô tương ứng.
3. Nhập **API key** Gemini (nếu chưa lưu), chọn **model**, bấm **Dịch sang tiếng Việt** — wikitext VI hiển thị ở ô Wikitext VI.
4. (Tùy chọn) Bấm **Kiểm tra & Chuẩn hóa** — xem cảnh báo bố cục, nội dung, chuẩn hóa; có thể bấm **Áp dụng chuẩn hóa lên Wikitext VI**.
5. Chỉnh sửa tay nếu cần, rồi **Copy wikitext VI** hoặc **Lưu ra file...** (hoặc **File → Lưu Wikitext VI...**).

---

## Cấu trúc dự án

```
automatic-wikipedia-translation/
├── config/                 # Cấu hình (config.json, glossary.txt — không commit config.json)
│   └── .gitkeep
├── docs/
│   ├── nghien-cuu.md       # Nghiên cứu luồng, API, Gemini, kiểm tra
│   ├── ke-hoach.md         # Kế hoạch triển khai theo phase
│   └── vi-du.md            # Mẫu wikitext (Front-side bus)
├── src/
│   ├── main.py             # Entry point, khởi chạy GUI
│   ├── config_loader.py     # Đọc/ghi config (API key, model)
│   ├── gui/
│   │   ├── app.py           # Cửa sổ chính
│   │   ├── frames.py        # Các frame (link, cấu hình, log, wikitext EN/VI, xuất, kết quả kiểm tra)
│   │   ├── dialogs.py       # Hộp thoại, tooltip
│   │   └── background.py    # Chạy tác vụ nền (threading)
│   ├── wikipedia/
│   │   └── fetch.py         # Parse URL, GET MediaWiki REST API → wikitext
│   ├── translate/
│   │   ├── gemini_client.py # Dịch wikitext EN → VI (translate_wikitext, translate_wikitext_chunked)
│   │   └── chunker.py       # Tách wikitext theo section / max_chars cho bài dài
│   └── check/
│       ├── layout.py       # Kiểm tra bố cục ([[ ]], {{ }}, <ref>, {{reflist}})
│       ├── content.py      # So sánh EN vs VI (section, độ dài)
│       └── normalize.py    # Chuẩn hóa thuật ngữ (glossary), gợi ý link
├── .gitignore
├── requirements.txt
└── README.md
```

---

## Tài liệu

| Tài liệu | Mô tả |
|----------|--------|
| [docs/nghien-cuu.md](docs/nghien-cuu.md) | Nghiên cứu: luồng dịch, Wikipedia REST API, Gemini API, kiểm tra & chuẩn hóa |
| [docs/ke-hoach.md](docs/ke-hoach.md) | Kế hoạch triển khai (Phase 1–8), thiết kế GUI, module chức năng |
| [docs/vi-du.md](docs/vi-du.md) | Mẫu wikitext (bài Front-side bus) dùng tham chiếu |

---

## Giấy phép

Dự án tham khảo; xem repository để biết điều khoản sử dụng.
