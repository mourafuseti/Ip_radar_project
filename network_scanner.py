# network_scanner.py

from scapy.all import ARP, Ether, srp
import threading
import time
import netifaces 
import ipaddress 
import sys # Para tratar saídas de erro

# --- Variáveis Globais de Configuração ---
ACCEPTED_IPS = set()
SCAN_INTERVAL = 5 # Intervalo de scan em segundos

# --- Whitelist Manager ---

def load_accepted_ips(filename="accepted_ips.txt"):
    """Carrega a lista de IPs aceitos de um arquivo."""
    global ACCEPTED_IPS
    try:
        with open(filename, 'r') as f:
            # Usa um set para consultas rápidas
            ACCEPTED_IPS = {line.strip() for line in f if line.strip()}
    except FileNotFoundError:
        # Imprime no terminal, mas não deve parar a execução
        print("Arquivo 'accepted_ips.txt' não encontrado. Whitelist vazia.")

def check_ip_status(ip_address):
    """Retorna a cor e o status do IP com base na whitelist."""
    if ip_address in ACCEPTED_IPS:
        return "green", "Aceito"
    else:
        return "red", "ALERTA - Novo/Desconhecido"

# --- Detector de Gateway e Range ---

def get_network_range_from_gateway():
    """
    Descobre o endereço do gateway padrão e constrói o range de rede /24.
    """
    # Define um fallback em caso de falha na detecção
    FALLBACK_RANGE = "192.168.1.1/24" 
    
    try:
        gws = netifaces.gateways()
        
        # Tenta obter o IP do gateway padrão (AF_INET = IPv4)
        default_interface = gws['default'][netifaces.AF_INET]
        gateway_ip = default_interface[0]
        
        # Constrói o range /24 a partir do gateway (ex: 192.168.1.1 -> 192.168.1.0/24)
        network = ipaddress.ip_network(f'{gateway_ip}/24', strict=False)
        target_range = str(network) 
        
        print(f"✅ Range de rede detectado a partir do Gateway ({gateway_ip}): {target_range}")
        return target_range
        
    except Exception:
        # Captura KeyError se 'default' ou 'AF_INET' não for encontrado,
        # ou falha ao processar o IP.
        print(f"⚠️ AVISO: Não foi possível detectar o gateway padrão. Usando fallback: {FALLBACK_RANGE}")
        return FALLBACK_RANGE


# --- Network Scanner ---

def scan_network(target_ip_range):
    """
    Realiza o ARP scan na rede e retorna a lista de hosts ativos com status de cor.
    """
    load_accepted_ips() # Recarrega a whitelist a cada scan

    # Cria o pacote ARP
    ether_frame = Ether(dst="ff:ff:ff:ff:ff:ff") 
    arp_request = ARP(pdst=target_ip_range)
    packet = ether_frame / arp_request

    hosts_list = []
    
    try:
        # Envia e recebe a resposta (o timeout é baixo para scans frequentes)
        answered_list, unanswered_list = srp(packet, timeout=1, verbose=False)

        # Processa a resposta
        for sent, received in answered_list:
            ip = received.psrc
            mac = received.hwsrc
            
            # Classifica o IP (Verde ou Vermelho)
            color, status = check_ip_status(ip) 
            
            hosts_list.append({
                'IP': ip, 
                'MAC': mac,
                'StatusColor': color,
                'StatusText': status
            })
            
    except Exception as e:
        # Captura qualquer erro de rede/driver que causaria o crash do processo
        # (incluindo erros de permissão do Scapy)
        print("\n" + "="*50)
        print("❌ ERRO GRAVE DE SCAN NA REDE! O SCAN FALHOU.")
        print(f"   Detalhamento do Erro: {e}")
        print("   CAUSA PROVÁVEL: Permissão de Administrador ou Driver de Rede (Npcap).")
        print("="*50 + "\n")
        # Retorna lista vazia para que o radar não trave
        return []

    return hosts_list

# --- Threading para varredura em background ---

class ScannerThread(threading.Thread):
    def __init__(self, target_ip_range, update_callback):
        threading.Thread.__init__(self)
        
        # 1. Se o range passado for o padrão (fallback), tenta detectar o gateway
        if target_ip_range == "192.168.1.1/24":
             self.target_ip_range = get_network_range_from_gateway()
        else:
             self.target_ip_range = target_ip_range
             
        self.update_callback = update_callback
        self.running = True

    def run(self):
        # Loop de scan contínuo
        while self.running:
            # Realiza o scan
            hosts = scan_network(self.target_ip_range)
            
            # Chama a função na UI para atualizar os dados
            self.update_callback(hosts)
            
            # Espera o intervalo antes do próximo scan
            time.sleep(SCAN_INTERVAL) 

    def stop(self):
        self.running = False