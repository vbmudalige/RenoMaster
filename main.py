import sys
import os

# Add src directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

# Import after path modification
from image_generator import transform_image  # noqa: E402


def main():
    """Main function to run image transformation."""
    # Get user inputs
    image_name = input("Enter image name: ")
    prompt = input("Enter prompt: ")

    # Transform image and handle errors
    try:
        transform_image(image_name, prompt)
        print("Image saved as after.png")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
