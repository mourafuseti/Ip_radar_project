# 👋🏻 Leonardo de Moura Fuseti

Estudante de Defesa Cibernetica no Polo Estacio Piumhi MG . Formação tecnica em Tecnico em Redes de Computadores no IFMG Bambui MG , intusiasta na programação gostando muito de Python e evoluindo dia a dia .

### Conecte-se comigo

[![Perfil DIO](https://img.shields.io/badge/-Meu%20Perfil%20na%20DIO-30A3DC?style=for-the-badge)](https://www.dio.me/users/mourafuseti)
[![E-mail](https://img.shields.io/badge/-Email-000?style=for-the-badge&logo=microsoft-outlook&logoColor=E94D5F)](mailto:mourafuseti@gmail.com)
[![LinkedIn](https://img.shields.io/badge/-LinkedIn-000?style=for-the-badge&logo=linkedin&logoColor=30A3DC)](https://www.linkedin.com/in/leonardo-moura-fuseti-4052b0359/)

### Habilidades

![HTML](https://img.shields.io/badge/HTML-000?style=for-the-badge&logo=html5&logoColor=30A3DC)
![CSS3](https://img.shields.io/badge/CSS3-000?style=for-the-badge&logo=css3&logoColor=E94D5F)
![JavaScript](https://img.shields.io/badge/JavaScript-000?style=for-the-badge&logo=javascript&logoColor=F0DB4F)
![Sass](https://img.shields.io/badge/SASS-000?style=for-the-badge&logo=sass&logoColor=CD6799)
![Bootstrap](https://img.shields.io/badge/bootstrap-000?style=for-the-badge&logo=bootstrap&logoColor=553C7B)
[![Git](https://img.shields.io/badge/Git-000?style=for-the-badge&logo=git&logoColor=E94D5F)](https://git-scm.com/doc)
[![GitHub](https://img.shields.io/badge/GitHub-000?style=for-the-badge&logo=github&logoColor=30A3DC)](https://docs.github.com/)

### GitHub Stats

![GitHub Stats](https://github-readme-stats.vercel.app/api?username=mourafuseti&theme=transparent&bg_color=000&border_color=30A3DC&show_icons=true&icon_color=30A3DC&title_color=E94D5F&text_color=FFF)


## 🚀 README: Radar de Rede em Tempo Real com Python

Este projeto implementa um "Radar" de IPs em tempo real, permitindo a **varredura (scan)** de uma rede local (ex: `192.168.1.0/24`) e a **visualização** dos *hosts* ativos em uma interface gráfica estilo radar (utilizando **Tkinter**).

A principal funcionalidade de segurança é o sistema de **Whitelist** (lista de IPs aceitos), que identifica e destaca (em vermelho) qualquer dispositivo **novo ou desconhecido** que se conecte à rede.

-----

## 🛠️ Requisitos e Dependências

Para que o projeto funcione corretamente, você precisa do Python 3 e das seguintes bibliotecas:

| Biblioteca | Função | Instalação |
| :--- | :--- | :--- |
| **Scapy** | Faz o *ARP scan* de rede de baixo nível. | `pip install scapy` |
| **simpleaudio** | Reprodução de som (o "blip" do radar). | `pip install simpleaudio` |
| **netifaces** | Detecção automática do *gateway* da rede. | `pip install netifaces` |
| **ipaddress** | Manipulação de endereços IP. | `pip install ipaddress` (geralmente embutido) |

> ⚠️ **IMPORTANTE:** No **Windows**, o Scapy exige que o driver **Npcap** esteja instalado. O aplicativo deve ser executado no PowerShell como **Administrador** para acessar a camada de rede.

-----

## 📂 Estrutura do Projeto

O projeto é modularizado para separar a lógica de rede da interface gráfica e dos dados:

```
/ip_radar_project/
├── main.py             # Ponto de entrada que inicializa a aplicação.
├── radar_app.py        # Módulo da Interface Gráfica (Frontend Tkinter).
├── network_scanner.py  # Módulo de Backend (Scapy, netifaces, Whitelist).
├── accepted_ips.txt    # Arquivo de dados: Whitelist de IPs conhecidos.
├── radar_blip.wav      # Arquivo de áudio para o alerta (o "blip").
└── README.md           # Este arquivo.
```

-----

## ⚙️ Configuração e Execução

### 1\. Configurar Whitelist (`accepted_ips.txt`)

Edite o arquivo `accepted_ips.txt` e adicione todos os endereços IP confiáveis e conhecidos da sua rede (um por linha):

```text
192.168.1.1
192.168.1.100
192.168.1.254
```

### 2\. Definir a Faixa de Rede (Opcional)

Por padrão, o `network_scanner.py` tenta **detectar o *gateway*** e definir a faixa de scan para `/24`.

Se a detecção falhar, ele usará o *fallback* `192.168.1.1/24`. Você pode ajustar a variável `TARGET_NETWORK_FALLBACK` no `main.py` se souber o endereço exato da sua rede.

### 3\. Rodar o Aplicativo

#### Linux/macOS (Recomendado)

Use `sudo` para garantir as permissões de rede:

```bash
sudo python3 main.py
```

#### Windows (PowerShell)

1.  **Abra o PowerShell como Administrador.**
2.  Navegue até o diretório do projeto.
3.  Use o *launcher* do Python com a versão que você usou para instalar as dependências (ex: 3.13):

<!-- end list -->

```powershell
py -3.13 main.py
```

-----

## ✨ Funcionalidades

| Funcionalidade | Detalhe |
| :--- | :--- |
| **Varredura Contínua** | O scanner roda em uma *thread* de *background* e repete o scan a cada **5 segundos** (definido em `network_scanner.py`). |
| **Identificação Visual** | **Verde:** IPs que estão na Whitelist (`accepted_ips.txt`). **Vermelho:** IPs desconhecidos (alerta de novo dispositivo na rede). |
| **Alerta Sonoro** | Um som de "blip" é reproduzido (usando `simpleaudio`) **apenas** quando um host que **não estava** presente no scan anterior é detectado. |
| **Visualização de Radar** | Interface em tempo real que exibe os *hosts* ativos no painel de detalhes e como "blips" no gráfico circular. |
