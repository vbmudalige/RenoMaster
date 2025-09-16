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

from image_generator import generate_image, transform_room_image


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
        
        # Choose between image generation and room transformation
        print("\n🎨 Choose your AI image task:")
        print("1. Generate new images from text prompts")
        print("2. Transform room image with IKEA furniture (requires before.jpg)")
        
        choice = input("Enter your choice (1 or 2): ").strip()
        
        if choice == "2":
            # Room transformation mode
            input_file = "before.jpg"
            if not os.path.exists(input_file):
                print(f"❌ {input_file} not found in the project directory!")
                print("Please add your room image as 'before.jpg' and try again.")
                return
            
            print(f"\n🏠 Transforming {input_file} into a modern living room with IKEA furniture...")
            
            # Custom prompt for IKEA transformation
            style_prompt = ("Transform this room into a modern, stylish living room using IKEA furniture "
                          "available in Australia. Include contemporary IKEA sofas, coffee tables, "
                          "storage solutions, lighting, and decorative accessories. Make it look "
                          "clean, minimalist, and inviting with a Scandinavian design aesthetic.")
            
            try:
                result_file = transform_room_image(
                    input_image_path=input_file,
                    output_prefix="ikea_transformed",
                    style_prompt=style_prompt
                )
                print(f"\n✅ Room transformation completed!")
                if result_file:
                    print(f"📁 Transformed image saved as: {result_file}")
            except FileNotFoundError as e:
                print(f"❌ Error: {e}")
            except Exception as e:
                print(f"❌ Transformation failed: {e}")
                
        else:
            # Original image generation mode
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
