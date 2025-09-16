#!/usr/bin/env python3
"""
Image Generator Module using Google Gemini API

This module provides functionality to generate images using Google's Gemini AI model.
"""

import base64
import mimetypes
import os
import time
import re
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


def extract_retry_delay(error_message):
    """
    Extract retry delay from error message.
    
    Args:
        error_message (str): The error message from the API
        
    Returns:
        int: Retry delay in seconds, or 60 if not found
    """
    match = re.search(r"'retryDelay': '(\d+)s'", str(error_message))
    if match:
        return int(match.group(1))
    return 60  # Default to 60 seconds if not found


def generate_image(prompt="Generate an image of a banana wearing a costume.", output_prefix="generated_image", max_retries=3):
    """
    Generate an image using Google Gemini AI with retry logic for quota limits.
    
    Args:
        prompt (str): The text prompt for image generation
        output_prefix (str): Prefix for the output file name
        max_retries (int): Maximum number of retry attempts
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
    
    for attempt in range(max_retries + 1):
        try:
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
            return  # Success, exit function
            
        except Exception as e:
            error_str = str(e)
            
            # Check if it's a quota/rate limit error
            if "429" in error_str and "RESOURCE_EXHAUSTED" in error_str:
                if attempt < max_retries:
                    retry_delay = extract_retry_delay(error_str)
                    print(f"⚠️  Quota limit reached. Waiting {retry_delay} seconds before retry {attempt + 1}/{max_retries}...")
                    time.sleep(retry_delay)
                    continue
                else:
                    print("❌ Maximum retries reached. Quota limits exceeded.")
                    print("\n💡 Solutions to try:")
                    print("1. Wait a few minutes/hours for quota to reset")
                    print("2. Check your Google Cloud billing and upgrade if needed")
                    print("3. Try using a different model (gemini-1.5-flash)")
                    print("4. Use the Gemini API web interface instead")
                    print("5. Check quota limits at: https://ai.google.dev/gemini-api/docs/rate-limits")
                    raise
            else:
                # Re-raise non-quota errors immediately
                raise


def generate_text_description(prompt="Generate an image of a banana wearing a costume."):
    """
    Generate a detailed text description when image generation is not available.
    
    Args:
        prompt (str): The text prompt for description generation
    """
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY environment variable is not set.")
    
    client = genai.Client(api_key=api_key)
    
    # Use text-only model as fallback
    model = "gemini-1.5-flash"
    enhanced_prompt = f"Create a detailed visual description for this image prompt: '{prompt}'. Describe colors, composition, style, lighting, and artistic details as if you were describing a real image."
    
    contents = [
        types.Content(
            role="user",
            parts=[
                types.Part.from_text(text=enhanced_prompt),
            ],
        ),
    ]
    
    print(f"🎨 Generating detailed description for: '{prompt}'")
    print("📝 Since image generation is unavailable, here's a detailed visual description:\n")
    
    response = client.models.generate_content(
        model=model,
        contents=contents,
    )
    
    if response.text:
        print(response.text)
        print(f"\n💾 You can use this description with other AI image generators like:")
        print("- DALL-E (OpenAI)")
        print("- Midjourney")
        print("- Stable Diffusion")
        print("- Adobe Firefly")


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
        error_str = str(e)
        if "429" in error_str and "RESOURCE_EXHAUSTED" in error_str:
            print(f"\n🔄 Trying alternative: generating detailed text description instead...")
            try:
                # Try to generate a detailed description as fallback
                prompt = "Generate an image of a banana wearing a costume."  # Default prompt
                generate_text_description(prompt)
            except Exception as fallback_error:
                print(f"❌ Fallback also failed: {fallback_error}")
                print("\n⏰ Please try again later when quota resets.")
        else:
            print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
