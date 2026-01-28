import arcade

class Player(arcade.Sprite):
    """Управляемый луноход."""
    
    def __init__(self):
        # Используем встроенный спрайт корабля (стилизован под луноход)
        super().__init__(
            ":resources:/images/space_shooter/playerShip1_orange.png",
            scale=0.5
        )
        self.center_x = 100
        self.center_y = 100
        self.change_y = 0
        self.jump_sound = arcade.load_sound(":resources:/sounds/jump1.wav")
        self.is_on_ground = False
        
    def update(self) -> None:
        """Применение лунной гравитации."""
        # Слабая гравитация Луны
        self.change_y -= 0.3
        
        # Ограничение скорости падения
        if self.change_y < -10:
            self.change_y = -10
            
        self.center_y += self.change_y
        
        # Проверка приземления (будет реализована в Level)
        if self.center_y < 64:
            self.center_y = 64
            self.change_y = 0
            self.is_on_ground = True
    
    def jump(self) -> None:
        """Выполнение прыжка при условии контакта с поверхностью."""
        if self.is_on_ground:
            self.change_y = 12  # Высокий прыжок из-за слабой гравитации
            self.is_on_ground = False
            arcade.play_sound(self.jump_sound)
