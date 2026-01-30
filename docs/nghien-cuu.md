# Nghiên cứu: Dịch bài viết Wikipedia EN → VI và trả về mã nguồn (wikitext)

*Cập nhật tham chiếu: 30/1/2026 — mô hình Gemini và API Wikipedia theo thời điểm hiện tại.*

## 1. Mục tiêu nhiệm vụ

- **Đầu vào:** Link bài viết Wikipedia tiếng Anh (ví dụ: `https://en.wikipedia.org/wiki/Front-side_bus`).
- **Xử lý:** Dùng Gemini API để dịch nội dung sang tiếng Việt.
- **Kiểm tra:** Bố cục, nội dung (thiếu / sai / lặp), chuẩn hóa thuật ngữ, link nội bộ, citation/reference.
- **Đầu ra:** Mã nguồn Wikipedia (wikitext) tiếng Việt, sẵn sàng cho source editing (copy vào trang soạn thảo Wikipedia).

Tham chiếu mẫu wikitext: [vi-du.md](./vi-du.md) (bài Front-side bus).

---

## 2. Luồng công việc tổng quát

```
[Link EN Wikipedia] → Lấy wikitext EN → Dịch (Gemini) → Kiểm tra & Chuẩn hóa → Wikitext VI
```

---

## 3. Lấy nội dung Wikipedia tiếng Anh (wikitext)

### 3.1. Từ URL → title trang

- URL dạng: `https://en.wikipedia.org/wiki/Front-side_bus` hoặc `https://en.wikipedia.org/wiki/Earth`.
- **Title** = phần sau `/wiki/`, decode URL (ví dụ: `Front-side_bus` → `Front-side bus` nếu cần hiển thị; với API thường dùng dạng có gạch dưới).
- Có thể dùng `urllib.parse` (Python) hoặc `decodeURIComponent` (JS) để lấy và chuẩn hóa title.

### 3.2. Wikipedia REST API (khuyến nghị 2026)

- **Endpoint khuyến nghị (MediaWiki REST API):**  
  `GET https://en.wikipedia.org/w/rest.php/v1/page/{title}`  
  - Ví dụ: `https://en.wikipedia.org/w/rest.php/v1/page/Front-side_bus`
- **Kết quả:** JSON chứa nội dung trang dạng **wikitext** (và metadata phiên bản, license).
- **Lưu ý:**
  - Nên gửi **User-Agent** (ví dụ: `YourAppName (contact@example.com)`).
  - `title` trong URL thường dùng dạng có gạch dưới thay khoảng trắng.
  - API này **không** yêu cầu Bearer token cho đọc công khai.

**Core REST API (api.wikimedia.org):** Endpoint `GET https://api.wikimedia.org/core/v1/{project}/{language}/page/{title}` dự kiến **lỗi thời dần từ tháng 7/2026**; nên ưu tiên MediaWiki REST API (`rest.php/v1/page/...`) cho dự án mới.

**Cách khác:** MediaWiki Action API (`action=query&prop=revisions&rvprop=content`) cũng trả về wikitext.

---

## 4. Dịch bằng Gemini API và giữ cấu trúc wikitext

### 4.1. Wikitext cần giữ nguyên cấu trúc

Từ [vi-du.md](./vi-du.md), wikitext gồm:

| Thành phần | Ví dụ | Cách xử lý khi dịch |
|------------|--------|----------------------|
| **Template** | `{{Short description|...}}`, `{{cite book\|...}}` | Chỉ dịch chuỗi tiếng Anh bên trong; giữ nguyên tên template và cú pháp `\|`, `}}`. |
| **Link nội bộ** | `[[bus (computing)\|bus]]`, `[[Northbridge (computing)\|northbridge]]` | Dịch phần hiển thị (sau `\|`); phần trang đích có thể giữ EN hoặc map sang title tiếng Việt (xem mục Chuẩn hóa). |
| **Tiêu đề** | `==History==`, `===CPU===` | Dịch nội dung tiêu đề; giữ đúng cấp `=`, `==`, `===`. |
| **In đậm** | `'''front-side bus'''` | Dịch nội dung; giữ `'''`. |
| **Chú thích** | `<ref name="pcs">{{cite book\|...}}</ref>` | Thường **không dịch** nội dung ref (tài liệu gốc); có thể dịch phần mô tả ngắn nếu cộng đồng cho phép. |
| **Bảng** | `{\|class="wikitable" ... \|}` | Dịch ô chữ; giữ nguyên cú pháp `\|-`, `\|`, `!\|`, `{\|`, `\|}`. |
| **Hình** | `[[File:...\|thumb\|...]]` | Thường giữ nguyên; chỉ dịch chuỗi mô tả (caption) nếu có. |
| **Category, DEFAULTSORT** | `[[Category:...]]`, `{{DEFAULTSORT:...}}` | Chuẩn hóa sang tiếng Việt (category và thứ tự sắp xếp). |

### 4.2. Dùng Gemini API (cập nhật 30/1/2026)

- **Mô hình khuyến nghị (thời điểm 2026):**
  - **Gemini 3** (ra mắt 11/2025): `gemini-3-pro` (lý luận mạnh, đa phương thức, context lớn), `gemini-3-flash` (nhanh, chi phí thấp). Phù hợp dịch bài dài, cần giữ cấu trúc.
  - **Gemini 2.5:** `gemini-2.5-pro`, `gemini-2.5-flash`, `gemini-2.5-flash-lite` — lựa chọn cân bằng chất lượng / tốc độ / giá.
  - Có thể dùng tham số **thinking_level** (Gemini 3) để tăng độ sâu lý luận khi cần dịch chuẩn wikitext phức tạp.
- **Truy cập:** Google AI SDK hoặc REST API ([ai.google.dev](https://ai.google.dev)).
- **Prompt (ý tưởng):**
  - Yêu cầu dịch **toàn bộ** văn bản từ tiếng Anh sang tiếng Việt.
  - **Quan trọng:** Giữ nguyên cú pháp wikitext: không xóa/xóa nhầm `[[`, `]]`, `{{`, `}}`, `<ref>`, `|`, `=`, cấu trúc bảng, template.
  - Chỉ dịch phần là “văn bản người đọc” (câu, từ); không dịch tên kỹ thuật trong template (ví dụ `cite book`, `cite web`) trừ khi có hướng dẫn cụ thể.
  - Có thể cho Gemini một đoạn mẫu từ [vi-du.md](./vi-du.md) để nó “bắt chước” style và cách giữ markup.

**Khả năng:** Gemini đủ mạnh để vừa dịch vừa giữ phần lớn cấu trúc; với bài dài hoặc bảng/template phức tạp có thể cần **chia đoạn** (theo section) rồi dịch từng phần để giảm lỗi cú pháp.

---

## 5. Kiểm tra (sau khi dịch)

### 5.1. Bố cục đúng chuẩn

- **Tiêu đề:** Đủ cấp `=`, không thừa/thiếu; thứ tự section hợp lý (mở đầu → nội dung → Ghi chú/Tham khảo → Category).
- **Template đặc biệt:** Ví dụ `{{Short description|...}}`, `{{reflist}}`, infobox (nếu có) vẫn đúng vị trí và cú pháp.
- **Bảng:** Số cột mỗi dòng nhất quán; không vỡ `{\|` … `\|}`.

Có thể dùng **parser wikitext** (thư viện hoặc regex cơ bản) để kiểm tra cân bằng `[[`, `]]`, `{{`, `}}`, `<ref>`, `</ref>`.

### 5.2. Nội dung: thiếu / dịch sai / lặp

- **Thiếu:** So sánh số section, số câu hoặc độ dài tương đối EN vs VI (cảnh báo nếu chênh lệch lớn).
- **Sai:** Có thể dùng Gemini (hoặc model khác) với prompt “đối chiếu bản EN và bản VI, liệt kê chỗ nghi ngờ dịch sai”.
- **Lặp:** Tìm đoạn văn trùng lặp (hash theo câu hoặc đoạn ngắn).

### 5.3. Chuẩn hóa

- **Thuật ngữ:** Dùng bảng thuật ngữ EN→VI (từ Wikipedia tiếng Việt hoặc từ điển chuyên ngành); thay thế nhất quán (ví dụ “front-side bus” → “bus phía trước” hoặc thuật ngữ chuẩn đã dùng trên Wikipedia tiếng Việt).
- **Link nội bộ:**  
  - `[[Tên trang|nhãn hiển thị]]`: nhãn đã dịch; “Tên trang” nên trỏ tới bài viết đúng trên vi.wikipedia (kiểm tra tồn tại trang hoặc dùng interwiki).
- **Citation / reference:** Giữ nguyên format `{{cite book|...}}`, `{{cite web|...}}`; chỉ sửa lỗi do dịch làm vỡ cú pháp (dấu `|`, `=`, `}}`).

---

## 6. Đầu ra: Mã nguồn Wikipedia (source editing)

- Kết quả cuối cùng là **một chuỗi wikitext** (plain text), encoding UTF-8.
- Người dùng có thể copy vào trang soạn thảo Wikipedia tiếng Việt (chế độ “Mã nguồn” / “Edit source”).
- Nên xuất đúng định dạng giống [vi-du.md](./vi-du.md): xuống dòng section, bảng, ref; không cần chuyển sang HTML.

---

## 7. Đánh giá khả năng thực hiện

| Hạng mục | Khả năng | Ghi chú |
|----------|----------|--------|
| Lấy wikitext từ link EN | **Tốt** | REST API hoặc Action API ổn định; chỉ cần parse URL và gọi API. |
| Dịch bằng Gemini giữ markup | **Khả thi, cần chỉnh prompt** | LLM có thể giữ phần lớn cú pháp; nên có bước kiểm tra/validate và có thể chia nhỏ bài dài. |
| Kiểm tra bố cục | **Tốt** | Rule-based + parser/regex đủ để kiểm cơ bản. |
| Kiểm tra thiếu/sai/lặp | **Khả thi** | So sánh EN/VI + prompt “review” bằng Gemini. |
| Chuẩn hóa thuật ngữ, link, ref | **Khả thi** | Glossary + map link; ref chủ yếu giữ nguyên. |
| Trả về đúng dạng source editing | **Tốt** | Output là wikitext thuần, không cần render HTML. |

**Kết luận:** Nhiệm vụ **khả thi**. Nên triển khai theo bước: (1) Lấy wikitext từ link EN, (2) Dịch bằng Gemini với prompt rõ ràng “chỉ dịch văn bản, giữ wikitext”, (3) Bước kiểm tra và chuẩn hóa (có thể bán tự động), (4) Xuất wikitext tiếng Việt. Có thể lấy [vi-du.md](./vi-du.md) làm test case (so sánh với bản EN gốc và bản dịch mẫu) để tinh chỉnh prompt và quy tắc chuẩn hóa.

---

## 8. Tài liệu tham khảo (cập nhật 30/1/2026)

- [MediaWiki REST API – Get page](https://www.mediawiki.org/wiki/API:REST_API/Reference) — endpoint `rest.php/v1/page/{title}` (khuyến nghị thay Core REST API trước khi deprecation 7/2026).
- [Core REST API – Get page source](https://api.wikimedia.org/wiki/Core_REST_API/Reference/Pages/Get_page_source) (Wikimedia; lưu ý lộ trình lỗi thời).
- [Gemini API – Models](https://ai.google.dev/gemini-api/docs/models) và [Gemini API docs](https://ai.google.dev/gemini-api/docs) (Google AI for Developers).
- [Wikipedia:Quy định biên tập](https://vi.wikipedia.org/wiki/Wikipedia:Quy_định_biên_tập) (Wikipedia tiếng Việt).
- Mẫu wikitext tham chiếu: [vi-du.md](./vi-du.md).
