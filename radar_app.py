# radar_app.py

import tkinter as tk
import math
import threading 
# import simpleaudio as sa # REMOVIDO: Biblioteca de reprodução de som
# import time # REMOVIDO: Necessário para o sleep

# Importa a classe do scanner de rede
try:
    from network_scanner import ScannerThread 
except ImportError:
    # Esta mensagem será exibida se houver erro no network_scanner.py
    print("ERRO: Não foi possível importar network_scanner.py. Verifique o nome do arquivo.")
    exit()

class IPRadarApp:
    def __init__(self, master, target_ip_range="192.168.1.1/24"):
        """
        Inicializa a aplicação do Radar de IP e a interface gráfica.
        """
        self.master = master
        master.title("📡 Radar de Rede em Tempo Real")
        
        # --- Configurações de Estado ---
        self.known_ips = set() 
        # REMOVIDO: self.BLIP_SOUND_FILE, self.wave_obj, self.sound_lock
        # REMOVIDO: try/except para carregar o arquivo de som
        
        # --- Configurações do Radar e UI ---
        self.CANVAS_SIZE = 600
        self.CENTER_X = self.CANVAS_SIZE / 2
        self.CENTER_Y = self.CANVAS_SIZE / 2
        self.MAX_RADIUS = (self.CANVAS_SIZE / 2) - 40 
        self.sweep_angle = 0 
        self.sweep_id = None
        self.active_hosts = [] 
        
        # --- Configuração do Tkinter Canvas (Radar) ---
        self.canvas = tk.Canvas(master, width=self.CANVAS_SIZE, height=self.CANVAS_SIZE, bg="black")
        self.canvas.pack(padx=10, pady=10)
        
        # --- Interface de Status e Logs ---
        self.status_label = tk.Label(master, text="Iniciando Scanner...", bg="#333333", fg="white", 
                                     font=('Consolas', 10), justify=tk.LEFT, anchor='w')
        self.status_label.pack(fill='x', pady=(0, 10))
        
        # --- Inicializa o Visual ---
        self._draw_radar_grid()
        self._animate_sweep()
        
        # --- Inicializa o Scanner em Background ---
        self.scanner_thread = ScannerThread(target_ip_range, self.update_radar_data)
        self.scanner_thread.start()
        
        # --- Configura o encerramento seguro ---
        master.protocol("WM_DELETE_WINDOW", self.on_closing)

    # --- Métodos de Reprodução de Som (REMOVIDOS) ---
    
    # O método _play_blip_sound foi removido completamente.

    # --- Métodos de Desenho e Animação (Visual) ---

    def _draw_radar_grid(self):
        """Desenha o círculo e as linhas de grade do radar."""
        
        self.canvas.create_oval(self.CENTER_X - self.MAX_RADIUS, self.CENTER_Y - self.MAX_RADIUS,
                                self.CENTER_X + self.MAX_RADIUS, self.CENTER_Y + self.MAX_RADIUS,
                                outline="#00FF00", width=2)

        for r_factor in [0.33, 0.66]:
            r = self.MAX_RADIUS * r_factor
            self.canvas.create_oval(self.CENTER_X - r, self.CENTER_Y - r,
                                    self.CENTER_X + r, self.CENTER_Y + r,
                                    outline="#00AA00", dash=(4, 4))
        
        for angle in range(0, 360, 30):
            rad = math.radians(angle)
            x_end = self.CENTER_X + self.MAX_RADIUS * math.cos(rad)
            y_end = self.CENTER_Y - self.MAX_RADIUS * math.sin(rad) 
            self.canvas.create_line(self.CENTER_X, self.CENTER_Y, x_end, y_end,
                                    fill="#00AA00", dash=(2, 2), width=1)
            
            if angle not in [90, 270]:
                x_text = self.CENTER_X + (self.MAX_RADIUS + 15) * math.cos(rad)
                y_text = self.CENTER_Y - (self.MAX_RADIUS + 15) * math.sin(rad)
                self.canvas.create_text(x_text, y_text, text=f"{angle}°", fill="#00FF00", 
                                        font=('Consolas', 8), tags="labels")


    def _animate_sweep(self):
        """Cria o efeito de varredura (sweep) rotativo."""
        
        self.canvas.delete("sweep")
        
        rad = math.radians(self.sweep_angle)
        x_end = self.CENTER_X + self.MAX_RADIUS * math.cos(rad)
        y_end = self.CENTER_Y - self.MAX_RADIUS * math.sin(rad)
        
        self.canvas.create_line(self.CENTER_X, self.CENTER_Y, x_end, y_end,
                                fill="#00FF00", width=3, tags="sweep")
        
        self.sweep_angle = (self.sweep_angle + 3) % 360
        
        self.sweep_id = self.master.after(50, self._animate_sweep)


    # --- Métodos de Atualização de Dados ---

    def update_radar_data(self, hosts):
        """
        Callback chamado pela thread do scanner para atualizar os dados do host.
        """
        self.active_hosts = hosts
        self.master.after(0, self._plot_hosts) 

    def _plot_hosts(self):
        """Plota os pontos (blips) dos hosts ativos no radar."""
        
        self.canvas.delete("blips")
        self.canvas.delete("ip_text")
        
        num_hosts = len(self.active_hosts)
        current_ips = set()
        
        # new_host_detected não é mais usado para som, mas pode ser mantido para logs futuros
        new_host_detected = False
        
        details_text = f"Hosts Ativos ({num_hosts}):\n"
        radius = self.MAX_RADIUS * 0.75 

        for i, host in enumerate(self.active_hosts):
            ip = host['IP']
            current_ips.add(ip)
            
            # --- Lógica de Deteção (Mantida para fins de log/visualização) ---
            if ip not in self.known_ips and host['StatusColor'] == 'red':
                new_host_detected = True 
            # ----------------------------------------------------------------
            
            plot_angle = (i * (360 / max(1, num_hosts))) % 360
            rad = math.radians(plot_angle)
            
            x = self.CENTER_X + radius * math.cos(rad)
            y = self.CENTER_Y - radius * math.sin(rad)

            fill_color = host['StatusColor'] 
            
            # Desenhar o Blip (Ponto)
            self.canvas.create_oval(x - 6, y - 6, x + 6, y + 6,
                                    fill=fill_color,
                                    outline="white",
                                    width=2,
                                    tags="blips")
            
            # Desenhar o texto do IP
            text_offset_angle = math.radians(plot_angle + 10) 
            text_x = self.CENTER_X + (radius + 15) * math.cos(text_offset_angle)
            text_y = self.CENTER_Y - (radius + 15) * math.sin(text_offset_angle)
            
            self.canvas.create_text(text_x, text_y, text=host['IP'], fill=fill_color, 
                                    font=('Consolas', 9, 'bold'), tags="ip_text")

            details_text += f"[{host['StatusText']:<10}] {host['IP']:<15} {host['MAC']}\n"

        # REMOVIDO: A chamada da thread de som
            
        # Atualiza a lista de hosts conhecidos para o próximo scan
        self.known_ips = current_ips
        
        # Atualiza o label de status
        self.status_label.config(text=details_text)
        
    # --- Método de Encerramento ---
    
    def on_closing(self):
        """Limpa as threads e encerra o aplicativo com segurança."""
        print("\n[INFO] Encerrando threads do scanner...")
        
        self.scanner_thread.stop()
        if self.scanner_thread.is_alive():
            self.scanner_thread.join(timeout=1)
        
        if self.sweep_id:
            self.master.after_cancel(self.sweep_id) 
        
        self.master.destroy()
