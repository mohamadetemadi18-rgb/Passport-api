from fastapi import FastAPI, File, UploadFile
from fastapi.responses import Response
from PIL import Image
from rembg import remove
import io

app = FastAPI()

@app.post("/remove-bg")
async def remove_background(file: UploadFile = File(...)):
    image_bytes = await file.read()
    input_image = Image.open(io.BytesIO(image_bytes))
    
    # حذف پس‌زمینه با هوش مصنوعی
    output_image = remove(input_image)
    
    # آماده‌سازی خروجی عکس
    output_buffer = io.BytesIO()
    output_image.save(output_buffer, format="PNG")
    output_buffer.seek(0)
    
    return Response(content=output_buffer.getvalue(), media_type="image/png")

@app.get("/")
async def root():
    return {"status": "Passport Studio API is running!"}
