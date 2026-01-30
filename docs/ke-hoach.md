# Kế hoạch triển khai: Dịch Wikipedia EN → VI (Python + tkinter)

*Dựa trên [nghien-cuu.md](./nghien-cuu.md). Cập nhật: 30/1/2026.*

---

## 1. Mục tiêu dự án

- **Ứng dụng desktop** (Python + GUI tkinter) thực hiện:
  1. Nhập link bài viết Wikipedia tiếng Anh.
  2. Lấy wikitext EN qua Wikipedia REST API.
  3. Dịch sang tiếng Việt bằng Gemini API (giữ cấu trúc wikitext).
  4. Kiểm tra: bố cục, nội dung (thiếu/sai/lặp), chuẩn hóa thuật ngữ/link/citation.
  5. Xuất mã nguồn wikitext tiếng Việt (copy/save, sẵn sàng source editing).

---

## 2. Công nghệ

| Thành phần | Công nghệ |
|------------|-----------|
| Ngôn ngữ | **Python 3.10+** |
| GUI | **tkinter** (thư viện chuẩn) |
| Gọi Wikipedia | **requests** (MediaWiki REST API: `rest.php/v1/page/{title}`) |
| Gọi Gemini | **google-generativeai** (Gemini API) |
| Parse URL / xử lý chuỗi | **urllib.parse**, **re** |
| Lưu cấu hình (API key, User-Agent) | **json** hoặc file `.env` (optional) |

---

## 3. Cấu trúc thư mục dự kiến

```
automatic-wikipedia-translation/
├── docs/
│   ├── nghien-cuu.md
│   ├── ke-hoach.md
│   └── vi-du.md
├── src/
│   ├── __init__.py
│   ├── main.py              # Entry point, khởi chạy GUI
│   ├── gui/
│   │   ├── __init__.py
│   │   ├── app.py            # Cửa sổ chính tkinter
│   │   ├── frames.py         # Các frame: nhập link, cấu hình, kết quả
│   │   └── dialogs.py        # Hộp thoại: cài đặt API key, thông báo lỗi
│   ├── wikipedia/
│   │   ├── __init__.py
│   │   ├── fetch.py          # Parse URL → title, GET rest.php → wikitext
│   │   └── parser.py         # Kiểm tra bố cục (regex/đếm [[ ]], {{ }}, <ref>)
│   ├── translate/
│   │   ├── __init__.py
│   │   ├── gemini_client.py  # Gọi Gemini API, prompt dịch wikitext
│   │   └── chunker.py        # Chia bài dài theo section (nếu cần)
│   └── check/
│       ├── __init__.py
│       ├── layout.py         # Kiểm tra bố cục (tiêu đề, bảng, template)
│       ├── content.py       # So sánh EN/VI (thiếu, lặp), gợi ý review
│       └── normalize.py     # Chuẩn hóa thuật ngữ (glossary), link, ref
├── config/
│   └── config.json          # API key, User-Agent, model mặc định (optional)
├── requirements.txt
└── README.md
```

---

## 4. Thiết kế GUI (tkinter)

### 4.1. Cửa sổ chính

- **Title:** Ví dụ: "Dịch Wikipedia EN → VI".
- **Kích thước:** Có thể resize; min size phù hợp (ví dụ 800×600).

### 4.2. Các vùng chính

| Vùng | Widget | Mô tả |
|------|--------|--------|
| **Nhập link** | `Entry` + `Label` | Ô nhập URL bài Wikipedia tiếng Anh (vd: `https://en.wikipedia.org/wiki/Front-side_bus`). |
| **Nút hành động** | `Button` | "Lấy wikitext" → chỉ fetch EN; "Dịch sang tiếng Việt" → fetch (nếu chưa) + gọi Gemini; "Kiểm tra & Chuẩn hóa" → chạy bước kiểm tra/chuẩn hóa. Có thể gộp thành một luồng "Chạy tất cả". |
| **Cấu hình** | `Frame` với `Entry`/`Combobox` | API key Gemini (hoặc đọc từ config); chọn model (gemini-2.5-flash, gemini-2.5-pro, gemini-3-pro, …); User-Agent cho Wikipedia (có thể ẩn trong Settings). |
| **Trạng thái / Log** | `Text` hoặc `Label` | Hiển thị tiến trình: "Đang lấy wikitext...", "Đang dịch...", "Xong." hoặc lỗi. |
| **Wikitext EN** | `ScrolledText` (tkinter.scrolledtext) | Hiển thị wikitext tiếng Anh (read-only hoặc chỉ đọc). |
| **Wikitext VI** | `ScrolledText` | Hiển thị wikitext tiếng Việt sau dịch; cho phép chỉnh tay trước khi copy/save. |
| **Kết quả kiểm tra** | `Text` hoặc `Listbox` | Liệt kê cảnh báo: bố cục, thiếu đoạn, gợi ý chuẩn hóa thuật ngữ/link. |
| **Nút xuất** | `Button` | "Copy wikitext VI", "Lưu ra file .txt / .wiki". |

### 4.3. Luồng thao tác (GUI)

1. User dán link → (tùy chọn) nhập API key nếu chưa lưu.
2. Bấm "Lấy wikitext" → gọi `wikipedia.fetch` → hiển thị wikitext EN trong ô tương ứng; log trạng thái.
3. Bấm "Dịch sang tiếng Việt" → gọi `translate.gemini_client` (có thể dùng `chunker` nếu bài dài) → hiển thị wikitext VI; log trạng thái.
4. Bấm "Kiểm tra & Chuẩn hóa" → gọi `check.layout`, `check.content`, `check.normalize` → hiển thị báo cáo trong vùng "Kết quả kiểm tra"; có thể áp dụng một số chuẩn hóa tự động lên ô Wikitext VI.
5. User xem/sửa wikitext VI → "Copy" hoặc "Lưu file".

### 4.4. Chạy tác vụ nền (tránh đơ GUI)

- Dùng **threading**: các bước fetch/dịch/kiểm tra chạy trong `threading.Thread`, cập nhật GUI qua `root.after()` hoặc `queue.Queue` để tránh block main thread.
- Disable nút "Dịch" / "Lấy wikitext" khi đang chạy; hiển thị trạng thái "Đang xử lý...".

---

## 5. Các module chức năng (Python)

### 5.1. `wikipedia.fetch`

- **Input:** URL (string) hoặc title (string).
- **Xử lý:** `urllib.parse` lấy path, tách phần sau `/wiki/` → title; thay space bằng `_` nếu cần.
- **API:** `GET https://en.wikipedia.org/w/rest.php/v1/page/{title}` với header `User-Agent`.
- **Output:** Wikitext (string) hoặc raise nếu lỗi (404, network).  
- **Tham chiếu:** [nghien-cuu.md § 3](./nghien-cuu.md#3-lấy-nội-dung-wikipedia-tiếng-anh-wikitext).

### 5.2. `translate.gemini_client`

- **Input:** Wikitext EN (string), API key, tên model (vd: `gemini-2.5-flash`).
- **Prompt:** Theo [nghien-cuu.md § 4.2](./nghien-cuu.md#42-dùng-gemini-api-cập-nhật-3012026): dịch sang tiếng Việt, **giữ nguyên cú pháp wikitext** (template, link, ref, bảng, tiêu đề). Có thể đính kèm 1 đoạn mẫu từ vi-du.md.
- **Output:** Wikitext tiếng Việt (string). Bài rất dài: có thể dùng `chunker` chia theo `==Section==` rồi dịch từng phần, nối lại.

### 5.3. `translate.chunker`

- Tách wikitext thành các block (theo `==...==` hoặc kích thước tối đa token/char) để gửi Gemini từng phần; nối lại đúng thứ tự.

### 5.4. `check.layout`

- Đếm/cân bằng `[[`, `]]`, `{{`, `}}`, `<ref>`, `</ref>`; kiểm tra có `{{reflist}}` hoặc tương đương; cảnh báo nếu thiếu đóng mở.
- **Output:** Danh sách cảnh báo (list of str) để hiển thị trên GUI.

### 5.5. `check.content`

- So sánh sơ bộ EN vs VI: số section, độ dài tương đối; có thể gọi Gemini với prompt "đối chiếu EN và VI, liệt kê chỗ nghi ngờ dịch sai/thiếu".
- **Output:** Danh sách gợi ý/cảnh báo.

### 5.6. `check.normalize`

- **(Tùy chọn pha 1)** Áp dụng bảng thuật ngữ EN→VI (file từ vựng hoặc dict); thay thế nhất quán trong wikitext VI.
- Kiểm tra link nội bộ `[[...]]`: gợi ý hoặc map sang title tiếng Việt nếu có quy tắc.
- **Output:** Wikitext VI đã chuẩn hóa một phần + báo cáo thay đổi.

---

## 6. Phân đoạn triển khai (phases)

| Phase | Nội dung | Ưu tiên |
|-------|----------|--------|
| **1** | Cấu trúc repo, `requirements.txt`, `main.py` gọi GUI cơ bản (tkinter). Cửa sổ có ô link, nút "Lấy wikitext", ô log, ô wikitext EN. | Cao |
| **2** | `wikipedia.fetch`: parse URL, gọi REST API, hiển thị wikitext EN trên GUI. | Cao |
| **3** | Cấu hình API key (ô nhập hoặc file config). `translate.gemini_client`: gọi Gemini, prompt dịch giữ wikitext. Nút "Dịch sang tiếng Việt", ô wikitext VI. | Cao |
| **4** | Chạy tác vụ nền (threading) để GUI không đơ khi fetch/dịch. | Cao |
| **5** | `check.layout`: kiểm tra bố cục; hiển thị cảnh báo trên GUI. Nút "Kiểm tra & Chuẩn hóa". | Trung bình |
| **6** | `check.content` (so sánh EN/VI, gợi ý sai/thiếu); `check.normalize` (glossary cơ bản). | Trung bình |
| **7** | Nút "Copy", "Lưu file"; cải thiện UX (tooltip, menu, resize). | Trung bình |
| **8** | `chunker` cho bài dài; tùy chọn model (Gemini 2.5/3). | Thấp |

---

## 7. Phụ thuộc (requirements.txt)

```text
requests>=2.28.0
google-generativeai>=0.8.0
```

- **tkinter:** Đi kèm Python (trên Windows/macOS/Linux thường đã có; Linux có thể cần gói `python3-tk`).

---

## 8. Tài liệu tham chiếu

- [nghien-cuu.md](./nghien-cuu.md) — nghiên cứu luồng, API, Gemini, kiểm tra, chuẩn hóa.
- [vi-du.md](./vi-du.md) — mẫu wikitext (Front-side bus) dùng cho prompt và test.
- [MediaWiki REST API](https://www.mediawiki.org/wiki/API:REST_API/Reference).
- [Gemini API – Models](https://ai.google.dev/gemini-api/docs/models).

---

## 9. Rủi ro và giảm thiểu

| Rủi ro | Giảm thiểu |
|--------|------------|
| Bài quá dài vượt context Gemini | Chia section (`chunker`), dịch từng phần rồi nối. |
| API key lộ khi lưu config | Lưu vào file ngoài repo (`.env` hoặc config trong thư mục user); thêm vào `.gitignore`. |
| Wikipedia chặn request thiếu User-Agent | Luôn gửi User-Agent hợp lệ (tên app + contact). |
| Dịch làm vỡ cú pháp wikitext | Prompt rõ ràng + bước kiểm tra `check.layout` để cảnh báo và sửa tay. |

---

*Kế hoạch này đủ để bắt đầu triển khai từ Phase 1; có thể bổ sung chi tiết từng file (signature hàm, ví dụ code) trong từng phase.*
