import mimetypes
import os
from google import genai
from google.genai import types


def transform_image(input_image_path, prompt):
    """Transform an image using Google Gemini AI with a text prompt."""
    # Get API key
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY not set")

    # Read input image
    with open(input_image_path, "rb") as f:
        image_data = f.read()

    # Determine MIME type
    mime_type, _ = mimetypes.guess_type(input_image_path)
    if not mime_type or not mime_type.startswith('image/'):
        mime_type = 'image/jpeg'

    # Initialize client and model
    client = genai.Client(api_key=api_key)
    model = "gemini-2.5-flash-image-preview"

    # Create request content with image and prompt
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

    # Configure response to include images
    generate_content_config = types.GenerateContentConfig(
        response_modalities=["IMAGE", "TEXT"],
    )

    # Process response and save image
    for chunk in client.models.generate_content_stream(
        model=model,
        contents=contents,
        config=generate_content_config,
    ):
        if (chunk.candidates and
                chunk.candidates[0].content and
                chunk.candidates[0].content.parts):
            part = chunk.candidates[0].content.parts[0]

            # Save generated image as after.png
            if (hasattr(part, 'inline_data') and
                    part.inline_data and part.inline_data.data):
                with open("after.png", "wb") as f:
                    f.write(part.inline_data.data)
                return
