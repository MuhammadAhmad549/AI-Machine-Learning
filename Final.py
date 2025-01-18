import pytesseract
from PIL import Image

# Step 3: Load and Preprocess Image
image_path = "Diabetes.JPG"  # Replace "path_to_your_image.jpg" with the actual path to your image file
try:
    image = Image.open(image_path)
except Exception as e:
    print("Error:", e)

# Step 4: Perform OCR
extracted_text = pytesseract.image_to_string(image)

# Step 5: Print Extracted Text
print(extracted_text)




