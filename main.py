from fastapi import FastAPI
from pydantic import BaseModel
import base64
import io
import zipfile
from PIL import Image

app = FastAPI()

class RenderRequest(BaseModel):
    filename: str
    content_type: str
    file_base64: str
    language: str

@app.post("/render")
async def render_file(req: RenderRequest):

    # STEP 1 — Decode base64 input
    try:
        input_bytes = base64.b64decode(req.file_base64)
    except Exception:
        return {
            "status": "error",
            "message": "Invalid Base64 input"
        }

    # STEP 2 — Load file (image or doc)
    file_stream = io.BytesIO(input_bytes)

    # Example: open image for processing
    try:
        img = Image.open(file_stream)
    except:
        return {
            "status": "error",
            "message": "Unable to load file. Only images allowed in demo."
        }

    # STEP 3 — *** YOUR RENDER LOGIC HERE ***
    # Demonstration: convert image to grayscale
    rendered_img = img.convert("L")

    # STEP 4 — Create ZIP in memory
    zip_buffer = io.BytesIO()

    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zipf:
        buf = io.BytesIO()
        rendered_img.save(buf, format="JPEG")
        zipf.writestr("rendered_" + req.filename, buf.getvalue())

    zip_bytes = zip_buffer.getvalue()

    # STEP 5 — Return Base64 ZIP
    zip_b64 = base64.b64encode(zip_bytes).decode()

    return {
        "status": "success",
        "output_zip_base64": zip_b64
    }
