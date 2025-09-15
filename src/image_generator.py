#!/usr/bin/env python3
"""
Image Generator Module using Google Gemini API

This module provides functionality to generate images using Google's Gemini AI model.
"""

import base64
import mimetypes
import os
from google import genai
from google.genai import types


def save_binary_file(file_name, data):
    """
    Save binary data to a file.
    
    Args:
        file_name (str): The name of the file to save
        data (bytes): The binary data to save
    """
    with open(file_name, "wb") as f:
        f.write(data)
    print(f"File saved to: {file_name}")


def generate_image(prompt="Generate an image of a banana wearing a costume.", output_prefix="generated_image"):
    """
    Generate an image using Google Gemini AI.
    
    Args:
        prompt (str): The text prompt for image generation
        output_prefix (str): Prefix for the output file name
    """
    # Check if API key is set
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise ValueError(
            "GEMINI_API_KEY environment variable is not set. "
            "Please set your Google Gemini API key."
        )
    
    client = genai.Client(api_key=api_key)

    model = "gemini-2.5-flash-image-preview"
    contents = [
        types.Content(
            role="user",
            parts=[
                types.Part.from_text(text=prompt),
            ],
        ),
    ]
    generate_content_config = types.GenerateContentConfig(
        response_modalities=[
            "IMAGE",
            "TEXT",
        ],
    )

    file_index = 0
    print(f"Generating image with prompt: '{prompt}'")
    
    for chunk in client.models.generate_content_stream(
        model=model,
        contents=contents,
        config=generate_content_config,
    ):
        if (
            chunk.candidates is None
            or chunk.candidates[0].content is None
            or chunk.candidates[0].content.parts is None
        ):
            continue
            
        if (chunk.candidates[0].content.parts[0].inline_data and 
            chunk.candidates[0].content.parts[0].inline_data.data):
            file_name = f"{output_prefix}_{file_index}"
            file_index += 1
            inline_data = chunk.candidates[0].content.parts[0].inline_data
            data_buffer = inline_data.data
            file_extension = mimetypes.guess_extension(inline_data.mime_type)
            save_binary_file(f"{file_name}{file_extension}", data_buffer)
        else:
            if hasattr(chunk, 'text') and chunk.text:
                print(chunk.text)


def main():
    """Main function to run image generation."""
    try:
        generate_image()
    except ValueError as e:
        print(f"Error: {e}")
        print("\nTo set up your API key:")
        print("1. Get your API key from Google AI Studio")
        print("2. Set the environment variable:")
        print("   export GEMINI_API_KEY='your-api-key-here'")
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
