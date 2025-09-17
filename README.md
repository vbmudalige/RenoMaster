# AI Image Transformer

Transform images using Google Gemini AI via a simple REST API.

## Features

- 🎨 **AI Image Transformation** - Transform images with text prompts using Google Gemini
- 🌐 **REST API** - Simple HTTP endpoints for easy integration
- 📱 **Interactive Docs** - Built-in Swagger UI for testing
- 🔧 **Easy Setup** - Minimal configuration required

## Quick Start

### 1. Installation

```bash
# Clone the repository
git clone https://github.com/vbmudalige/RenoMaster.git
cd RenoMaster

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Setup API Key

Get your Google Gemini API key from [Google AI Studio](https://aistudio.google.com/app/apikey)

```bash
export GEMINI_API_KEY='your-api-key-here'
```

### 3. Run the API

```bash
python api.py
```

The API will be available at `http://localhost:8000`

## API Usage

### Transform Image

**Endpoint:** `POST /transform`

**Parameters:**
- `image` (file): Input image to transform
- `prompt` (text): Transformation description

**Example with curl:**
```bash
curl -X POST "http://localhost:8000/transform" \
  -F "image=@your-image.jpg" \
  -F "prompt=Transform this into a modern living room" \
  --output result.png
```

**Example with Python:**
```python
import requests

with open('input.jpg', 'rb') as f:
    response = requests.post(
        'http://localhost:8000/transform',
        files={'image': f},
        data={'prompt': 'Transform into modern living room'}
    )

with open('output.png', 'wb') as f:
    f.write(response.content)
```

### Health Check

**Endpoint:** `GET /health`

Check API status and configuration.

## Interactive Documentation

Visit `http://localhost:8000/docs` for interactive API documentation where you can:
- Upload images directly
- Test different prompts
- Download results

## Example Prompts

- "Transform this into a modern living room using IKEA furniture"
- "Convert to a minimalist bedroom with white furniture"
- "Make this a cozy coffee shop interior"
- "Transform into a professional office space"

## Project Structure

```
├── api.py                 # FastAPI application
├── main.py               # CLI version (optional)
├── src/
│   └── image_generator.py # Core transformation logic
├── requirements.txt      # Dependencies
└── README.md            # This file
```

## Dependencies

- `google-genai` - Google Gemini AI SDK
- `fastapi` - Web framework
- `uvicorn` - ASGI server
- `python-multipart` - File upload support
- `pillow` - Image processing

## License

Open source project.

---

**Happy Transforming! 🎨✨**