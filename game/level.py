import arcade
import random
from game.player import Player
from game.crystal import Crystal
from game.meteor import Meteor

class Level:
    """Игровой уровень с ландшафтом и объектами."""
    
    def __init__(self):
        self.ground_list: arcade.SpriteList = arcade.SpriteList()
        self.platform_list: arcade.SpriteList = arcade.SpriteList()
        self.crystals: arcade.SpriteList = arcade.SpriteList()
        self.meteors: arcade.SpriteList = arcade.SpriteList()
        self.particle_system: arcade.ParticleEmitter | None = None
        self.meteor_timer: float = 0.0
        
    def setup(self, player: Player) -> None:
        """Генерация ландшафта и объектов."""
        # Создание земли
        for x in range(0, 2000, 64):
            ground = arcade.Sprite(
                ":resources:/images/tiles/grassMid.png",
                scale=1.0
            )
            ground.center_x = x
            ground.center_y = 32
            self.ground_list.append(ground)
            
        # Создание платформ
        platform_positions = [(300, 150), (500, 250), (700, 200), (900, 300)]
        for x, y in platform_positions:
            platform = arcade.Sprite(
                ":resources:/images/tiles/grassHalf.png",
                scale=1.0
            )
            platform.center_x = x
            platform.center_y = y
            self.platform_list.append(platform)
            
        # Создание кристаллов
        for _ in range(8):
            crystal = Crystal(
                x=random.randint(100, 1800),
                y=random.randint(100, 400)
            )
            self.crystals.append(crystal)
            
        # Система частиц для эффектов
        self.particle_system = arcade.ParticleEmitter(
            center_xy=(0, 0),
            change_xy=arcade.rand_vec_spread_deg(90, 45, 5.0),
            emit_controller=arcade.EmitterIntervalWithTime(0.02, 0.5),
            particle_factory=lambda emitter: arcade.FadeParticle(
                filename_or_texture=":resources:/images/particles/star.png",
                change_xy=arcade.rand_vec_spread_deg(90, 10, 2.0),
                lifetime=1.0,
                scale=0.3,
                alpha=128
            )
        )
    
    def draw(self) -> None:
        """Отрисовка всех элементов уровня."""
        self.ground_list.draw()
        self.platform_list.draw()
        self.crystals.draw()
        self.meteors.draw()
        if self.particle_system:
            self.particle_system.draw()
    
    def update(self, delta_time: float, player: Player) -> None:
        """Обновление объектов уровня."""
        # Обновление метеоритов
        self.meteors.update()
        
        # Генерация новых метеоритов
        self.meteor_timer += delta_time
        if self.meteor_timer >= 2.0:
            self.meteor_timer = 0.0
            meteor = Meteor(
                x=random.randint(50, 750),
                speed=random.uniform(3.0, 6.0)
            )
            self.meteors.append(meteor)
            
        # Обновление частиц
        if self.particle_system:
            self.particle_system.update()
            
        # Проверка контакта игрока с платформами
        player.is_on_ground = False
        if arcade.check_for_collision_with_list(player, self.ground_list):
            player.is_on_ground = True
            player.center_y = 64  # Высота земли + половина спрайта
            
        for platform in self.platform_list:
            if (player.bottom <= platform.top + 10 and 
                player.bottom >= platform.top - 5 and
                platform.left - 30 <= player.center_x <= platform.right + 30):
                player.is_on_ground = True
                player.center_y = platform.top + 32  # 32 = половина высоты спрайта игрока
