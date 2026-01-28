import arcade

class CameraController:
    """Контроллер игровой камеры."""
    
    def __init__(self, window: arcade.Window, player: arcade.Sprite):
        self.window = window
        self.player = player
        self.camera = arcade.Camera(window.width, window.height)
        self.gui_camera = arcade.Camera(window.width, window.height)
        
    def update(self) -> None:
        """Плавное следование камеры за игроком."""
        # Центрирование камеры по игроку с ограничениями
        camera_x = self.player.center_x - self.window.width / 2
        camera_y = self.player.center_y - self.window.height / 2
        
        # Ограничение по краям уровня
        camera_x = max(0, min(camera_x, 2000 - self.window.width))
        camera_y = max(0, min(camera_y, 500 - self.window.height))
        
        self.camera.move_to((camera_x, camera_y), 0.1)
    
    def use(self) -> None:
        """Активация игровой камеры."""
        self.camera.use()
        
    def gui_camera_use(self) -> None:
        """Активация камеры интерфейса."""
        self.gui_camera.use()
