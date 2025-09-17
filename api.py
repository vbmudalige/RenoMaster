import os
import tempfile
from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.responses import FileResponse
import sys

# Add src directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from image_generator import transform_image

app = FastAPI(title="AI Image Transformer", version="1.0.0")


@app.get("/")
async def root():
    """Health check endpoint."""
    return {"message": "AI Image Transformer API is running"}


@app.post("/transform")
async def transform_image_endpoint(
    image: UploadFile = File(..., description="Input image file"),
    prompt: str = Form(..., description="Transformation prompt")
):
    """Transform an image using AI with the given prompt."""
    
    # Validate file type
    if not image.content_type.startswith('image/'):
        raise HTTPException(status_code=400, detail="File must be an image")
    
    # Create temporary files
    with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as temp_input:
        # Save uploaded image
        content = await image.read()
        temp_input.write(content)
        temp_input_path = temp_input.name
    
    try:
        # Transform the image
        transform_image(temp_input_path, prompt)
        
        # Check if output file exists
        if not os.path.exists("after.png"):
            raise HTTPException(status_code=500, detail="Image transformation failed")
        
        # Return the transformed image
        return FileResponse(
            "after.png",
            media_type="image/png",
            filename="transformed_image.png"
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Transformation error: {str(e)}")
    
    finally:
        # Clean up temporary input file
        if os.path.exists(temp_input_path):
            os.unlink(temp_input_path)


@app.get("/health")
async def health_check():
    """Check if the API and dependencies are working."""
    try:
        # Check if GEMINI_API_KEY is set
        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key:
            return {"status": "error", "message": "GEMINI_API_KEY not set"}
        
        return {"status": "healthy", "message": "All systems operational"}
    
    except Exception as e:
        return {"status": "error", "message": f"Health check failed: {str(e)}"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
