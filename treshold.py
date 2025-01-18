z


import pytesseract
from PIL import Image
import re

def load_image(image_path):
    try:
        image = Image.open(image_path)
        return image
    except Exception as e:
        print("Error:", e)
        return None

def extract_text(image):
    if image:
        try:
            extracted_text = pytesseract.image_to_string(image)
            return extracted_text
        except Exception as e:
            print("Error during text extraction:", e)
            return None
    else:
        return None

def extract_parameter_value(text, parameter_name):
    regex = r"\b(\d{1,3}(?:,\d{3})*(?:\.\d+)?)\b"
    for line in text.split('\n'):
        if parameter_name.lower() in line.lower():
            matches = re.findall(regex, line)
            if matches:
                parameter_value = matches[0].replace(',', '')  # Remove commas from the number
                return parameter_value
    return None

def apply_threshold(count_str, normal_range_min, normal_range_max, cell_type):
    if count_str:
        try:
            count = float(count_str)
            if normal_range_min <= count <= normal_range_max:
                print(f"{cell_type} is within normal range:", count_str)
            else:
                print(f"{cell_type} is abnormal. Value:", count_str)
        except ValueError:
            print(f"Error: Invalid {cell_type} value:", count_str)
    else:
        print(f"{cell_type} not found in the extracted text.")

def main():
    image_path = "WhatsApp Image 2024-05-02 at 4.56.56 PM.jpeg"
    image = load_image(image_path)
    if image:
        extracted_text = extract_text(image)
        if extracted_text:
            parameters = {
                "WBC Count": {"min": 4000, "max": 11000, "name": ["WBC","Total WBC count"]},
                "RBC Count": {"min": 4.5, "max": 5.5, "name": "RBC Count"},
                "RDW-CV": {"min": 11.6, "max": 14.6, "name": ["RDW-CV","RDW"]},
                "HCT": {"min": 36, "max": 46, "name": "HCT"},
                "Hematocrit": {"min": 40, "max": 50, "name": "Hematocrit"},
                "MCH": {"min": 26, "max": 32, "name": "MCH"},
                "MCV": {"min": 83, "max": 101, "name": ["MCV", "MCV (Mean Corpuscular Volume)"]},
                "Hb (Hemoglobin)": {"min": 11, "max": 16, "name": ["Hb", "Haemoglobin","Hemoglobin"]},
                "MCHC": {"min": 30, "max": 35, "name": "MCHC"},
                "Neutrophils": {"min": 50, "max": 62, "name": "Neutrophils"},
                "Lymphocytes": {"min": 20, "max": 40, "name": "Lymphocytes"},
                "Monocytes": {"min": 0, "max": 10, "name": "Monocytes"},
                "Eosinophils": {"min": 1, "max": 5, "name": "Eosinophils"},
                "Basophils": {"min": 0, "max": 1, "name": "Basophils"},
                "Bands": {"min": 0, "max": 3, "name": "Bands"},
                "Platelets": {"min": 150000, "max": 410000, "name": [ "Platelet Count","Platelets","PLATELET COUNT"]}
            }
            found_any_param = False
            for param_name, param_info in parameters.items():
                param_value = None
                if isinstance(param_info["name"], str):
                    param_value = extract_parameter_value(extracted_text, param_info["name"])
                elif isinstance(param_info["name"], list):
                    for alt_name in param_info["name"]:
                        param_value = extract_parameter_value(extracted_text, alt_name)
                        if param_value:
                            break
                if param_value:
                    found_any_param = True
                    apply_threshold(param_value, param_info["min"], param_info["max"], param_name)
                else:
                    print(f"{param_name} not found in the extracted text.")
            if not found_any_param:
                print("Please Enter a Valid CBC report.")

if __name__ == "__main__":
    main()














# import pytesseract
# from PIL import Image
# import re
# from flask import Flask, request, jsonify
# from flask_cors import CORS

# app = Flask(__name__)
# CORS(app, resources={r'/*': {"origins": '*'}})

# @app.route('/', methods=["POST"])
# def load_image():
#     try:
#         image = Image.open(request.files['image'])
#         extracted_text = extract_text(image)
#         if extracted_text:
#             return jsonify({"extracted_text": extracted_text})
#         else:
#             return jsonify({"error": "Error during text extraction."}), 500
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500

# def extract_text(image):
#     if image:
#         try:
#             extracted_text = pytesseract.image_to_string(image)
#             return extracted_text
#         except Exception as e:
#             print("Error during text extraction:", e)
#             return None
#     else:
#         return None

# def extract_parameter_value(text, parameter_name):
#     regex = r"\b(\d{1,3}(?:,\d{3})*(?:\.\d+)?)\b"
#     for line in text.split('\n'):
#         if parameter_name.lower() in line.lower():
#             matches = re.findall(regex, line)
#             if matches:
#                 parameter_value = matches[0].replace(',', '')  # Remove commas from the number
#                 return parameter_value
#     return None

# def apply_threshold(count_str, normal_range_min, normal_range_max, cell_type):
#     if count_str:
#         try:
#             count = float(count_str)
#             if normal_range_min <= count <= normal_range_max:
#                 return f"{cell_type} is within normal range: {count_str}"
#             else:
#                 return f"{cell_type} is abnormal. Value: {count_str}"
#         except ValueError:
#             return f"Error: Invalid {cell_type} value: {count_str}"
#     else:
#         return f"{cell_type} not found in the extracted text."

# @app.route('/analyze', methods=["POST"])
# def analyze_image():
#     try:
#         image = Image.open(request.files['image'])
#         extracted_text = extract_text(image)
#         if extracted_text:
#             results = {}
#             parameters = {
#                 "WBC Count": {"min": 4000, "max": 11000, "name": "WBC"},
#                 "RBC Count": {"min": 4.5, "max": 5.5, "name": "RBC Count"},
#                 "RDW-CV": {"min": 11.6, "max": 14.6, "name": "RDW-CV"},
#                 "HCT": {"min": 36, "max": 46, "name": "HCT"},
#                 "MCH": {"min": 26, "max": 32, "name": "MCH"},
#                 "Hb (Hemoglobin)": {"min": 11, "max": 16, "name": ["Hb", "Hemoglobin"]},
#                 "MCHC": {"min": 30, "max": 35, "name": "MCHC"},
#                 "Platelet Count": {"min": 150000, "max": 410000, "name": ["Platelets", "Platelet Count"]}
#             }
#             for param_name, param_info in parameters.items():
#                 param_value = None
#                 if isinstance(param_info["name"], str):
#                     param_value = extract_parameter_value(extracted_text, param_info["name"])
#                 elif isinstance(param_info["name"], list):
#                     for alt_name in param_info["name"]:
#                         param_value = extract_parameter_value(extracted_text, alt_name)
#                         if param_value:
#                             break
#                 if param_value:
#                     result = apply_threshold(param_value, param_info["min"], param_info["max"], param_name)
#                     results[param_name] = result
#                 else:
#                     results[param_name] = f"{param_name} not found in the extracted text."
#             return jsonify(results)
#         else:
#             return jsonify({"error": "Error during text extraction."}), 500
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500

# if __name__ == "__main__":
#     app.run(debug=True, port=5000)



# import pytesseract
# from PIL import Image
# import re
# from flask import Flask, request, jsonify
# from flask_cors import CORS

# app = Flask(__name__)
# CORS(app, resources={r'/*': {"origins": '*'}})

# @app.route('/analyze', methods=["POST"])
# def analyze_image():
#     try:
#         if 'image' not in request.files:
#             return jsonify({"error": "No image file provided."}), 400
        
#         image = Image.open(request.files['image'])
#         extracted_text = pytesseract.image_to_string(image)
        
#         if not extracted_text:
#             return jsonify({"error": "Error during text extraction."}), 500

#         results = {}
#         parameters = {
#                 "WBC Count": {"min": 4000, "max": 11000, "name": ["WBC","Total WBC count"]},
#                 "RBC Count": {"min": 4.5, "max": 5.5, "name": "RBC Count"},
#                 "RDW-CV": {"min": 11.6, "max": 14.6, "name": ["RDW-CV","RDW"]},
#                 "HCT": {"min": 36, "max": 46, "name": "HCT"},
#                 "Hematocrit": {"min": 40, "max": 50, "name": "Hematocrit"},
#                 "MCH": {"min": 26, "max": 32, "name": "MCH"},
#                 "MCV": {"min": 83, "max": 101, "name": ["MCV", "MCV (Mean Corpuscular Volume)"]},
#                 "Hb (Hemoglobin)": {"min": 11, "max": 16, "name": ["Hb", "Haemoglobin","Hemoglobin"]},
#                 "MCHC": {"min": 30, "max": 35, "name": "MCHC"},
#                 "Neutrophils": {"min": 50, "max": 62, "name": "Neutrophils"},
#                 "Lymphocytes": {"min": 20, "max": 40, "name": "Lymphocytes"},
#                 "Monocytes": {"min": 0, "max": 10, "name": "Monocytes"},
#                 "Platelets": {"min": 150000, "max": 410000, "name": [ "Platelet Count","Platelets","PLATELET COUNT"]}
#             }
#         for param_name, param_info in parameters.items():
#             param_value = None
#             if isinstance(param_info["name"], str):
#                 param_value = extract_parameter_value(extracted_text, param_info["name"])
#             elif isinstance(param_info["name"], list):
#                 for alt_name in param_info["name"]:
#                     param_value = extract_parameter_value(extracted_text, alt_name)
#                     if param_value:
#                         break
#             if param_value:
#                 result = apply_threshold(param_value, param_info["min"], param_info["max"], param_name)
#                 results[param_name] = result
#             else:
#                 results[param_name] = ""

#         return jsonify(results)
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500

# def extract_parameter_value(text, parameter_name):
#     regex = r"\b(\d{1,3}(?:,\d{3})*(?:\.\d+)?)\b"
#     for line in text.split('\n'):
#         if parameter_name.lower() in line.lower():
#             matches = re.findall(regex, line)
#             if matches:
#                 parameter_value = matches[0].replace(',', '')  # Remove commas from the number
#                 return parameter_value
#     return None

# def apply_threshold(count_str, normal_range_min, normal_range_max, cell_type):
#     if count_str:
#         try:
#             count = float(count_str)
#             if normal_range_min <= count <= normal_range_max:
#                 return f"{cell_type} is within normal range: {count_str}"
#             else:
#                 return f"{cell_type} is abnormal. Value: {count_str}"
#         except ValueError:
#             return f"Error: Invalid {cell_type} value: {count_str}"
#     else:
#         return f"{cell_type} not found in the extracted text."

# if __name__ == "__main__":
#     app.run(debug=False, port=5000)

