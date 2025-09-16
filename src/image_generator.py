import mimetypes
import os
from google import genai
from google.genai import types

def transform_image(input_image_path, prompt):
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY not set")
    
    with open(input_image_path, "rb") as f:
        image_data = f.read()
    
    mime_type, _ = mimetypes.guess_type(input_image_path)
    if not mime_type or not mime_type.startswith('image/'):
        mime_type = 'image/jpeg'
    
    client = genai.Client(api_key=api_key)
    model = "gemini-2.5-flash-image-preview"
    
    contents = [
        types.Content(
            role="user",
            parts=[
                types.Part(
                    inline_data=types.Blob(
                        mime_type=mime_type,
                        data=image_data
                    )
                ),
                types.Part.from_text(text=prompt),
            ],
        ),
    ]
    
    generate_content_config = types.GenerateContentConfig(
        response_modalities=["IMAGE", "TEXT"],
    )

    for chunk in client.models.generate_content_stream(
        model=model,
        contents=contents,
        config=generate_content_config,
    ):
        if (chunk.candidates and 
            chunk.candidates[0].content and 
            chunk.candidates[0].content.parts):
            
            part = chunk.candidates[0].content.parts[0]
            
            if hasattr(part, 'inline_data') and part.inline_data and part.inline_data.data:
                with open("after.png", "wb") as f:
                    f.write(part.inline_data.data)
                return
