

# import pytesseract
# from PIL import Image
# import re
# from flask import Flask, request, jsonify
# from flask_cors import CORS

# app = Flask(__name__)
# CORS(app, resources={r'/*': {"origins": '*'}})

# # Function to analyze the uploaded image
# @app.route('/analyze', methods=["POST"])
# def analyze_image():
#     try:
#         # Check if image file is provided
#         if 'image' not in request.files:
#             return jsonify({"error": "No image file provided."}), 400
        
#         # Open the image file
#         image = Image.open(request.files['image'])
        
#         # Extract text from the image
#         extracted_text = pytesseract.image_to_string(image)
        
#         # Check if text extraction was successful
#         if not extracted_text:
#             return jsonify({"error": "Error during text extraction."}), 500

#         # Define parameters for analysis
#         parameters = {
#             "WBC Count": {"min": 4000, "max": 10000, "name": ["WBC", "Total WBC count"]},
#             "RBC Count": {"min": 4.5, "max": 5.5, "name": "RBC Count"},
#             "RDW-CV": {"min": 11, "max": 16, "name": ["RDW-CV", "RDW"]},
#             "HCT": {"min": 36, "max": 46, "name": "HCT"},
#             "Hematocrit": {"min": 40, "max": 50, "name": "Hematocrit"},
#             "MCH": {"min": 27, "max": 32, "name": "MCH"},
#             "MCV": {"min": 83, "max": 101, "name": ["MCV", "MCV (Mean Corpuscular Volume)"]},
#             "Hb (Hemoglobin)": {"min": 13, "max": 17, "name": ["Hb", "Haemoglobin", "Hemoglobin"]},
#             "MCHC": {"min": 31.5, "max": 34.5, "name": "MCHC"},
#             "Neutrophils": {"min": 40, "max": 70, "name": "Neutrophils"},
#             "Lymphocytes": {"min": 25, "max": 45, "name": "Lymphocytes"},
#             "Monocytes": {"min": 2, "max": 12, "name": "Monocytes"},
#             "Eosinophils": {"min": 1, "max": 5, "name": "Eosinophils"},
#             "Basophils": {"min": 0, "max": 1, "name": "Basophils"},
#             "Bands": {"min": 0, "max": 3, "name": "Bands"},
#             "Platelets": {"min": 150000, "max": 410000, "name": ["Platelet Count", "Platelets", "PLATELET COUNT"]}
#         }

#         # Initialize results dictionary
#         results = {}

#         # Iterate through parameters and analyze extracted text
#         param_found = False
#         for param_name, param_info in parameters.items():
#             param_value = None
#             if isinstance(param_info["name"], str):
#                 param_value = extract_parameter_value(extracted_text, param_info["name"])
#             elif isinstance(param_info["name"], list):
#                 for alt_name in param_info["name"]:
#                     param_value = extract_parameter_value(extracted_text, alt_name)
#                     if param_value:
#                         param_found = True
#                         break
#             # Apply threshold and add result to results dictionary
#             if param_value:
#                 result = apply_threshold(param_value, param_info["min"], param_info["max"], param_name)
#                 results[param_name] = result
#             else:
#                 results[param_name] = ""

#         # Check if any parameter values are found
#         if not param_found:
#             return jsonify({"error": "Please Enter a valid CBC Report."}), 400

#         # Return results without double quotes
#         cleaned_results = {key: value.strip('"') for key, value in results.items()}
#         return jsonify(cleaned_results)
    
#     except Exception as e:
#         # Handle exceptions
#         return jsonify({"error": str(e)}), 500

# # Function to extract parameter value from extracted text
# def extract_parameter_value(text, parameter_name):
#     regex = r"\b(\d{1,3}(?:,\d{3})*(?:\.\d+)?)\b"
#     for line in text.split('\n'):
#         if parameter_name.lower() in line.lower():
#             matches = re.findall(regex, line)
#             if matches:
#                 parameter_value = matches[0].replace(',', '')  # Remove commas from the number
#                 return parameter_value
#     return None

# # Function to apply threshold to parameter value
# def apply_threshold(count_str, normal_range_min, normal_range_max, cell_type):
#     if count_str:
#         try:
#             count = float(count_str)
#             if normal_range_min <= count <= normal_range_max:
#                 # Normal values
#                 return f"{cell_type} is within normal range: {count_str}"
#             else:
#                 # Abnormal values
#                 return f"{cell_type} is abnormal. Value: {count_str}"
#         except ValueError:
#             return f"Error: Invalid {cell_type} value: {count_str}"
#     else:
#         return f"{cell_type} not found in the extracted text."

# # Run the Flask app
# if __name__ == "__main__":
#     app.run(host='0.0.0.0', port=5000)







import pytesseract
from PIL import Image
import re
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r'/*': {"origins": '*'}})

# Function to analyze the uploaded image
@app.route('/analyze', methods=["POST"])
def analyze_image():
    try:
        # Check if image file is provided
        if 'image' not in request.files:
            return jsonify({"error": "No image file provided."}), 400
        
        # Open the image file
        image = Image.open(request.files['image'])
        
        # Extract text from the image
        extracted_text = pytesseract.image_to_string(image)
        
        # Check if text extraction was successful
        if not extracted_text:
            return jsonify({"error": "Error during text extraction."}), 500

        # Define parameters for analysis
        parameters = {
            "WBC Count": {"min": 4000, "max": 11000, "name": ["WBC", "Total WBC count"]},
            "RBC Count": {"min": 4.5, "max": 5.5, "name": "RBC Count"},
            "RDW-CV": {"min": 11, "max": 16, "name": ["RDW-CV", "RDW"]},
            "HCT": {"min": 36, "max": 46, "name": "HCT"},
            "Hematocrit": {"min": 40, "max": 50, "name": "Hematocrit"},
            "MCH": {"min": 27, "max": 32, "name": "MCH"},
            "MCV": {"min": 83, "max": 101, "name": ["MCV", "MCV (Mean Corpuscular Volume)"]},
            "Hb (Hemoglobin)": {"min": 13, "max": 17, "name": ["Hb", "Haemoglobin", "Hemoglobin"]},
            "MCHC": {"min": 31.5, "max": 34.5, "name": "MCHC"},
            "Neutrophils": {"min": 40, "max": 70, "name": "Neutrophils"},
            "Lymphocytes": {"min": 25, "max": 45, "name": "Lymphocytes"},
            "Monocytes": {"min": 2, "max": 12, "name": "Monocytes"},
            "Eosinophils": {"min": 1, "max": 5, "name": "Eosinophils"},
            "Basophils": {"min": 0, "max": 1, "name": "Basophils"},
            "Bands": {"min": 0, "max": 3, "name": "Bands"},
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
            return jsonify({"error": "Please Enter a valid CBC Report."}), 400

        # Return results without double quotes
        cleaned_results = {key: value.strip('"') for key, value in results.items()}
        return jsonify(cleaned_results)
    
    except Exception as e:
        # Handle exceptions
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
                # Normal values
                return f"{cell_type} is within normal range: {count_str}"
            else:
                # Abnormal values
                return f"{cell_type} is abnormal. Value: {count_str}"
        except ValueError:
            return f"Error: Invalid {cell_type} value: {count_str}"
    else:
        return f"{cell_type} not found in the extracted text."

# Run the Flask app
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
