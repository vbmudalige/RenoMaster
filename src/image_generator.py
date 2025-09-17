import mimetypes
import os
from google import genai
from google.genai import types


def transform_image(input_path, prompt):
    """Transform image using Google Gemini AI with renovation report."""

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

    # Create enhanced prompt with system instructions
    system_prompt = """You are an expert architect and interior designer with a strong understanding of human psychology, mood, and behavior in interior spaces. You specialize in renovating and decorating existing rooms while respecting their structure and perspective. Thus not changing the building itself of the given image.

Your task is to:
- Take an input image of an empty room
- Renovate and decorate it according to the given style
- Do not alter the dimensions, walls, or perspective of the room
- Only apply surface and decorative changes (paint, textures, flooring, lighting, furniture, décor)

Produce a renovation report with:
1. List of all changes made (walls, floor, ceiling, furniture, décor, lighting)
2. For each item: description, psychology/mood effect, Australian retail options (Bunnings, Temple & Webster, Freedom, Harvey Norman, IKEA)
3. Labour requirements: tradesperson type (painter, carpenter, handyman, electrician, tiler)
4. Estimated cost breakdown: item cost + labour cost

User request: """ + prompt

    # Create request
    contents = [types.Content(
        role="user",
        parts=[
            types.Part(inline_data=types.Blob(
                mime_type=mime_type, data=image_data)),
            types.Part.from_text(text=system_prompt),
        ],
    )]

    config = types.GenerateContentConfig(response_modalities=["IMAGE", "TEXT"])

    renovation_report = ""
    image_saved = False

    # Generate and save
    for chunk in client.models.generate_content_stream(
        model="gemini-2.5-flash-image-preview",
        contents=contents,
        config=config,
    ):
        if (chunk.candidates and chunk.candidates[0].content and
                chunk.candidates[0].content.parts):

            part = chunk.candidates[0].content.parts[0]

            # Save image if available
            if (hasattr(part, 'inline_data') and part.inline_data and
                    part.inline_data.data and not image_saved):
                with open("after.png", "wb") as f:
                    f.write(part.inline_data.data)
                image_saved = True

            # Collect text response
            if hasattr(part, 'text') and part.text:
                renovation_report += part.text

    return renovation_report
