import tkinter as tk
from tkinter import ttk
import sounddevice as sd
import numpy as np
import wave
from PIL import Image, ImageTk  # Para lidar com o ícone
import pystray  # Para o ícone da bandeja de tarefas
from pystray import MenuItem as item
import threading

# Função para listar dispositivos de áudio
def listar_dispositivos_audio():
    dispositivos = sd.query_devices()
    return [dispositivo['name'] for dispositivo in dispositivos]

# Função para capturar áudio do dispositivo selecionado
def capturar_audio(dispositivo_indice):
    fs = 44100  # Taxa de amostragem (44.1 kHz)
    duracao = int(entry_duracao.get())  # Duração da gravação em segundos
    canais = 2  # Gravar em estéreo

    print(f"Gravando por {duracao} segundos com o dispositivo: {dispositivo_indice}")
    
    # Capturando o áudio
    audio = sd.rec(int(duracao * fs), samplerate=fs, channels=canais, device=dispositivo_indice)
    sd.wait()  # Aguarda a gravação finalizar
    print("Gravação finalizada!")
    
    # Salvar o áudio em um arquivo .wav
    salvar_audio_wav(audio, fs)

# Função para salvar o áudio gravado como arquivo .wav
def salvar_audio_wav(audio, fs):
    nome_arquivo = entry_nome_arquivo.get() or "gravacao"
    nome_arquivo += ".wav"
    
    # Normalizando o áudio
    audio = np.int16(audio / np.max(np.abs(audio)) * 32767)
    
    # Salvando o áudio no formato .wav
    with wave.open(nome_arquivo, 'wb') as f:
        f.setnchannels(2)  # Estéreo
        f.setsampwidth(2)  # 16-bit
        f.setframerate(fs)
        f.writeframes(audio.tobytes())
    
    print(f"Arquivo salvo como: {nome_arquivo}")

# Função que inicia a captura de áudio com o dispositivo selecionado
def iniciar_captura_audio():
    dispositivo = combo.get()
    indice_dispositivo = dispositivos.index(dispositivo)
    capturar_audio(indice_dispositivo)

# Função para criar o ícone da bandeja do sistema
def criar_icone_bandeja():
    # Carregar o ícone (substitua pelo caminho do seu ícone)
    icone_imagem = Image.open("icone.png")
    
    # Função para quando o usuário clicar no ícone da bandeja
    def ao_clicar_icone(icon, item):
        # Mostrar novamente a interface quando o ícone for clicado
        root.deiconify()

    # Menu da bandeja com opção de sair
    menu = (item('Abrir', ao_clicar_icone), item('Sair', sair))

    # Criar ícone de bandeja
    icone = pystray.Icon("audio_capture", icone_imagem, "Captura de Áudio", menu)
    threading.Thread(target=icone.run).start()

# Função para esconder a janela principal ao minimizar
def minimizar_janela():
    root.withdraw()  # Esconde a janela
    criar_icone_bandeja()

# Função para encerrar o programa
def sair(icon, item):
    icon.stop()  # Para o ícone da bandeja
    root.quit()  # Encerra o programa

# Criação da janela principal com Tkinter
root = tk.Tk()
root.title("Captura de Áudio")
root.geometry("400x300")  # Aumenta a altura para acomodar melhor os widgets

# Estilização do Tkinter
style = ttk.Style()
style.configure("TCombobox", padding=5, width=40)  # Aumenta a largura do ComboBox

# Evento de minimizar a janela
root.protocol("WM_DELETE_WINDOW", minimizar_janela)

# Label para o nome do dispositivo
label = tk.Label(root, text="Selecione a Placa de Áudio:")
label.pack(pady=5)

# Listar dispositivos de áudio
dispositivos = listar_dispositivos_audio()

# ComboBox para selecionar dispositivo de áudio
combo = ttk.Combobox(root, values=dispositivos, state="readonly")
combo.pack(pady=5)
combo.current(0)  # Seleciona o primeiro dispositivo por padrão

# Label e entrada para o nome do arquivo
label_nome_arquivo = tk.Label(root, text="Nome do arquivo:")
label_nome_arquivo.pack(pady=5)

entry_nome_arquivo = tk.Entry(root, width=30)  # Define a largura da entrada
entry_nome_arquivo.pack(pady=5)

# Label e entrada para a duração da gravação
label_duracao = tk.Label(root, text="Duração da gravação (segundos):")
label_duracao.pack(pady=5)

entry_duracao = tk.Entry(root, width=10)  # Define a largura da entrada
entry_duracao.pack(pady=5)
entry_duracao.insert(0, "5")  # Valor padrão de 5 segundos

# Botão para iniciar a captura
botao_iniciar = tk.Button(root, text="Iniciar Captura", command=iniciar_captura_audio)
botao_iniciar.pack(pady=10)

# Iniciar o loop da interface
root.mainloop()
