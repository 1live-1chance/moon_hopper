import arcade

class Meteor(arcade.Sprite):
    """Опасный метеорит."""
    
    def __init__(self, x: float, speed: float):
        super().__init__(
            ":resources:/images/space_shooter/meteorGrey_big1.png",
            scale=0.6
        )
        self.center_x = x
        self.center_y = 650  # Начинает падение сверху экрана
        self.speed = speed
        
    def update(self) -> None:
        """Падение метеорита вниз."""
        self.center_y -= self.speed
        
        # Удаление при выходе за экран
        if self.center_y < -50:
            self.remove_from_sprite_lists()
