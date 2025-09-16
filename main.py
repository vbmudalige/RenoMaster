import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from image_generator import transform_image

def main():
    image_name = input("Enter image name: ")
    prompt = input("Enter prompt: ")
    
    try:
        transform_image(image_name, prompt)
        print("Image saved as after.png")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
