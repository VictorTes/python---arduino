import time
import serial
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from comtypes import CLSCTX_ALL
import pyautogui

# Inicia comunicação serial
ser = serial.Serial("COM3", 115200, timeout=1)
time.sleep(2)  # Espera o Arduino resetar

# Inicializa o controle de volume
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = interface.QueryInterface(IAudioEndpointVolume)

while True:
    try:
        line = ser.readline().decode('utf-8').strip()
        if line:
            # Verifica se é comando de música
            if line.startswith("CMD:"):
                cmd = line[4:]
                if cmd == "BACK":
                    print("Comando: Voltar música")
                    pyautogui.press('prevtrack')  # Tecla multimídia voltar música
                elif cmd == "PAUSE":
                    print("Comando: Pausar/Play")
                    pyautogui.press('playpause')  # Tecla multimídia pausar/reproduzir
                elif cmd == "NEXT":
                    print("Comando: Próxima música")
                    pyautogui.press('nexttrack')  # Tecla multimídia próxima música

            else:
                # Tenta interpretar como float para volume
                try:
                    pot_volume = float(line)
                    pot_volume = min(max(pot_volume, 0.0), 1.0)  # Garante faixa válida
                    volume.SetMasterVolumeLevelScalar(pot_volume, None)
                    print(f"Volume ajustado para: {pot_volume:.2f}")
                except ValueError:
                    print(f"Linha recebida inválida: {line}")
    except Exception as e:
        print("Erro:", e)
    time.sleep(0.05)
