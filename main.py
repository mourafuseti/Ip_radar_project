# main.py

import tkinter as tk
from radar_app import IPRadarApp
import network_scanner 

def main():
    """
    Função principal que inicializa o aplicativo de Radar de Rede.
    """
    # Define um range padrão de fallback. O scanner tentará detectar o correto.
    TARGET_NETWORK_FALLBACK = "192.168.1.1/24" 
    
    root = tk.Tk()
    
    try:
        app = IPRadarApp(root, target_ip_range=TARGET_NETWORK_FALLBACK)
        print("[*] Radar de IP iniciado. Tentando detectar o gateway da rede.")
        
        root.mainloop()

    except Exception as e:
        print(f"ERRO CRÍTICO ao iniciar a aplicação: {e}")
        # ... mensagens de erro ...

if __name__ == "__main__":
    main()