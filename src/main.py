import os
import cv2
import threading
import queue
import time
import logging
from ultralytics import YOLO
from modules.detect_cars import CarDetector
from modules.plate_detection import LicensePlateDetector
from modules.plate_reader import PlateReader
from modules.register import escreve_no_arquivo
from modules.validatePlate import validate_and_correct_plate
from interface.gui import Interface
from database.database import DatabaseManager

#iniciar o banco
db = DatabaseManager("meuIFPlacas.db")

# Configurações
dia_folder = 'dia4'
video = 'video6.mp4'

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
video_path = os.path.join(ROOT_DIR, 'videos', dia_folder, video)
output_dir = os.path.join(ROOT_DIR, 'output_frames')
os.makedirs(output_dir, exist_ok=True)

frame_width = 640
frame_height = 480

# Configurações Gerais
SHARPNESS_THRESHOLD = 1.79  # Nitidez mínima para quadros e placas
CAPTURE_DURATION = 4  # Duração da captura em segundos
FRAME_PROCESS_INTERVAL = 60  # Processar 1 frame por segundo

# Configurar logging
logging.basicConfig(level=logging.INFO, format='[%(asctime)s] %(message)s')

# Carregar modelos
model_car = YOLO(os.path.join(ROOT_DIR, 'models', 'front_vehicle.pt'))
model_plate = YOLO(os.path.join(ROOT_DIR, 'models', 'model_plate_recognizer.pt'))
model_characters = YOLO(os.path.join(ROOT_DIR, 'models', 'best.pt'))

# Inicializar detectores
car_detector = CarDetector(model_car)
plate_detector = LicensePlateDetector(model_plate)
plate_reader = PlateReader(model_characters)

# Interface
def start_thread(target, threads):
    """Inicia e adiciona uma thread à lista de threads gerenciadas."""
    thread = threading.Thread(target=target, daemon=True)
    thread.start()
    threads.append(thread)

app = Interface()
threads = []

# Fila para pipeline
frame_queue = queue.Queue(maxsize=60)  # Limite de frames em processamento
results_queue = queue.Queue(maxsize=60)  # Resultados para interface

# Variável de controle
stop_processing = threading.Event()

# Funções Auxiliares
def is_sharp(image, threshold=SHARPNESS_THRESHOLD):
    """Verifica se a imagem é suficientemente nítida."""
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    laplacian_var = cv2.Laplacian(gray, cv2.CV_64F).var()
    return laplacian_var > threshold

def select_best_frame(frames):
    """Seleciona o melhor frame com base na nitidez."""
    if not frames:
        return None

    return max(frames, key=lambda frame: cv2.Laplacian(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY), cv2.CV_64F).var())

# Função para capturar frames
def capture_frames():
    """Captura frames somente quando um veículo é detectado."""
    cap = cv2.VideoCapture(video_path)
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    frame_interval = max(1, fps // FRAME_PROCESS_INTERVAL)
    frame_count = 0

    captured_frames = []
    start_time = None
    vehicle_detected = False

    while not stop_processing.is_set():
        ret, frame = cap.read()

        if not ret:
            logging.info("Fim do vídeo detectado.")
            if vehicle_detected and captured_frames:
                logging.info("Selecionando melhor frame com os dados disponíveis.")
                best_frame = select_best_frame(captured_frames)
                if best_frame is not None:
                    frame_queue.put(best_frame)
                    logging.info("Melhor frame selecionado.")
                else:
                    logging.warning("Nenhum frame válido encontrado.")

            break

        cv2.imshow('Video', cv2.resize(frame, (frame_width, frame_height)))
        cv2.waitKey(1)  # Pequeno atraso para processar eventos da janela
        frame_count += 1
        if frame_count % frame_interval == 0:
            resized_frame = cv2.resize(frame, (frame_width, frame_height))

            # Detectar veículo
            img_with_cars, car_boxes = car_detector.detect_cars(resized_frame, drawboxes=True)

            if car_boxes and not vehicle_detected:
                vehicle_detected = True
                start_time = time.time()
                logging.info("Veículo detectado. Iniciando captura de frames.")

            if vehicle_detected:
                captured_frames.append(resized_frame)
                print('Salvando frame...')

                if time.time() - start_time >= CAPTURE_DURATION:
                    logging.info('Tempo de captura concluído.')
                    
                    if captured_frames:
                        best_frame = select_best_frame(captured_frames)
                        if best_frame is not None:
                            frame_queue.put(best_frame)
                            logging.info('Melhor frame selecionado.')
                        else:
                            logging.warning('Nenhum frame válido encontrado.')

                    captured_frames.clear()
                    vehicle_detected = False

    cap.release()
    frame_queue.put(None)
# Função para processamento de frames
def process_frames():
    """Processa os frames para detectar placas e enviar resultados."""
    while True:
        frame = frame_queue.get()
        if frame is None:
            results_queue.put(None)
            break

        print('Processando frame...')
        
        try:
            img_with_cars, car_boxes = car_detector.detect_cars(frame, drawboxes=False)
            print(car_boxes, 'box')
            if car_boxes:
                vehicle_img = car_detector.extract_and_resize_vehicle(frame, car_boxes[0])
                
                _, plate_boxes = plate_detector.detect_license_plate_box(vehicle_img, drawboxes=False)
                if plate_boxes:
                    plate_img = car_detector.extract_and_resize_vehicle(vehicle_img, plate_boxes[0])

                    if not is_sharp(plate_img):
                        logging.warning("Placa ignorada por estar borrada.")
                        continue

                    _, _, plate_str = plate_reader.detect_characters(plate_img, drawboxes=False)

                    print(plate_str, '--------------------------------')
                    corrected_plate = validate_and_correct_plate(plate_str)

                    if len(corrected_plate) > 0:
                        # Salvar frame completo
                        output_path = os.path.join(output_dir, dia_folder, f"frame_{video.split('.')[0]}_{dia_folder}.jpg")
                        cv2.imwrite(output_path, frame)

                        escreve_no_arquivo(corrected_plate)
                        results_queue.put((corrected_plate, plate_img))
                        logging.info(f"Placa registrada: {corrected_plate}")

                        # Parar processamento ao encontrar o melhor frame
                        stop_processing.set()
                        return

        except Exception as e:
            logging.error("Erro ao processar frame:", exc_info=True)

# Função para atualização da interface
def update_interface():
    """Atualiza a interface com os resultados do processamento."""
    while True:
        result = results_queue.get()
        if result is None:
            break
        
        plate, plate_img = result

        # Consultar o banco de dados
        aluno = db.get_register(plate)
        print('registro:', aluno, plate)
        tk_image = app.convert_mat_to_tk(cv2.resize(plate_img, (400, 200)))
        app.image_label.config(image=tk_image)
        app.image_label.image = tk_image

        app.atualizar_inferior(nome=aluno[1], placa=aluno[2], permissao=aluno[3])

# Iniciar threads
start_thread(capture_frames, threads)
start_thread(process_frames, threads)
start_thread(update_interface, threads)

# Iniciar interface
app.iniciar()

# Parar threads ao fechar
stop_processing.set()
for thread in threads:
    thread.join()
