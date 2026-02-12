import arcade

class TextButton:
    """Простая текстовая кнопка."""
    
    def __init__(
        self,
        center_x: int,
        center_y: int,
        text: str,
        action
    ):
        self.center_x = center_x
        self.center_y = center_y
        self.text = text
        self.action = action
        self.width = 200
        self.height = 50
        self.font_size = 24
        self.font_name = ":resources:/fonts/kenney_fonts/kenney_pixel.ttf"
        
    def draw(self) -> None:
        """Отрисовка кнопки."""
        # Фон кнопки
        arcade.draw_rectangle_filled(
            self.center_x,
            self.center_y,
            self.width,
            self.height,
            arcade.color.DARK_GRAY
        )
        arcade.draw_rectangle_outline(
            self.center_x,
            self.center_y,
            self.width,
            self.height,
            arcade.color.WHITE,
            2
        )
        # Текст
        arcade.draw_text(
            self.text,
            self.center_x,
            self.center_y,
            arcade.color.WHITE,
            self.font_size,
            anchor_x="center",
            anchor_y="center",
            font_name=self.font_name
        )
    
    def on_click(self, x: int, y: int) -> None:
        """Проверка попадания по кнопке и выполнение действия."""
        if (self.center_x - self.width/2 < x < self.center_x + self.width/2 and
            self.center_y - self.height/2 < y < self.center_y + self.height/2):
            if self.action:
                self.action()
