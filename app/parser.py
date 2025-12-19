import os
from typing import List, Dict, Any

from unstructured.partition.pdf import partition_pdf


DEFAULT_STRATEGY = os.getenv("UNSTRUCTURED_STRATEGY", "auto")
ENABLE_VLM = os.getenv("ENABLE_VLM", "false").lower() == "true"


def parse_pdf(
    file_path: str,
    strategy: str | None = None
) -> List[Dict[str, Any]]:
    """
    Parse a PDF using Unstructured OSS.
    - strategy defaults to env UNSTRUCTURED_STRATEGY (auto)
    - VLM is explicitly disabled in Phase 1
    """
    used_strategy = strategy or DEFAULT_STRATEGY

    if ENABLE_VLM:
        # Guardrail: VLM must never be active in Phase 1
        raise RuntimeError("VLM is disabled in Phase 1")

    elements = partition_pdf(
        filename=file_path,
        strategy=used_strategy,
    )

    # Return raw element dicts (no Budgi logic)
    return [el.to_dict() for el in elements]
