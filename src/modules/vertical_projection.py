import cv2
import numpy as np
import matplotlib.pyplot as plt

class VerticalProjection:
    def __init__(self, image):
        self.image = image
        self.cleaned_image = self.clean_image()  # Limpeza da imagem

    def clean_image(self):
        # Aplicar filtro bilateral para suavizar a imagem enquanto preserva as bordas
        blured = cv2.bilateralFilter(self.image, d=25, sigmaColor=75, sigmaSpace=75)
        # Converter para escala de cinza
        gray = cv2.cvtColor(blured, cv2.COLOR_BGR2GRAY)
        # Aplicar limiarização
        _, binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

        # Detectar bordas
        edges = cv2.Canny(binary, threshold1=50, threshold2=150)
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cv2.imshow('binary', edges)
        
        # # Configurações para o desenho de retângulos e filtragem de ruído
        # height, width = self.image.shape[:2]
        # min_area = 50
        # rectangles = []

        # for contour in contours:
        #     epsilon = 0.02 * cv2.arcLength(contour, True)
        #     approx = cv2.approxPolyDP(contour, epsilon, True)

        #     # Verifica se o contorno é um retângulo (quatro vértices) e filtra contornos nas bordas
        #     if len(approx) == 4:
        #         x, y, w, h = cv2.boundingRect(approx)

        #         # Verifica se o retângulo está dentro da imagem e tem área mínima
        #         if x > 0 and y > 0 and x + w < width and y + h < height and cv2.contourArea(contour) >= min_area:
        #             # Desenha o retângulo na imagem
        #             cv2.rectangle(self.image, (x, y), (x + w, y + h), (0, 255, 0), 2)
                    
        #             # Recorta a região retangular da imagem original
        #             rectangle_img = self.image[y:y+h, x:x+w]
        #             rectangles.append(rectangle_img)

        #             height, width = rectangle_img.shape[:2]

        #             # Defina a largura e a altura do recorte desejado
        #             crop_width = 850  # Substitua pelo valor desejado
        #             crop_height = 700  # Substitua pelo valor desejado

        #             # Calcule as coordenadas do centro
        #             x_center = width // 2
        #             y_center = height // 2

        #             # Calcule as coordenadas do recorte
        #             x1 = max(0, x_center - crop_width // 2)
        #             y1 = max(0, y_center - crop_height // 2)
        #             x2 = min(width, x_center + crop_width // 2)
        #             y2 = min(height, y_center + crop_height // 2)

        #             # Recorte a imagem
        #             center_cropped_image =  rectangle_img[y1:y2, x1:x2]

        #             # Exibe o recorte do retângulo
        #             cv2.imshow(f"Rectangle {len(rectangles)}", center_cropped_image)

        # # Remover pequenos ruídos usando operação morfológica de abertura
        # kernel = np.ones((3, 3), np.uint8)
        # binary_cleaned = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel)

        # # Remover componentes conectados pequenos
        # num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(binary_cleaned, connectivity=8)
        # cleaned_image = np.zeros(binary_cleaned.shape, dtype=np.uint8)

        # for i in range(1, num_labels):  # Ignorar o rótulo 0 (background)
        #     if stats[i, cv2.CC_STAT_AREA] >= min_area:
        #         cleaned_image[labels == i] = 255

        # Exibir a imagem original com retângulos desenhados
        # cv2.imshow("Image with Rectangles", self.image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

        return cleaned_image

    def make_projection(self):
        # Exibir a imagem limpa para verificação
        cv2.imshow('Cleaned Image', self.cleaned_image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

        # Calcular projeção vertical
        vertical_projection = np.sum(self.cleaned_image, axis=0)

        # Definir um limiar para detectar vales
        threshold = np.mean(vertical_projection) * 0.5
        valleys = np.where(vertical_projection < threshold)[0]
        
        if len(valleys) < 2:
            print("Nenhum vale encontrado com o threshold atual. Tente ajustar o threshold.")
            return []

        segments = []
        prev_valley = valleys[0]

        for valley in valleys[1:]:
            if valley - prev_valley > 5:
                segments.append((prev_valley, valley))
            prev_valley = valley

        # Exibir cada caractere segmentado
        for i, (start, end) in enumerate(segments):
            character_image = self.cleaned_image[:, start:end]
            plt.imshow(character_image, cmap='gray')
            plt.title(f'Caractere {i}')
            plt.axis('off')
            plt.show()

        return segments
