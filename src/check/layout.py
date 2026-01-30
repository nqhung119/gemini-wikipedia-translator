"""
Kiểm tra bố cục wikitext: cân bằng [[ ]], {{ }}, <ref> </ref>; có {{reflist}}.
Tham chiếu: docs/nghien-cuu.md § 5.1, docs/ke-hoach.md § 5.4.
"""
import re


def check_layout(wikitext: str) -> list[str]:
    """
    Kiểm tra bố cục wikitext, trả về danh sách cảnh báo (list[str]).
    - Đếm/cân bằng [[, ]], {{, }}, <ref, </ref>
    - Cảnh báo nếu có <ref> nhưng không có {{reflist}} (hoặc tương đương)
    """
    if not (wikitext or "").strip():
        return ["Wikitext trống."]

    warnings: list[str] = []
    s = wikitext

    # Link nội bộ [[ ... ]]
    link_open = s.count("[[")
    link_close = s.count("]]")
    if link_open != link_close:
        warnings.append(
            f"Cảnh báo bố cục: Số [[ ({link_open}) khác số ]] ({link_close})."
        )

    # Template {{ ... }}
    template_open = s.count("{{")
    template_close = s.count("}}")
    if template_open != template_close:
        warnings.append(
            f"Cảnh báo bố cục: Số {{ ({template_open}) khác số }} ({template_close})."
        )

    # Chú thích <ref> ... </ref>
    ref_open = s.count("<ref")
    ref_close = s.count("</ref>")
    if ref_open > 0:
        if ref_close > ref_open:
            warnings.append(
                f"Cảnh báo bố cục: Số </ref> ({ref_close}) nhiều hơn số <ref ({ref_open})."
            )
        elif ref_open > ref_close:
            self_closing = len(re.findall(r"<ref[^>]*/>", s))
            if ref_open - ref_close != self_closing:
                warnings.append(
                    f"Cảnh báo bố cục: Số <ref ({ref_open}) nhiều hơn </ref> ({ref_close}); "
                    "có thể thiếu đóng thẻ hoặc dùng <ref ... />."
                )
        # Có <ref> thì nên có {{reflist}} hoặc {{Reflist}}
        if "reflist" not in s.lower():
            warnings.append(
                "Cảnh báo bố cục: Có <ref> nhưng không tìm thấy {{reflist}} (hoặc {{Reflist}})."
            )

    if not warnings:
        warnings.append("Không phát hiện lỗi bố cục ([[ ]], {{ }}, <ref>).")

    return warnings
