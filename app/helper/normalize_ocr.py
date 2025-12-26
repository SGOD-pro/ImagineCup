from typing import Dict, Any, List, Optional



def normalize_ocr(raw_ocr: Dict[str, Any]) -> Dict[str, Any]:
    """
    Normalize both image OCR (Azure Vision) and PDF OCR (Document Intelligence)
    into ONE canonical OCR structure.
    """

    segments: List[Dict[str, Optional[str]]] = []

    # -------------------------
    # CASE 1: PDF OCR (Document Intelligence)
    # -------------------------
    if raw_ocr.get("source") == "pdf" and "pages" in raw_ocr:
        for page in raw_ocr["pages"]:
            page_number = page.get("page_number")
            lines = page.get("text", "").split("\n")

            for line in lines:
                line = line.strip()
                if not line:
                    continue

                segments.append({
                    "text": line,
                    "confidence": None,   # DI does not provide per-line confidence
                    "page": page_number
                })

        return {
            "source": "pdf",
            "full_text": raw_ocr.get("full_text", ""),
            "segments": segments
        }

    # -------------------------
    # CASE 2: IMAGE OCR (Azure Vision)
    # -------------------------
    if "ocr" in raw_ocr and "lines" in raw_ocr["ocr"]:
        for line in raw_ocr["ocr"]["lines"]:
            words = line.get("words", [])

            confidences = [
                w.get("confidence")
                for w in words
                if isinstance(w.get("confidence"), (int, float))
            ]

            avg_confidence = (
                round(sum(confidences) / len(confidences), 3)
                if confidences else None
            )

            text = line.get("text", "").strip()
            if not text:
                continue

            segments.append({
                "text": text,
                "confidence": f'{avg_confidence}',
                "page": None
            })

        return {
            "source": "image",
            "full_text": raw_ocr.get("ocr", {}).get("full_text", ""),
            "segments": segments
        }

    # -------------------------
    # FAIL FAST (IMPORTANT)
    # -------------------------
    raise ValueError("Unsupported OCR response format")
