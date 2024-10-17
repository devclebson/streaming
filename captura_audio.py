import tkinter as tk
from tkinter import ttk
import sounddevice as sd
import numpy as np
import wave
from PIL import Image, ImageTk
import pystray
from pystray import MenuItem as item
import threading

# Função para listar dispositivos de áudio
def listar_dispositivos_audio():
    dispositivos = sd.query_devices()
    return [dispositivo['name'] for dispositivo in dispositivos]

# Função para capturar áudio do dispositivo selecionado
def capturar_audio(dispositivo_indice):
    fs = 44100
    duracao = int(entry_duracao.get())
    canais = 2

    print(f"Gravando por {duracao} segundos com o dispositivo: {dispositivo_indice}")
    
    audio = sd.rec(int(duracao * fs), samplerate=fs, channels=canais, device=dispositivo_indice)
    sd.wait()
    print("Gravação finalizada!")
    
    salvar_audio_wav(audio, fs)

# Função para salvar o áudio gravado como arquivo .wav
def salvar_audio_wav(audio, fs):
    nome_arquivo = entry_nome_arquivo.get() or "gravacao"
    nome_arquivo += ".wav"

    # Verifique se o áudio não está vazio
    if audio.size == 0:
        print("Erro: Nenhum áudio foi gravado.")
        return
    
    # Normalizando o áudio
    max_val = np.max(np.abs(audio))
    if max_val > 0:  # Verifica se o máximo não é zero
        audio = np.int16(audio / max_val * 32767)
    else:
        print("Erro: Máximo do áudio é zero, não é possível normalizar.")
        return

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
    icone_imagem = Image.open("icone.png")
    
    def ao_clicar_icone(icon, item):
        root.deiconify()

    menu = (item('Abrir', ao_clicar_icone), item('Sair', sair))

    icone = pystray.Icon("audio_capture", icone_imagem, "Captura de Áudio", menu)
    threading.Thread(target=icone.run).start()

# Função para esconder a janela principal ao minimizar
def minimizar_janela():
    root.withdraw()
    criar_icone_bandeja()

# Função para encerrar o programa
def sair(icon, item):
    icon.stop()
    root.quit()

# Criação da janela principal com Tkinter
root = tk.Tk()
root.title("Captura de Áudio")
root.geometry("450x350")

# Evento de minimizar a janela
root.protocol("WM_DELETE_WINDOW", minimizar_janela)

# Label para o nome do dispositivo
label = tk.Label(root, text="Selecione a Placa de Áudio:")
label.pack(pady=5)

# Listar dispositivos de áudio
dispositivos = listar_dispositivos_audio()

# ComboBox para selecionar dispositivo de áudio
combo = ttk.Combobox(root, values=dispositivos, state="readonly", width=40)
combo.pack(pady=5)
combo.current(0)  # Seleciona o primeiro dispositivo por padrão

# Label e entrada para o nome do arquivo
label_nome_arquivo = tk.Label(root, text="Nome do arquivo:")
label_nome_arquivo.pack(pady=5)

entry_nome_arquivo = tk.Entry(root, width=30)
entry_nome_arquivo.pack(pady=5)

# Label e entrada para a duração da gravação
label_duracao = tk.Label(root, text="Duração da gravação (segundos):")
label_duracao.pack(pady=5)

entry_duracao = tk.Entry(root, width=10)
entry_duracao.pack(pady=5)
entry_duracao.insert(0, "5")

# Botão para iniciar a captura
botao_iniciar = tk.Button(root, text="Iniciar Captura", command=iniciar_captura_audio)
botao_iniciar.pack(pady=10)

# Iniciar o loop da interface
root.mainloop()
