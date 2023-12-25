import pygame

from StateMachine import GameState


class GameLoop:
    def __init__(self, game):
        self.game = game
        self.initialized = False

    def start(self):
        """
        Выполняет первоначальную настройку уровня, например инициализацию спрайтов.
        """

    def update(self):
        """
        Вызывается каждый кадр.
        """

    def handle_event(self, event):
        """
        Обрабатывает одиночный ивент.
        """

    def loop(self):
        if not self.initialized:
            self.start()
            self.initialized = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.set_state(GameState.QUITTING)

            self.handle_event(event)

        self.update()

    # Методы для удобства
    def set_state(self, new_state: GameState):
        self.game.state_machine.set_state(new_state)

    @property
    def state(self) -> GameState:
        return self.game.state_machine.state

    @property
    def all_sprites(self) -> pygame.sprite.Group:
        return self.game.all_sprites

    @property
    def screen(self) -> pygame.Surface:
        return self.game.screen

    @property
    def width(self) -> int:
        return self.game.width

    @property
    def height(self) -> int:
        return self.game.height

    @property
    def clock(self) -> pygame.time.Clock:
        return self.game.clock


class MainMenuLoop(GameLoop):
    def start(self):
        import Sprites
        self.all_sprites.empty()
        Sprites.MainMenuBackground(self.all_sprites)
        Sprites.CloudsSprite(self.all_sprites, x=150, y=120)
        Sprites.PlayerSprite(self.all_sprites, x=100, y=300)
        Sprites.BirdSprite(self.all_sprites, x=960, y=200)
        Sprites.GameNameSprite(self.all_sprites, x=420, y=10)

    def update(self):
        self.all_sprites.draw(self.screen)
        pygame.display.flip()

    def handle_event(self, event):
        pass  # TODO обработка кнопок


class MainGameLoop(GameLoop):
    def start(self):
        pass

    def update(self):
        pass

    def handle_event(self, event):
        pass
