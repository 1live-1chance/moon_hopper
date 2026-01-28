import arcade
from game.window import GameWindow

def main():
    """Запуск игры."""
    window = GameWindow(
        width=800,
        height=600,
        title="Лунный Скачок"
    )
    window.setup()
    arcade.run()

if __name__ == "__main__":
    main()
