import sys
import threading
import time

# Importações dos seus módulos da GUI
from PySide6.QtWidgets import QApplication, QStackedWidget
from gui.main_window import MinhaJanela
from gui.shuffler_window import GameModeWidget
from gui.dealer_window import ContadorWidget
from gui.match_window import GameSetupWindow
from gui.scoreboard_window import ScoreboardWindow

# Importação da função do serviço de base de dados
from services.database_writer import start_database_service


if __name__ == "__main__":
    # --- PARTE 1: INICIAR O SERVIÇO EM SEGUNDO PLANO ---
    print("A iniciar a aplicação...")

    # Cria e inicia a thread para o serviço da base de dados
    service_thread = threading.Thread(target=start_database_service, daemon=True)
    service_thread.start()
    
    # Aguarda um momento para a conexão MQTT ser estabelecida
    print("A iniciar o serviço de base de dados, por favor aguarde...")
    time.sleep(3)
    
    # --- PARTE 2: INICIAR A INTERFACE GRÁFICA ---
    print("A iniciar a interface gráfica...")
    
    app = QApplication(sys.argv)
    
    stacked_widget = QStackedWidget()
    stacked_widget.setWindowTitle("Embaralhador de Cartas")
    stacked_widget.resize(800, 480)

    # Cria as instâncias das suas telas
    main_page = MinhaJanela(stacked_widget)
    shuffler_page = GameModeWidget(stacked_widget)
    dealer_page = ContadorWidget(stacked_widget)
    match_page = GameSetupWindow(stacked_widget)
    scoreboard_page = ScoreboardWindow(stacked_widget)

    # Adiciona as telas ao QStackedWidget
    stacked_widget.addWidget(main_page)       # index 0
    stacked_widget.addWidget(shuffler_page)   # index 1
    stacked_widget.addWidget(dealer_page)     # index 2
    stacked_widget.addWidget(match_page)      # index 3
    stacked_widget.addWidget(scoreboard_page) # index 4

    def start_match():
        # Pega os nomes da tela de configuração
        team1 = match_page.team1_input.text()
        team2 = match_page.team2_input.text()
        
        # Acedendo ao índice do carrossel diretamente
        game_mode_index = match_page.current_game_mode_index
        
        # Chama o método para configurar o placar
        scoreboard_page.setup_match(team1, team2, game_mode_index)
        
        # Muda para a tela do placar
        stacked_widget.setCurrentWidget(scoreboard_page)

    # Conecta os sinais dos botões para a navegação
    main_page.shuffle_button.clicked.connect(lambda: stacked_widget.setCurrentIndex(1))
    main_page.deal_button.clicked.connect(lambda: stacked_widget.setCurrentIndex(2))
    
    if hasattr(main_page, 'match_button'):
        main_page.match_button.clicked.connect(lambda: stacked_widget.setCurrentIndex(3))

    shuffler_page.back_button.clicked.connect(lambda: stacked_widget.setCurrentIndex(0))
    dealer_page.back_button.clicked.connect(lambda: stacked_widget.setCurrentIndex(0))
    match_page.back_button.clicked.connect(lambda: stacked_widget.setCurrentIndex(0))
    # Botão voltar do placar deve voltar para a tela de configuração
    scoreboard_page.back_button.clicked.connect(lambda: stacked_widget.setCurrentIndex(3)) 

    match_page.start_button.clicked.connect(start_match)

    # Exibe a janela principal
    stacked_widget.show()
    sys.exit(app.exec())