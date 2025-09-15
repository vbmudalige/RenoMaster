#!/usr/bin/env python3
"""
Hackathon Project - Main Entry Point

This is the main entry point for the hackathon project.
Features Google Gemini AI image generation capabilities.
"""

import sys
import os

# Add src directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from image_generator import generate_image


def main():
    """Main function to run the hackathon project."""
    print("Welcome to the Hackathon Project!")
    print("🎨 AI Image Generator powered by Google Gemini")
    print("-" * 50)
    
    try:
        # Check if API key is available
        if not os.environ.get("GEMINI_API_KEY"):
            print("⚠️  GEMINI_API_KEY environment variable not found!")
            print("\nTo get started:")
            print("1. Get your API key from Google AI Studio")
            print("2. Set the environment variable:")
            print("   export GEMINI_API_KEY='your-api-key-here'")
            print("3. Run the program again")
            return
        
        # Get user input for image generation
        print("\n🤖 Let's generate some AI images!")
        prompt = input("Enter your image prompt (or press Enter for default): ").strip()
        
        if not prompt:
            prompt = "Generate an image of a banana wearing a costume."
            print(f"Using default prompt: {prompt}")
        
        # Generate the image
        generate_image(prompt=prompt, output_prefix="hackathon_generated")
        print("\n✅ Image generation completed!")
        
    except KeyboardInterrupt:
        print("\n\n👋 Thanks for using the AI Image Generator!")
    except Exception as e:
        print(f"\n❌ An error occurred: {e}")


if __name__ == "__main__":
    main()
