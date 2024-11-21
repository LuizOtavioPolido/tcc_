import requests
import base64

# Chave da API do Google Cloud diretamente no código
google_cloud_key = 'AIzaSyAr1CzAwtwz66nBdicS3F8nt2tWHqLOqp4'

# URL da API do Google Cloud Vision
vision_api_url = f'https://vision.googleapis.com/v1/images:annotate?key={google_cloud_key}'

# Função para utilizar o Google Cloud Vision API
def detect_text_google(img_path):
    with open(img_path, 'rb') as image_file:
        content = base64.b64encode(image_file.read()).decode('utf-8')

    request_payload = {
        'requests': [{
            'image': {
                'content': content
            },
            'features': [{
                'type': 'TEXT_DETECTION'
            }]
        }]
    }

    response = requests.post(vision_api_url, json=request_payload)
    response_data = response.json()

    if 'error' in response_data:
        raise Exception(f"{response_data['error']['message']}")

    texts = response_data['responses'][0].get('textAnnotations', [])
    return texts

# Lista de imagens para testar
image_paths = [
    'carro1.jpg',
    'carro3.jpg',
    'image1.jpg',
    'image2.jpg',
    'image3.jpg',
    'image4.jpg'
]

# Analisar as imagens usando Google Cloud Vision API
for img_path in image_paths:
    detected_texts = detect_text_google(img_path)
    
    print(f"Resultados para a imagem: {img_path}")
    for text in detected_texts:
        print(f"Texto reconhecido: {text['description']}")
    print()
