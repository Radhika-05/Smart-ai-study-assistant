"""
OCR Service — uses the official glmocr SDK with Zhipu MaaS cloud API.

No GPU or local model needed. The SDK sends images to open.bigmodel.cn
and returns structured OCR results.

SDK docs: https://github.com/zai-org/GLM-OCR
Get API key: https://open.bigmodel.cn (free tier available)
"""

import os
import tempfile
from pathlib import Path
from PIL import Image

# Lazy-loaded SDK client
_parser = None

# Path to the glmocr config file shipped with this project
CONFIG_PATH = Path(__file__).parent.parent / "glmocr_config.yaml"


def load_ocr_model(api_key: str | None = None) -> None:
    """
    Initialise the glmocr SDK client (cloud/MaaS mode).
    Safe to call multiple times — only initialises once per session.

    Args:
        api_key: Zhipu API key. Falls back to ZHIPU_API_KEY env variable.

    Raises:
        RuntimeError: If the SDK cannot be initialised.
    """
    global _parser
    if _parser is not None:
        return

    resolved_key = api_key or os.getenv("ZHIPU_API_KEY", "")
    if not resolved_key:
        raise ValueError(
            "Zhipu API key is missing. Add ZHIPU_API_KEY to your .env file "
            "or enter it in the sidebar."
        )

    # Inject key via the env var the SDK reads
    os.environ["API_KEY"] = resolved_key

    try:
        from glmocr import GlmOcr
        _parser = GlmOcr(config_path=str(CONFIG_PATH))
    except Exception as e:
        _parser = None
        raise RuntimeError(f"Failed to initialise glmocr SDK: {e}") from e


def is_model_loaded() -> bool:
    """Returns True once the SDK client has been initialised."""
    return _parser is not None


def extract_text_from_image(
    image: Image.Image,
    api_key: str | None = None,
) -> str:
    """
    Send a PIL image to GLM-OCR (cloud) and return extracted plain text.

    The function saves the image to a temp file, calls the glmocr SDK,
    then assembles plain text from the structured JSON result.

    Args:
        image:   PIL Image — any mode, converted to RGB internally.
        api_key: Zhipu API key (used on first call to init the client).

    Returns:
        Extracted text string. Empty string if nothing was detected.

    Raises:
        ValueError:  If the API key is missing.
        RuntimeError: If the SDK call fails.
    """
    # Initialise client if needed (picks up api_key on first call)
    if not is_model_loaded():
        load_ocr_model(api_key=api_key)

    if image.mode != "RGB":
        image = image.convert("RGB")

    tmp_path = None
    try:
        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
            tmp_path = tmp.name
            image.save(tmp_path, format="PNG")

        with _parser as ocr:
            result = ocr.parse(tmp_path)

        return _extract_plain_text(result)

    except Exception as e:
        raise RuntimeError(f"GLM-OCR inference failed: {e}") from e
    finally:
        if tmp_path and os.path.exists(tmp_path):
            os.remove(tmp_path)


def _extract_plain_text(result) -> str:
    """
    Pull plain text out of a glmocr result object.

    The result has:
      result.json_result  →  list[list[dict]]  (pages → elements)
        element keys: index, label, content, bbox_2d

    Labels of interest: "text", "formula"
    Labels to skip:     "image", "table" (keep table as-is if present)
    """
    try:
        pages = result.json_result  # list of pages
    except AttributeError:
        pages = []

    parts = []
    for page in pages:
        for element in page:
            label = element.get("label", "")
            content = element.get("content", "").strip()
            if content and label in ("text", "formula", "table"):
                parts.append(content)

    text = "\n\n".join(parts)

    # Fallback: try markdown attribute if json_result was empty
    if not text.strip():
        try:
            md = getattr(result, "markdown", "") or ""
            text = md.strip()
        except Exception:
            pass

    return text.strip()
