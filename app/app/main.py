import os
import tempfile
from fastapi import FastAPI, UploadFile, File, Header, HTTPException
from fastapi.responses import JSONResponse

from app.parser import parse_pdf

SERVICE_TOKEN = os.getenv("SERVICE_TOKEN")

app = FastAPI(title="Budgi Unstructured Service", version="1.0.0")


@app.get("/healthz")
def healthz():
    return {"status": "ok"}


@app.post("/partition/pdf")
async def partition_pdf_endpoint(
    file: UploadFile = File(...),
    authorization: str | None = Header(default=None),
):
    # --- Auth ---
    if not SERVICE_TOKEN:
        raise HTTPException(status_code=500, detail="SERVICE_TOKEN not configured")

    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Unauthorized")

    token = authorization.replace("Bearer ", "").strip()
    if token != SERVICE_TOKEN:
        raise HTTPException(status_code=401, detail="Unauthorized")

    # --- Validate file ---
    if not file.filename.lower().endswith(".pdf"):
        return JSONResponse(
            status_code=400,
            content={
                "status": "error",
                "error_code": "INVALID_FILE",
                "message": "Only PDF files are supported",
            },
        )

    # --- Save temp file ---
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        content = await file.read()
        tmp.write(content)
        tmp_path = tmp.name

    # --- Parse ---
    try:
        elements = parse_pdf(tmp_path)
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "status": "error",
                "error_code": "PARSE_FAILED",
                "message": str(e),
            },
        )

    # --- Build response ---
    table_count = sum(
        1 for el in elements if el.get("type") == "Table"
    )
    page_numbers = {
        el.get("metadata", {}).get("page_number")
        for el in elements
        if el.get("metadata", {}).get("page_number") is not None
    }

    return {
        "status": "success",
        "strategy_used": os.getenv("UNSTRUCTURED_STRATEGY", "auto"),
        "page_count": len(page_numbers),
        "table_count": table_count,
        "elements": elements,
    }
