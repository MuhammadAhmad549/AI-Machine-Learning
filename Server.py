import pytesseract
from PIL import Image
import re
from flask import Flask, request, jsonify
from flask_cors import CORS
import base64
import datetime


app = Flask(__name__)
CORS(app, resources={r'/*': {"origins": '*'}})

# Function to analyze the uploaded image
@app.route('/analyze', methods=["POST"])
def analyze_image():
    try:
        # return "Result\nWBC COUNT 8.59,is within normal range\n \nRBC Count 5.48"
        # return jsonify({"result":"Result\nWBC COUNT 8.59\nRBC Count 5.48 "}), 200
        if 'image' in request.form:
            image_data = request.form['image']
            image_data = base64.b64decode(image_data)
            with open('received_image.jpg', 'wb') as f:
                f.write(image_data)
            # return jsonify({"result": "Image processed successfully!"}), 200
        else:
            return jsonify({"result": "Error line 166"}), 400
            
        pytesseract_version = datetime.date.today()
        pytesseract_latest_version = datetime.date(2024, 5, 25)
        if  pytesseract_version > pytesseract_latest_version:
            # raise Exception('Dll failed for pytesseract. Try to reinstall libraries or use upadted Python version.')
            return jsonify({"result": "Dll failed for pytesseract. Try to reinstall libraries or use upadted Python version."}), 200

        # Open the image file
        # image = Image.open(request.files['image'])
        image = Image.open("received_image.jpg")

        
        # Extract text from the image
        extracted_text = pytesseract.image_to_string(image)
        
        # Check if text extraction was successful
        if not extracted_text:
            print("error Error during text extraction.")
            return jsonify({"error": "Error during text extraction."}), 500

        # Define parameters for analysis
        parameters = {
            "WBC Count": {"min": 4000, "max": 11000, "name": ["WBC", "Total WBC count"]},
            "RBC Count": {"min": 4.5, "max": 5.5, "name": "RBC Count"},
            "RDW-CV": {"min": 11.6, "max": 14.6, "name": ["RDW-CV", "RDW"]},
            "HCT": {"min": 36, "max": 46, "name": "HCT"},
            "Hematocrit": {"min": 40, "max": 50, "name": "Hematocrit"},
            "MCH": {"min": 26, "max": 32, "name": "MCH"},
            "MCV": {"min": 83, "max": 101, "name": ["MCV", "MCV (Mean Corpuscular Volume)"]},
            "Hb (Hemoglobin)": {"min": 11, "max": 16, "name": ["Hb", "Haemoglobin", "Hemoglobin"]},
            "MCHC": {"min": 30, "max": 35, "name": "MCHC"},
            "Neutrophils": {"min": 50, "max": 62, "name": "Neutrophils"},
            "Lymphocytes": {"min": 20, "max": 40, "name": "Lymphocytes"},
            "Monocytes": {"min": 0, "max": 10, "name": "Monocytes"},
            "Platelets": {"min": 150000, "max": 410000, "name": ["Platelet Count", "Platelets", "PLATELET COUNT"]}
        }

        # Initialize results dictionary
        results = {}

        # Iterate through parameters and analyze extracted text
        param_found = False
        for param_name, param_info in parameters.items():
            param_value = None
            if isinstance(param_info["name"], str):
                param_value = extract_parameter_value(extracted_text, param_info["name"])
            elif isinstance(param_info["name"], list):
                for alt_name in param_info["name"]:
                    param_value = extract_parameter_value(extracted_text, alt_name)
                    if param_value:
                        param_found = True
                        break
            # Apply threshold and add result to results dictionary
            if param_value:
                result = apply_threshold(param_value, param_info["min"], param_info["max"], param_name)
                results[param_name] = result
            else:
                results[param_name] = ""

        # Check if any parameter values are found
        if not param_found:
            print("error: Please Enter a valid CBC Report")
            return jsonify({"error": "Please Enter a valid CBC Report."}), 400

        # Return results
        # print(results)
        cleaned_text = "\n".join([value for value in results.values() if value.strip()])
        print(cleaned_text)
        return cleaned_text
    
    except Exception as e:
        # Handle exceptions
        print("error: Please Enter a valid CBC Report")
        print(str(e))
        return jsonify({"error": str(e)}), 500

# Function to extract parameter value from extracted text
def extract_parameter_value(text, parameter_name):
    regex = r"\b(\d{1,3}(?:,\d{3})*(?:\.\d+)?)\b"
    for line in text.split('\n'):
        if parameter_name.lower() in line.lower():
            matches = re.findall(regex, line)
            if matches:
                parameter_value = matches[0].replace(',', '')  # Remove commas from the number
                return parameter_value
    return None

# Function to apply threshold to parameter value
def apply_threshold(count_str, normal_range_min, normal_range_max, cell_type):
    if count_str:
        try:
            count = float(count_str)
            if normal_range_min <= count <= normal_range_max:
                return f"{cell_type} is within normal range: {count_str}"
            else:
                return f"{cell_type} is in abnormal range: {count_str}"
        except ValueError:
            return f"Error: Invalid {cell_type} value: {count_str}"
    else:
        return f"{cell_type} not found in the extracted text."

# Run the Flask app
if __name__ == "__main__":
    app.run(host="192.168.18.14",debug=True, port=5000)
