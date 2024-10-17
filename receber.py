import socket
import wave
import pyaudio

def start_audio_server():
    SERVER_IP = '0.0.0.0'
    SERVER_PORT = 12345
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 2
    RATE = 44100

    p = pyaudio.PyAudio()

    wf = wave.open('output.wav', 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((SERVER_IP, SERVER_PORT))
        s.listen(1)
        print("Servidor de áudio aguardando conexão...")

        conn, addr = s.accept()
        with conn:
            print(f"Conectado por {addr}")
            while True:
                data = conn.recv(CHUNK)
                if not data:
                    break
                wf.writeframes(data)

    wf.close()

start_audio_server()
