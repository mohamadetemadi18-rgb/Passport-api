import io
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import Response
from PIL import Image
from rembg import remove, new_session

app = FastAPI()

# لود کردن مدل سبک برای جلوگیری از خطای حافظه
session = new_session("u2netp")

@app.get("/")
def home():
    return {"status": "Server is running successfully!"}

@app.post("/remove-bg")
async def remove_background(file: UploadFile = File(...)):
    try:
        image_bytes = await file.read()
        input_image = Image.open(io.BytesIO(image_bytes))
        
        # پردازش و حذف پس‌زمینه
        output_image = remove(input_image, session=session)
        
        output_buffer = io.BytesIO()
        output_image.save(output_buffer, format="PNG")
        output_buffer.seek(0)
        
        return Response(content=output_buffer.getvalue(), media_type="image/png")
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
