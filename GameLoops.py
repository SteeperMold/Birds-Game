import pygame

from StateMachine import GameState


class GameLoop:
    def __init__(self, game):
        self.game = game
        self.initialized = False

    def init(self):
        """
        Выполняет первоначальную настройку уровня, например инициализацию спрайтов.
        """

    def loop(self):
        if not self.initialized:
            self.init()
            self.initialized = True

        self.handle_events()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.set_state(GameState.QUITTING)

            self.handle_event(event)

    def handle_event(self, event):
        """
        Обрабатывает одиночный ивент.
        """

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
    def width(self):
        return self.game.width

    @property
    def height(self):
        return self.game.height


class MainMenuLoop(GameLoop):
    def init(self):
        from Sprites import MainMenuBackground, PlayerSprite, GameNameSprite, CloudsSprite, BirdSprite
        self.all_sprites.empty()
        MainMenuBackground(self.all_sprites)
        CloudsSprite(self.all_sprites, x=150, y=120)
        PlayerSprite(self.all_sprites, x=100, y=300)
        BirdSprite(self.all_sprites, x=960, y=200)
        GameNameSprite(self.all_sprites, x=420, y=10)

    def handle_event(self, event):
        pass


class MainGameLoop(GameLoop):
    pass
