import arcade
from enum import Enum
from game.player import Player
from game.level import Level
from game.camera_controller import CameraController
from ui.hud import HUD
from ui.button import TextButton
from data.score_manager import ScoreManager

class GameState(Enum):
    MENU = 0
    GAME = 1
    GAME_OVER = 2

class GameWindow(arcade.Window):
    """Основное окно игры."""
    
    def __init__(self, width: int, height: int, title: str):
        super().__init__(width, height, title)
        self.state: GameState = GameState.MENU
        self.player: Player | None = None
        self.level: Level | None = None
        self.camera: CameraController | None = None
        self.hud: HUD | None = None
        self.score_manager: ScoreManager | None = None
        self.score: int = 0
        self.time_left: float = 60.0
        self.start_button: TextButton | None = None
        self.restart_button: TextButton | None = None
        
    def setup(self) -> None:
        """Инициализация всех игровых объектов."""
        # Загрузка рекорда
        self.score_manager = ScoreManager()
        self.score_manager.load_high_score()
        
        # Создание игрока и уровня
        self.player = Player()
        self.level = Level()
        self.level.setup(self.player)
        
        # Камера и интерфейс
        self.camera = CameraController(self, self.player)
        self.hud = HUD()
        
        # Кнопки
        self.start_button = TextButton(
            center_x=self.width // 2,
            center_y=self.height // 2,
            text="Старт",
            action=self.switch_to_game
        )
        self.restart_button = TextButton(
            center_x=self.width // 2,
            center_y=self.height // 2 - 50,
            text="Заново",
            action=self.switch_to_game
        )
        
        # Сброс состояния
        self.score = 0
        self.time_left = 60.0
        self.state = GameState.MENU
        
    def on_draw(self) -> None:
        """Отрисовка всей сцены."""
        self.clear()
        
        if self.state == GameState.GAME:
            # Игровая камера
            self.camera.use_game_camera()
            self.level.draw()
            self.player.draw()
            
            # Камера интерфейса
            self.camera.use_gui_camera()
            self.hud.draw(self.score, self.time_left, self.score_manager.high_score)
            
        elif self.state == GameState.MENU:
            arcade.draw_text(
                "Лунный Скачок",
                self.width // 2,
                self.height // 2 + 100,
                arcade.color.WHITE,
                36,
                anchor_x="center",
                font_name=":resources:/fonts/kenney_fonts/kenney_pixel.ttf"
            )
            self.start_button.draw()
            
        elif self.state == GameState.GAME_OVER:
            arcade.draw_text(
                "Игра окончена!",
                self.width // 2,
                self.height // 2 + 50,
                arcade.color.WHITE,
                36,
                anchor_x="center",
                font_name=":resources:/fonts/kenney_fonts/kenney_pixel.ttf"
            )
            arcade.draw_text(
                f"Счёт: {self.score}",
                self.width // 2,
                self.height // 2,
                arcade.color.WHITE,
                24,
                anchor_x="center",
                font_name=":resources:/fonts/kenney_fonts/kenney_pixel.ttf"
            )
            arcade.draw_text(
                f"Рекорд: {self.score_manager.high_score}",
                self.width // 2,
                self.height // 2 - 30,
                arcade.color.YELLOW,
                20,
                anchor_x="center",
                font_name=":resources:/fonts/kenney_fonts/kenney_pixel.ttf"
            )
            self.restart_button.draw()
    
    def on_update(self, delta_time: float) -> None:
        """Обновление логики игры."""
        if self.state != GameState.GAME:
            return
            
        # Обновление времени
        self.time_left -= delta_time
        if self.time_left <= 0:
            self.switch_to_game_over()
            return
            
        # Обновление игрока и уровня
        self.player.update()
        self.level.update(delta_time, self.player)
        
        # Обновление камеры
        self.camera.update()
        
        # Проверка сбора кристаллов
        crystals_hit = arcade.check_for_collision_with_list(
            self.player, self.level.crystals
        )
        for crystal in crystals_hit:
            crystal.collect(self.level.particle_system, crystal.center_x, crystal.center_y)
            self.score += 10
            
        # Проверка столкновения с метеоритами
        if arcade.check_for_collision_with_list(self.player, self.level.meteors):
            self.switch_to_game_over()
    
    def on_key_press(self, key: int, modifiers: int) -> None:
        """Обработка нажатий клавиш."""
        if self.state != GameState.GAME:
            return
            
        if key == arcade.key.SPACE:
            self.player.jump()
    
    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int) -> None:
        """Обработка кликов мыши для кнопок."""
        if button != arcade.MOUSE_BUTTON_LEFT:
            return
            
        if self.state == GameState.MENU and self.start_button:
            self.start_button.on_click(x, y)
        elif self.state == GameState.GAME_OVER and self.restart_button:
            self.restart_button.on_click(x, y)
    
    def switch_to_game(self) -> None:
        """Переход в игровое состояние."""
        self.setup()  # Пересоздаём уровень и игрока
        self.state = GameState.GAME
    
    def switch_to_game_over(self) -> None:
        """Переход в состояние окончания игры."""
        # Сохранение рекорда
        if self.score > self.score_manager.high_score:
            self.score_manager.high_score = self.score
            self.score_manager.save_high_score()
        self.state = GameState.GAME_OVER
