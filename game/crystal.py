import arcade

class Crystal(arcade.Sprite):
    """Кристалл для сбора."""
    
    def __init__(self, x: float, y: float):
        super().__init__(
            ":resources:/images/items/gemBlue.png",
            scale=0.7
        )
        self.center_x = x
        self.center_y = y
        self.collect_sound = arcade.load_sound(":resources:/sounds/coin5.wav")
        
    def collect(self, particle_system, x: float, y: float) -> None:
        """Сбор кристалла с визуальным эффектом."""
        arcade.play_sound(self.collect_sound)
        # Запуск частиц в точке кристалла
        if particle_system:
            particle_system.center_x = x
            particle_system.center_y = y
            particle_system.rate = 1.0
        self.remove_from_sprite_lists()
