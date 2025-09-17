import mimetypes
import os
from google import genai
from google.genai import types


def transform_image(input_path, prompt):
    """Transform image using Google Gemini AI."""

    # Check API key
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY not set")

    # Read image
    with open(input_path, "rb") as f:
        image_data = f.read()

    # Get MIME type
    mime_type, _ = mimetypes.guess_type(input_path)
    if not mime_type or not mime_type.startswith('image/'):
        mime_type = 'image/jpeg'

    # Setup client
    client = genai.Client(api_key=api_key)

    # Create request
    contents = [types.Content(
        role="user",
        parts=[
            types.Part(inline_data=types.Blob(
                mime_type=mime_type, data=image_data)),
            types.Part.from_text(text=prompt),
        ],
    )]

    config = types.GenerateContentConfig(response_modalities=["IMAGE", "TEXT"])

    # Generate and save
    for chunk in client.models.generate_content_stream(
        model="gemini-2.5-flash-image-preview",
        contents=contents,
        config=config,
    ):
        if (chunk.candidates and chunk.candidates[0].content and
                chunk.candidates[0].content.parts):

            part = chunk.candidates[0].content.parts[0]

            if (hasattr(part, 'inline_data') and part.inline_data and
                    part.inline_data.data):
                with open("after.png", "wb") as f:
                    f.write(part.inline_data.data)
                return
