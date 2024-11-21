import pytesseract

def recognize_text(preprocessed_plate):
    
    # pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

    text = pytesseract.image_to_string(preprocessed_plate, lang='por')
    
    return text.strip()
