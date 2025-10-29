Projeto: Card Shuffler v2
==========================================================================
Este projeto é uma continução do projeto CardShufller, um embaralhador de cartas controlado por um Raspberry Pico. Dessa vezes tem-se uma solução completa de hardware e software para automatizar e gerir jogos de cartas, como o Truco. A aplicação central é executada num **Raspberry Pi 3**, que serve simultaneamente como a interface de controlo para o utilizador (GUI) e como a unidade de controlo para o hardware (motor do embaralhador).

1\. Visão Geral da Arquitetura
------------------------------

O sistema é desenhado para funcionar como uma estação de jogo autónoma:

1.  **Controlador Central:** Um **Raspberry Pi 3** executa a aplicação principal em Python.
    
2.  **Interface (GUI):** Uma aplicação **PySide6** (Qt) corre no Raspberry Pi (ligado a um monitor), permitindo aos utilizadores controlar tudo.
    
3.  **Controlo de Hardware:** A partir da GUI, os utilizadores podem acionar um **embaralhador de cartas físico**, controlado diretamente pelos pinos GPIO do Raspberry Pi através da biblioteca gpiozero.
    
4.  **Pipeline de Dados (Placar):**
    
    *   A GUI também funciona como um placar digital.
        
    *   Ao **Finalizar uma Partida**, a aplicação publica os resultados via **MQTT**.
        
    *   Um serviço em segundo plano (database\_writer.py), a correr no mesmo Pi, escuta o tópico MQTT.
        
    *   O serviço guarda os dados da partida numa base de dados **PostgreSQL** na nuvem.
        
5.  **Visualização (Dashboard):** A base de dados PostgreSQL está conectada ao **Google Looker Studio**, que fornece um dashboard para análise de partidas, pontuações e histórico.
    *  Link: https://lookerstudio.google.com/reporting/456ce03f-c7ff-4873-bf18-b3469851a2a4 
    
2\. Funcionalidades
-------------------

*   **Interface Unificada:** Um único ecrã controla o hardware e o software.
    
*   **Controlo de Hardware:** Lógica de embaralhamento de cargas que aciona um motor físico ligado ao Raspberry Pi.
    
*   **Placar Digital:** Gestão de pontuação com modos de jogo.
        
*   **Persistência de Dados na Nuvem:** Os resultados de cada partida são enviados via MQTT para um serviço que os armazena numa base de dados SQL remota.
    
*   **Análise de Dados:** O histórico de partidas é visualizado e analisado através de um dashboard no Looker Studio.
    

3\. Tecnologias e Bibliotecas
-----------------------------

A lista completa de bibliotecas está no ficheiro requirements.txt.

*   **Hardware:** Raspberry Pi 3
    
*   **Interface Gráfica (GUI):** PySide6 (PySide6\_Addons, PySide6\_Essentials, shiboken6)
    
*   **Controlo de Hardware:** gpiozero, colorzero
    
*   **Comunicação (Dados):** paho-mqtt
    
*   **Base de Dados:** PostgreSQL (driver: psycopg2-binary)
    
*   **Gestão de Configuração:** python-dotenv
    
*   **Visualização de Dados:** Google Looker Studio
    

4\. Como Executar o Projeto
---------------------------

### Passo 1: Pré-requisitos (Hardware)

1.  Um **Raspberry Pi 3** com o Raspberry Pi OS (com Desktop) instalado e ligado a um monitor e à internet.
    
2.  O circuito do embaralhador (motor, etc.) conectado corretamente aos pinos GPIO do Pi.
    

### Passo 2: Configurar a Base de Dados e o Dashboard

1.  Crie uma base de dados PostgreSQL gratuita em serviços como [Supabase](https://supabase.com/) ou [Neon](https://neon.tech/).
    
2.  ```
    CREATE TABLE matches (
    id SERIAL PRIMARY KEY,
    team1_name VARCHAR(255),
    team1_score INT,
    team2_name VARCHAR(255),
    team2_score INT,
    game_mode VARCHAR(50),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT\_TIMESTAMP);
    ```
    
3.  Aceda ao [Google Looker Studio](https://lookerstudio.google.com/) e crie uma nova fonte de dados, ligando-a à sua base de dados PostgreSQL.
    

### Passo 3: Configuração do Raspberry Pi

1.  Abra um terminal no seu Raspberry Pi.
    
2.  ```
    git clone \[URL\_DO\_SEU\_REPOSITORIO\]
    ```
3.  ```
    cd \[NOME\_DA\_PASTA\_DO\_PROJETO\]
    ```
4.   ```
     pip install -r requirements.txt
      ```
    
5.   ```
     nano .env
     ```
6.   ```
     DATABASE\_URL="postgres://seu\_usuario:sua\_senha@seu\_host:5432/sua\_database"
      ```
    

### Passo 4: Executar a Aplicação

Execute um único comando no terminal do Raspberry Pi. O script main.py foi configurado para iniciar o serviço da base de dados em segundo plano e, de seguida, abrir a aplicação gráfica.

 ```
 python main.py
 ```

A interface do placar e controlo do embaralhador irá aparecer no monitor do seu Raspberry Pi.

5\. Integrantes
---------------

| Nome | RA |
| ------------- | ------------- |
| Lucas Castanho Paganotto Carvalho  | 22.00921-3  |
| Tiago S. A. Barros  | 22.01117-0  |
| Felipe Massao Miranda Kamikawa | 22.00299-5
| Oliver K. Sauberli | 19.02220-4 |

6\.Video Explicativo
---------------
https://github.com/user-attachments/assets/c9a83dd4-e8fb-4255-b3db-8d3f14694a2b

7\.Equipe
---------------
![Imagem do WhatsApp de 2025-10-29 à(s) 19 24 03_cb5c4d38](https://github.com/user-attachments/assets/1a35ff0c-d4dd-4f1a-9fa2-c4b07d9b3da9)
