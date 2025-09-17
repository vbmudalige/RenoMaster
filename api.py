import os
import sys
import tempfile
from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.responses import FileResponse

# Add src directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

# Import after path modification
from image_generator import transform_image  # noqa: E402

app = FastAPI(title="AI Image Transformer", version="1.0.0")


@app.get("/")
def root():
    """API status endpoint."""
    return {"message": "AI Image Transformer API", "status": "running"}


@app.post("/transform")
async def transform_image_api(
    image: UploadFile = File(...),
    prompt: str = Form(...)
):
    """Transform image with AI using text prompt."""

    # Validate image file
    if not image.content_type.startswith('image/'):
        raise HTTPException(400, "File must be an image")

    # Save uploaded image temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as temp_file:
        content = await image.read()
        temp_file.write(content)
        temp_path = temp_file.name

    try:
        # Transform image
        transform_image(temp_path, prompt)

        # Return transformed image
        if os.path.exists("after.png"):
            return FileResponse("after.png", media_type="image/png")
        else:
            raise HTTPException(500, "Transformation failed")

    except Exception as e:
        raise HTTPException(500, f"Error: {str(e)}")

    finally:
        # Cleanup
        if os.path.exists(temp_path):
            os.unlink(temp_path)


@app.get("/health")
def health():
    """Health check endpoint."""
    api_key = os.environ.get("GEMINI_API_KEY")
    status = "healthy" if api_key else "error"
    message = "Ready" if api_key else "GEMINI_API_KEY not set"
    return {"status": status, "message": message}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
