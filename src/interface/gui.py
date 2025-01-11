import tkinter as tk
from PIL import Image, ImageTk
import os
import cv2

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
path_logo = os.path.join(ROOT_DIR, 'logo.png')

class Interface:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Minha Aplicação")
        self.root.geometry("1024x720")  # Define o tamanho inicial da janela
        self._setup_layout()

    def _setup_layout(self):
        """Configura o layout da interface"""

        # Frame superior (20% da altura)
        self.top_frame = tk.Frame(self.root)
        self.top_frame.place(relx=0, rely=0, relwidth=1, relheight=0.2)

        # Adiciona uma imagem no canto superior esquerdo
        self._add_image_to_top_frame()

        # Frame inferior (80% da altura)
        self.bottom_frame = tk.Frame(self.root, bg="lightgray")
        self.bottom_frame.place(relx=0, rely=0.2, relwidth=1, relheight=0.8)

        # Divide o bottom_frame em duas partes
        self._setup_bottom_divisions()

    def _add_image_to_top_frame(self):
        """Adiciona uma imagem no canto superior esquerdo do frame superior"""
        try:
            # Carrega a imagem (substitua 'logo.png' pelo caminho do arquivo)
            image = Image.open(path_logo)
            image = image.resize((200, 100))  # Ajuste o tamanho da imagem
            photo = ImageTk.PhotoImage(image)

            # Adiciona a imagem ao top_frame
            image_label = tk.Label(self.top_frame, image=photo)
            image_label.image = photo  # Referência para evitar garbage collection
            image_label.place(x=10, y=10)  # Posiciona no canto superior esquerdo
        except FileNotFoundError:
            print("Imagem não encontrada. Certifique-se de que o arquivo 'logo.png' está no mesmo diretório.")

    def _setup_bottom_divisions(self):
        """Divide o bottom_frame em dois frames iguais (50% cada)"""

        # Frame esquerdo (50% da largura)
        self.left_frame = tk.Frame(self.bottom_frame, bg="white")
        self.left_frame.place(relx=0, rely=0, relwidth=0.5, relheight=1)

        # Adiciona um espaço para a imagem centralizada no frame esquerdo
        self.image_label = tk.Label(self.left_frame, bg="white")
        self.image_label.pack(expand=True)

        # Frame direito (50% da largura)
        self.right_frame = tk.Frame(self.bottom_frame, bg="lightgray")
        self.right_frame.place(relx=0.5, rely=0, relwidth=0.5, relheight=1)

        # Adiciona informações no frame direito
        self.info_label = tk.Label(self.right_frame, text="", font=("Arial", 14), bg="lightgray", justify="left")
        self.info_label.pack(padx=10, pady=10, anchor="n")

    def atualizar_inferior(self, nome, placa, permissao):
        """
        Atualiza a imagem e as informações na área inferior.

        Args:
            img_path (str): Caminho para a nova imagem.
            nome (str): Nome a ser exibido.
            placa (str): Placa a ser exibida.
            permissao (str): Permissão a ser exibida.
        """
        
        print(permissao)
        # Atualizar as informações no frame direito
        info_text = f"Nome: {nome}\nPlaca: {placa}\nPermissão: {'Autorizado' if permissao == 1 else 'Não Autorizado'}"
        self.info_label.config(text=info_text)

    def convert_mat_to_tk(self, mat): 
        """Converte uma imagem OpenCV (MatLike) para um formato compatível com Tkinter."""
        # Converte BGR para RGB
        rgb_image = cv2.cvtColor(mat, cv2.COLOR_BGR2RGB)

        # Converte para Pillow Image
        pil_image = Image.fromarray(rgb_image)

        # Converte para Tkinter PhotoImage
        tk_image = ImageTk.PhotoImage(pil_image)

        return tk_image

    def iniciar(self):
        """Inicia o loop principal da interface"""
        self.root.mainloop()