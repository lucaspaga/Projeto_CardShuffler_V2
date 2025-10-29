import sys
import threading
import time

from PySide6.QtWidgets import QApplication, QStackedWidget
from gui.main_window import MinhaJanela
from gui.shuffler_window import GameModeWidget
from gui.dealer_window import ContadorWidget
from gui.match_window import GameSetupWindow
from gui.scoreboard_window import ScoreboardWindow

from services.database_writer import start_database_service


if __name__ == "__main__":
    print("A iniciar a aplicação...")

    service_thread = threading.Thread(target=start_database_service, daemon=True)
    service_thread.start()
    
    print("A iniciar o serviço de base de dados, por favor aguarde...")
    time.sleep(3)
    
    print("A iniciar a interface gráfica...")
    
    app = QApplication(sys.argv)
    
    stacked_widget = QStackedWidget()
    stacked_widget.setWindowTitle("Embaralhador de Cartas")
    stacked_widget.resize(800, 480)

    main_page = MinhaJanela(stacked_widget)
    shuffler_page = GameModeWidget(stacked_widget)
    dealer_page = ContadorWidget(stacked_widget)
    match_page = GameSetupWindow(stacked_widget)
    scoreboard_page = ScoreboardWindow(stacked_widget)

    stacked_widget.addWidget(main_page)       
    stacked_widget.addWidget(shuffler_page)   
    stacked_widget.addWidget(dealer_page)     
    stacked_widget.addWidget(match_page)      
    stacked_widget.addWidget(scoreboard_page) 

    def start_match():
        team1 = match_page.team1_input.text()
        team2 = match_page.team2_input.text()
        
        game_mode_index = match_page.current_game_mode_index
        scoreboard_page.setup_match(team1, team2, game_mode_index)
        stacked_widget.setCurrentWidget(scoreboard_page)

    main_page.shuffle_button.clicked.connect(lambda: stacked_widget.setCurrentIndex(1))
    main_page.deal_button.clicked.connect(lambda: stacked_widget.setCurrentIndex(2))
    
    if hasattr(main_page, 'match_button'):
        main_page.match_button.clicked.connect(lambda: stacked_widget.setCurrentIndex(3))

    shuffler_page.back_button.clicked.connect(lambda: stacked_widget.setCurrentIndex(0))
    dealer_page.back_button.clicked.connect(lambda: stacked_widget.setCurrentIndex(0))
    match_page.back_button.clicked.connect(lambda: stacked_widget.setCurrentIndex(0))
    scoreboard_page.back_button.clicked.connect(lambda: stacked_widget.setCurrentIndex(3)) 

    match_page.start_button.clicked.connect(start_match)

    stacked_widget.show()
    sys.exit(app.exec())