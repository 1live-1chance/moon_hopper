import arcade

class HUD:
    """Игровой интерфейс (HUD)."""
    
    def __init__(self):
        self.font_name = ":resources:/fonts/kenney_fonts/kenney_pixel.ttf"
        
    def draw(self, score: int, time_left: float, high_score: int) -> None:
        """Отрисовка элементов интерфейса."""
        # Счёт
        arcade.draw_text(
            f"Счёт: {score}",
            10,
            570,
            arcade.color.WHITE,
            18,
            font_name=self.font_name
        )
        
        # Таймер
        arcade.draw_text(
            f"Время: {max(0, int(time_left))}",
            10,
            545,
            arcade.color.WHITE,
            18,
            font_name=self.font_name
        )
        
        # Рекорд
        arcade.draw_text(
            f"Рекорд: {high_score}",
            650,
            570,
            arcade.color.YELLOW,
            18,
            font_name=self.font_name
        )
