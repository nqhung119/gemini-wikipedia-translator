"""
Tách wikitext thành các block (theo section ==...== hoặc kích thước tối đa) để dịch từng phần.
Tham chiếu: docs/ke-hoach.md § 5.3, docs/nghien-cuu.md § 4.
"""
import re


def chunk_wikitext(
    wikitext: str,
    *,
    max_chars: int = 100_000,
) -> list[str]:
    """
    Tách wikitext thành danh sách block (list[str]) theo section và/hoặc max_chars.

    - Ưu tiên cắt theo tiêu đề section (==...== hoặc ===...===).
    - Nếu một section (hoặc phần mở đầu) dài hơn max_chars thì cắt thêm theo max_chars (ưu tiên cắt tại xuống dòng).
    - Thứ tự các block giữ nguyên so với wikitext gốc.
    - max_chars mặc định 100k để tránh quá tải API và mất nội dung.
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

    # Gộp các section liên tiếp thành chunk cho đến khi gần đạt max_chars (tránh quá nhiều chunk).
    # Nếu một phần đơn lẻ dài hơn max_chars thì cắt theo max_chars.
    result: list[str] = []
    current: list[str] = []
    current_len = 0
    for part in parts:
        if len(part) > max_chars:
            if current:
                result.append("\n\n".join(current))
                current = []
                current_len = 0
            result.extend(_split_by_size(part, max_chars))
        else:
            need = len(part) + (2 if current else 0)  # \n\n giữa các phần
            if current_len + need > max_chars and current:
                result.append("\n\n".join(current))
                current = [part]
                current_len = len(part)
            else:
                current.append(part)
                current_len += need
    if current:
        result.append("\n\n".join(current))
    return result


def _split_by_size(text: str, max_chars: int) -> list[str]:
    """Cắt text thành các đoạn <= max_chars, ưu tiên cắt tại xuống dòng, rồi tại khoảng trắng."""
    if len(text) <= max_chars:
        return [text]
    chunks: list[str] = []
    start = 0
    while start < len(text):
        end = min(start + max_chars, len(text))
        if end < len(text):
            chunk = text[start:end]
            # Ưu tiên 1: cắt tại xuống dòng (trong nửa sau của chunk)
            last_newline = chunk.rfind("\n")
            if last_newline > max_chars // 2:
                end = start + last_newline + 1
            else:
                # Ưu tiên 2: cắt tại khoảng trắng để tránh cắt giữa từ
                last_space = chunk.rfind(" ")
                if last_space > max_chars // 2:
                    end = start + last_space + 1
                # Nếu không có newline/space trong nửa sau thì cắt cứng tại max_chars
        chunks.append(text[start:end].strip())
        start = end
    return [c for c in chunks if c]
