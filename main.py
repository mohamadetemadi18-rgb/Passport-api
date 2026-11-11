from rembg import remove, new_session

# ساختن یک نشست با مدل سبک‌تر (u2netp) که رم بسیار کمی مصرف می‌کند
session = new_session("u2netp")

@app.post("/remove-bg")
async def remove_background(file: UploadFile = File(...)):
    try:
        image_bytes = await file.read()
        input_image = Image.open(io.BytesIO(image_bytes))
        
        # استفاده از مدل سبک تعریف شده
        output_image = remove(input_image, session=session)
        
        output_buffer = io.BytesIO()
        output_image.save(output_buffer, format="PNG")
        output_buffer.seek(0)
        return Response(content=output_buffer.getvalue(), media_type="image/png")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
