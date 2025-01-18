from flask import Flask, render_template, request
import pytesseract
import re
from PIL import Image
import os

app = Flask(__name__)

# Define normal ranges for blood cell counts (customizable)
normal_ranges = {
    "WBC Count": {"min": 4000, "max": 11000},
    "RBC Count": {"min": 4.5, "max": 5.5},
    "RDW-CV": {"min": 11.6, "max": 14.6},
    "HCT": {"min": 36, "max": 46},
    "MCH": {"min": 26, "max": 32},
    "Hb (Hemoglobin)": {"min": 11, "max": 16},
    "MCHC": {"min": 30, "max": 35},
    "Platelet Count": {"min": 150000, "max": 410000},
}


def load_image(image_path):
    """Loads an image from the specified path."""
    try:
        image = Image.open(image_path)
        return image
    except Exception as e:
        print("Error loading image:", e)
        return None


def preprocess_image(image):
    """Preprocesses the image for better text extraction (optional)."""
    # You can add grayscale conversion, noise reduction, etc. here
    return image


def extract_text(image):
    """Extracts text from the image using Tesseract OCR."""
    if image:
        try:
            text = pytesseract.image_to_string(preprocess_image(image))
            return text
        except Exception as e:
            print("Error during text extraction:", e)
            return None
    else:
        return None


def extract_parameter_value(text, parameter_name):
    """Extracts the value for a specific parameter from the text."""
    regex = r"\b(\d{1,3}(?:,\d{3})*(?:\.\d+)?)\b"
    for line in text.split('\n'):
        if parameter_name.lower() in line.lower():
            matches = re.findall(regex, line)
            if matches:
                parameter_value = matches[0].replace(',', '')  # Remove commas
                return parameter_value
    return None


def analyze_parameters(extracted_text):
    """Analyzes extracted text and compares values with normal ranges."""
    found_any_param = False
    for param_name, param_info in normal_ranges.items():
        param_value = extract_parameter_value(extracted_text, param_name)
        if param_value:
            found_any_param = True
            try:
                count = float(param_value)
                if param_info["min"] <= count <= param_info["max"]:
                    print(f"{param_name} is within normal range:", count)
                else:
                    print(f"{param_name} is abnormal. Value:", count)
            except ValueError:
                print(f"Error: Invalid {param_name} value:", param_value)
    if not found_any_param:
        print("Please Enter a Valid CBC report.")


@app.route("/", methods=["GET", "POST"])
def analyze_report():
    """Handles file upload and analysis."""
    if request.method == "POST":
        image_file = request.files.get("report_image")
        if image_file:
            image = load_image(image_file.filename)
            if image:
                extracted_text = extract_text(image)
                if extracted_text:
                    analyze_parameters(extracted_text)
                else:
                    print("Error: Text extraction failed.")
            else:
                print("Error: Could not load image.")
        else:
            print("No image uploaded.")
    return render_template("index.html")  # Replace with your template


if __name__ == "__main__":
    app.run(debug=True)
