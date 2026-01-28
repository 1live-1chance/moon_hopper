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
        self.change_x = 0
        self.jump_sound = arcade.load_sound(":resources:/sounds/jump1.wav")
        self.is_on_ground = False
        
    def update(self) -> None:
        """Применение лунной гравитации и обновление позиции."""
        # Слабая гравитация Луны
        if not self.is_on_ground:
            self.change_y -= 0.4
        
        # Ограничение скорости падения
        if self.change_y < -12:
            self.change_y = -12
            
        self.center_y += self.change_y
        self.center_x += self.change_x
        
        # Горизонтальные границы уровня
        if self.left < 0:
            self.left = 0
        elif self.right > 2000:
            self.right = 2000
    
    def jump(self) -> None:
        """Выполнение прыжка при условии контакта с поверхностью."""
        if self.is_on_ground:
            self.change_y = 12  # Высокий прыжок из-за слабой гравитации
            self.is_on_ground = False
            arcade.play_sound(self.jump_sound)
