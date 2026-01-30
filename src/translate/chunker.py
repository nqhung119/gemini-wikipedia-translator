"""
Tách wikitext thành các block (theo section ==...== hoặc kích thước tối đa) để dịch từng phần.
Tham chiếu: docs/ke-hoach.md § 5.3, docs/nghien-cuu.md § 4.
"""
import re


def chunk_wikitext(
    wikitext: str,
    *,
    max_chars: int = 50000,
) -> list[str]:
    """
    Tách wikitext thành danh sách block (list[str]) theo section và/hoặc max_chars.

    - Ưu tiên cắt theo tiêu đề section (==...== hoặc ===...===).
    - Nếu một section (hoặc phần mở đầu) dài hơn max_chars thì cắt thêm theo max_chars (ưu tiên cắt tại xuống dòng).
    - Thứ tự các block giữ nguyên so với wikitext gốc.
    """
    if not (wikitext or "").strip():
        return []

    text = wikitext.strip()
    if len(text) <= max_chars:
        return [text]

    # Tìm vị trí các dòng section: ==Title== hoặc == Title ==
    section_pattern = re.compile(r"^=+\s*.+\s*=+\s*$", re.MULTILINE)
    matches = list(section_pattern.finditer(text))
    if not matches:
        # Không có section → cắt theo max_chars
        return _split_by_size(text, max_chars)

    # Xây danh sách "phần": từ start đến đầu section tiếp theo (hoặc hết)
    parts: list[str] = []
    for i, m in enumerate(matches):
        start = m.start()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        part = text[start:end].strip()
        if part:
            parts.append(part)

    # Phần mở đầu (trước section đầu tiên)
    first_section_start = matches[0].start()
    if first_section_start > 0:
        intro = text[:first_section_start].strip()
        if intro:
            parts.insert(0, intro)

    # Nếu phần nào dài hơn max_chars thì cắt nhỏ theo max_chars
    result: list[str] = []
    for part in parts:
        if len(part) <= max_chars:
            result.append(part)
        else:
            result.extend(_split_by_size(part, max_chars))
    return result


def _split_by_size(text: str, max_chars: int) -> list[str]:
    """Cắt text thành các đoạn <= max_chars, ưu tiên cắt tại xuống dòng."""
    if len(text) <= max_chars:
        return [text]
    chunks: list[str] = []
    start = 0
    while start < len(text):
        end = min(start + max_chars, len(text))
        if end < len(text):
            # Tìm vị trí xuống dòng gần end nhất
            chunk = text[start:end]
            last_newline = chunk.rfind("\n")
            if last_newline > max_chars // 2:
                end = start + last_newline + 1
        chunks.append(text[start:end].strip())
        start = end
    return [c for c in chunks if c]
