import io
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import Response
from PIL import Image
from rembg import remove

app = FastAPI()

@app.get("/")
def home():
    return {"status": "Server is running successfully!"}

@app.post("/remove-bg")
async def remove_background(file: UploadFile = File(...)):
    try:
        # خواندن بایت‌های عکس ارسالی از سمت اپلیکیشن اندروید
        image_bytes = await file.read()
        
        # باز کردن تصویر با کتابخانه Pillow
        input_image = Image.open(io.BytesIO(image_bytes))
        
        # حذف پس‌زمینه با استفاده از rembg
        output_image = remove(input_image)
        
        # ذخیره خروجی به صورت بایت در فرمت PNG
        output_buffer = io.BytesIO()
        output_image.save(output_buffer, format="PNG")
        output_buffer.seek(0)
        
        # بازگرداندن تصویر پردازش‌شده به اپلیکیشن
        return Response(content=output_buffer.getvalue(), media_type="image/png")
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
