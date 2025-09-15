# Hackathon Project - AI Image Generator

Welcome to your hackathon project! This is a Python-based AI image generator powered by Google Gemini API.

## Project Structure

```
hackathon/
├── main.py              # Main entry point
├── src/                 # Source code directory
├── tests/               # Test files
├── config/              # Configuration files
├── requirements.txt     # Project dependencies
├── requirements-dev.txt # Development dependencies
├── .gitignore          # Git ignore file
└── README.md           # This file
```

## Getting Started

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

### Installation

1. **Clone or navigate to the project directory:**
   ```bash
   cd hackathon
   ```

2. **Create a virtual environment (recommended):**
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment:**
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```

4. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

5. **Set up Google Gemini API:**
   - Get your API key from [Google AI Studio](https://aistudio.google.com/app/apikey)
   - Set the environment variable:
     ```bash
     export GEMINI_API_KEY='your-api-key-here'
     ```
   - On Windows:
     ```bash
     set GEMINI_API_KEY=your-api-key-here
     ```

6. **Install development dependencies (optional):**
   ```bash
   pip install -r requirements-dev.txt
   ```

### Running the Project

Run the AI image generator:
```bash
python main.py
```

The application will:
1. Check if your GEMINI_API_KEY is set
2. Prompt you to enter an image description
3. Generate an image using Google Gemini AI
4. Save the generated image to your project directory

### Features

- 🎨 **AI Image Generation**: Generate images from text prompts using Google Gemini
- 🔧 **Modular Design**: Clean separation of concerns with dedicated modules
- 🛡️ **Error Handling**: Comprehensive error handling and user guidance
- 📁 **File Management**: Automatic file saving with appropriate extensions

### Development

#### Code Formatting
```bash
black .
```

#### Linting
```bash
flake8 .
```

#### Type Checking
```bash
mypy .
```

#### Running Tests
```bash
pytest
```

## Project Structure Details

- **`main.py`**: The main entry point of your application
- **`src/`**: Place your main source code here
- **`tests/`**: Write your tests here
- **`config/`**: Configuration files and settings
- **`requirements.txt`**: List your project dependencies here
- **`requirements-dev.txt`**: Development tools and testing dependencies

## Contributing

1. Create a new branch for your feature
2. Make your changes
3. Run tests and linting
4. Create a pull request

## License

This project is open source. Add your license information here.

---

**Happy Hacking! 🚀**
