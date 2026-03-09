import arcade
import random
import math

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "KittyRun"

GRAVITY = 0.5
PLAYER_JUMP_SPEED = 12
PLAYER_MOVEMENT_SPEED = 5
ATTACK_RANGE = 60

ORANGE = (255, 165, 0)
DARK_ORANGE = (200, 120, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
DARK_GRAY = (64, 64, 64)
BROWN = (139, 69, 19)
GREEN = (34, 139, 34)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
PINK = (255, 192, 203)
YELLOW = (255, 255, 0)
SKY_BLUE = (135, 206, 235)
BLACK_TRANSPARENT = (0, 0, 0, 150)
LIGHT_BROWN = (160, 82, 45)
DARK_BROWN = (101, 67, 33)
LIGHT_PINK = (255, 182, 193)
PURPLE = (128, 0, 128)


class Cat:
    IDLE = 0
    RUNNING = 1
    JUMPING = 2
    FALLING = 3
    ATTACKING = 4

    def __init__(self, x, y):
        self.center_x = x
        self.center_y = y
        self.change_x = 0
        self.change_y = 0
        self.state = self.IDLE
        self.direction = 1
        self.animation_timer = 0
        self.frame = 0
        self.attacking = False
        self.attack_timer = 0
        self.attack_cooldown = 0
        self.on_ground = False

    def update(self):
        self.change_y -= GRAVITY
        self.center_x += self.change_x
        self.center_y += self.change_y

        self.animation_timer += 1
        if self.animation_timer > 10:
            self.animation_timer = 0
            self.frame = (self.frame + 1) % 4

        if self.attacking:
            self.attack_timer += 1
            if self.attack_timer > 8:
                self.attacking = False
                self.attack_timer = 0
                self.attack_cooldown = 20
            self.state = self.ATTACKING
        elif not self.on_ground:
            if self.change_y > 0:
                self.state = self.JUMPING
            else:
                self.state = self.FALLING
        elif abs(self.change_x) > 0.5:
            self.state = self.RUNNING
        else:
            self.state = self.IDLE

        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1

    def attack(self):
        if self.attack_cooldown <= 0 and not self.attacking:
            self.attacking = True
            self.attack_timer = 0
            return True
        return False

    def draw(self, camera_x, camera_y):
        x = self.center_x - camera_x
        y = self.center_y - camera_y

        leg_offset = 0
        if self.state == self.RUNNING:
            leg_offset = math.sin(self.animation_timer * 0.5) * 3

        arcade.draw_ellipse_filled(x, y, 40, 30, ORANGE)

        head_y = y + 20
        arcade.draw_circle_filled(x, head_y, 15, ORANGE)

        if self.direction == 1:
            arcade.draw_triangle_filled(
                x - 8, head_y + 10,
                x - 15, head_y + 22,
                x - 2, head_y + 18,
                ORANGE
            )
            arcade.draw_triangle_filled(
                x + 8, head_y + 10,
                x + 15, head_y + 22,
                x + 2, head_y + 18,
                ORANGE
            )
        else:
            arcade.draw_triangle_filled(
                x - 8, head_y + 10,
                x - 15, head_y + 22,
                x - 2, head_y + 18,
                ORANGE
            )
            arcade.draw_triangle_filled(
                x + 8, head_y + 10,
                x + 15, head_y + 22,
                x + 2, head_y + 18,
                ORANGE
            )

        if self.direction == 1:
            eye_x_offset = 5
        else:
            eye_x_offset = -5

        arcade.draw_circle_filled(x - 5 + eye_x_offset, head_y + 2, 3, WHITE)
        arcade.draw_circle_filled(x + 5 + eye_x_offset, head_y + 2, 3, WHITE)

        if abs(self.change_x) > 0.5:
            pupil_offset = 1
        else:
            pupil_offset = 0
        arcade.draw_circle_filled(x - 5 + eye_x_offset + pupil_offset, head_y + 2, 1.5, BLACK)
        arcade.draw_circle_filled(x + 5 + eye_x_offset + pupil_offset, head_y + 2, 1.5, BLACK)

        arcade.draw_triangle_filled(
            x, head_y - 2,
               x - 3, head_y - 5,
               x + 3, head_y - 5,
            PINK
        )

        if self.direction == 1:
            arcade.draw_line(x - 2, head_y - 3, x - 12, head_y - 1, BLACK, 1)
            arcade.draw_line(x - 2, head_y - 5, x - 12, head_y - 5, BLACK, 1)
            arcade.draw_line(x - 2, head_y - 7, x - 12, head_y - 9, BLACK, 1)
            arcade.draw_line(x + 2, head_y - 3, x + 12, head_y - 1, BLACK, 1)
            arcade.draw_line(x + 2, head_y - 5, x + 12, head_y - 5, BLACK, 1)
            arcade.draw_line(x + 2, head_y - 7, x + 12, head_y - 9, BLACK, 1)
        else:
            arcade.draw_line(x - 2, head_y - 3, x - 12, head_y - 1, BLACK, 1)
            arcade.draw_line(x - 2, head_y - 5, x - 12, head_y - 5, BLACK, 1)
            arcade.draw_line(x - 2, head_y - 7, x - 12, head_y - 9, BLACK, 1)
            arcade.draw_line(x + 2, head_y - 3, x + 12, head_y - 1, BLACK, 1)
            arcade.draw_line(x + 2, head_y - 5, x + 12, head_y - 5, BLACK, 1)
            arcade.draw_line(x + 2, head_y - 7, x + 12, head_y - 9, BLACK, 1)

        if self.direction == 1:
            tail_x = x - 25
        else:
            tail_x = x + 25

        if self.state == self.RUNNING:
            tail_offset = math.sin(self.animation_timer * 0.5) * 5
        else:
            tail_offset = 0

        arcade.draw_line(tail_x, y - 5, tail_x - 15, y - 15 + tail_offset, DARK_ORANGE, 3)

        if self.direction == 1:
            arcade.draw_line(x - 5, y - 15, x - 10, y - 25 - leg_offset, DARK_ORANGE, 4)
            arcade.draw_line(x + 5, y - 15, x, y - 25 + leg_offset, DARK_ORANGE, 4)
            arcade.draw_line(x - 15, y - 15, x - 20, y - 25 + leg_offset, DARK_ORANGE, 4)
            arcade.draw_line(x + 15, y - 15, x + 10, y - 25 - leg_offset, DARK_ORANGE, 4)
        else:
            arcade.draw_line(x - 5, y - 15, x - 10, y - 25 - leg_offset, DARK_ORANGE, 4)
            arcade.draw_line(x + 5, y - 15, x, y - 25 + leg_offset, DARK_ORANGE, 4)
            arcade.draw_line(x - 15, y - 15, x - 20, y - 25 + leg_offset, DARK_ORANGE, 4)
            arcade.draw_line(x + 15, y - 15, x + 10, y - 25 - leg_offset, DARK_ORANGE, 4)

        if self.attacking:
            if self.direction == 1:
                arcade.draw_line(x + 30, y, x + 45, y + 10, RED, 3)
                arcade.draw_line(x + 30, y, x + 45, y - 10, RED, 3)
                arcade.draw_line(x + 30, y + 5, x + 45, y + 15, RED, 3)
            else:
                arcade.draw_line(x - 30, y, x - 45, y + 10, RED, 3)
                arcade.draw_line(x - 30, y, x - 45, y - 10, RED, 3)
                arcade.draw_line(x - 30, y + 5, x - 45, y + 15, RED, 3)


class Bird:
    def __init__(self, x, y):
        self.center_x = x
        self.center_y = y
        self.change_x = random.choice([-1, 1])
        self.alive = True
        self.walk_timer = random.randint(0, 100)
        self.wing_offset = random.random() * 10

    def update(self):
        if not self.alive:
            return

        self.walk_timer += 1
        self.wing_offset += 0.2

        if self.walk_timer > 120:
            self.walk_timer = 0
            self.change_x = random.choice([-1, 1])

        self.center_x += self.change_x * 2

    def draw(self, camera_x, camera_y):
        if not self.alive:
            return

        x = self.center_x - camera_x
        y = self.center_y - camera_y

        wing_y = math.sin(self.wing_offset) * 3

        arcade.draw_ellipse_filled(x, y, 25, 15, DARK_GRAY)

        if self.change_x > 0:
            head_x = x + 12
        else:
            head_x = x - 12
        arcade.draw_circle_filled(head_x, y + 3, 6, DARK_GRAY)

        arcade.draw_circle_filled(head_x - 2, y + 6, 3, DARK_GRAY)
        arcade.draw_circle_filled(head_x + 2, y + 6, 3, DARK_GRAY)

        eye_x = head_x + (2 if self.change_x > 0 else -2)
        arcade.draw_circle_filled(eye_x - 1, y + 5, 1.5, BLACK)
        arcade.draw_circle_filled(eye_x + 1, y + 5, 1.5, BLACK)

        beak_x = head_x + (4 if self.change_x > 0 else -4)
        arcade.draw_triangle_filled(
            beak_x, y + 3,
                    beak_x + (3 if self.change_x > 0 else -3), y + 4,
                    beak_x + (3 if self.change_x > 0 else -3), y + 2,
            YELLOW
        )

        if self.change_x > 0:
            arcade.draw_arc_filled(x - 10, y + wing_y, 15, 8, DARK_GRAY, 0, 180)
        else:
            arcade.draw_arc_filled(x + 10, y + wing_y, 15, 8, DARK_GRAY, 0, 180)


class Fish:
    def __init__(self, x, y):
        self.center_x = x
        self.center_y = y
        self.collected = False
        self.float_offset = random.random() * 100

    def update(self):
        self.float_offset += 0.1

    def draw(self, camera_x, camera_y):
        if self.collected:
            return

        x = self.center_x - camera_x
        y = self.center_y - camera_y + math.sin(self.float_offset) * 3

        arcade.draw_ellipse_filled(x, y, 20, 10, YELLOW)
        arcade.draw_circle_filled(x + 5, y + 2, 2, BLACK)

        arcade.draw_triangle_filled(
            x - 12, y,
            x - 18, y + 5,
            x - 18, y - 5,
            YELLOW
        )

        arcade.draw_triangle_filled(
            x, y + 5,
               x - 5, y + 10,
               x + 5, y + 8,
            YELLOW
        )
        arcade.draw_triangle_filled(
            x, y - 5,
               x - 5, y - 10,
               x + 5, y - 8,
            YELLOW
        )


class MilkBowl:
    def __init__(self, x, y):
        self.center_x = x
        self.center_y = y
        self.reached = False

    def draw(self, camera_x, camera_y):
        x = self.center_x - camera_x
        y = self.center_y - camera_y

        arcade.draw_arc_filled(x, y, 40, 20, DARK_GRAY, 0, 180)
        arcade.draw_ellipse_filled(x, y + 5, 40, 15, DARK_GRAY)
        arcade.draw_ellipse_filled(x, y + 3, 30, 10, WHITE)
        arcade.draw_ellipse_filled(x - 5, y + 5, 5, 3, WHITE, 180)


class Platform:
    def __init__(self, x, y, width, height):
        self.left = x
        self.bottom = y
        self.width = width
        self.height = height

    @property
    def right(self):
        return self.left + self.width

    @property
    def top(self):
        return self.bottom + self.height

    def draw(self, camera_x, camera_y):
        left = self.left - camera_x
        bottom = self.bottom - camera_y

        arcade.draw_lbwh_rectangle_filled(
            left,
            bottom,
            self.width,
            self.height,
            LIGHT_BROWN
        )

        for i in range(0, self.width, 15):
            arcade.draw_line(
                left + i,
                bottom,
                left + i + 7,
                bottom + self.height,
                DARK_BROWN,
                2
            )

        arcade.draw_lbwh_rectangle_filled(
            left,
            bottom + self.height - 4,
            self.width,
            4,
            GREEN
        )


class Water:
    def __init__(self, x, y, width, height):
        self.left = x
        self.bottom = y
        self.width = width
        self.height = height
        self.wave_offset = random.random() * 100

    def update(self):
        self.wave_offset += 0.1

    def draw(self, camera_x, camera_y):
        left = self.left - camera_x
        bottom = self.bottom - camera_y

        arcade.draw_lbwh_rectangle_filled(
            left,
            bottom,
            self.width,
            self.height,
            BLUE
        )

        for i in range(0, self.width, 20):
            wave_y = bottom + self.height - 3 + math.sin(self.wave_offset + i * 0.1) * 2
            arcade.draw_line(
                left + i,
                wave_y,
                left + i + 15,
                wave_y,
                WHITE,
                2
            )

    @property
    def right(self):
        return self.left + self.width

    @property
    def top(self):
        return self.bottom + self.height

    def check_collision(self, cat):
        return (cat.center_x > self.left and
                cat.center_x < self.right and
                cat.center_y - 15 < self.top and
                cat.center_y + 15 > self.bottom)


class StartView(arcade.View):
    def __init__(self):
        super().__init__()
        self.title_text = arcade.Text("😺 KittyRun 😺",
                                      SCREEN_WIDTH // 2, 450,
                                      PURPLE, 60, anchor_x="center", font_name="Kenney Pixel")
        self.controls_text1 = arcade.Text("⬅️  ➡️  - движение",
                                          SCREEN_WIDTH // 2, 280,
                                          DARK_BROWN, 25, anchor_x="center", font_name="Kenney Pixel")
        self.controls_text2 = arcade.Text("␣ - прыжок",
                                          SCREEN_WIDTH // 2, 240,
                                          DARK_BROWN, 25, anchor_x="center", font_name="Kenney Pixel")
        self.controls_text3 = arcade.Text("A - атака 🐾",
                                          SCREEN_WIDTH // 2, 200,
                                          DARK_BROWN, 25, anchor_x="center", font_name="Kenney Pixel")
        self.start_text = arcade.Text("НАЧАТЬ ИГРУ",
                                      SCREEN_WIDTH // 2, 100,
                                      BLACK, 30, anchor_x="center", font_name="Kenney Pixel")

    def on_show(self):
        arcade.set_background_color(LIGHT_PINK)

    def on_draw(self):
        self.clear()

        for i in range(10):
            x = random.randint(0, SCREEN_WIDTH)
            y = random.randint(0, SCREEN_HEIGHT)
            arcade.draw_circle_filled(x, y, 3, PINK, 100)

        self.title_text.draw()

        cat_x = SCREEN_WIDTH // 2
        cat_y = 350

        arcade.draw_circle_filled(cat_x, cat_y + 20, 20, ORANGE)
        arcade.draw_ellipse_filled(cat_x, cat_y, 50, 40, ORANGE)

        arcade.draw_triangle_filled(
            cat_x - 12, cat_y + 30,
            cat_x - 20, cat_y + 45,
            cat_x - 5, cat_y + 38,
            ORANGE
        )
        arcade.draw_triangle_filled(
            cat_x + 12, cat_y + 30,
            cat_x + 20, cat_y + 45,
            cat_x + 5, cat_y + 38,
            ORANGE
        )

        arcade.draw_triangle_filled(
            cat_x - 12, cat_y + 32,
            cat_x - 18, cat_y + 42,
            cat_x - 8, cat_y + 36,
            PINK
        )
        arcade.draw_triangle_filled(
            cat_x + 12, cat_y + 32,
            cat_x + 18, cat_y + 42,
            cat_x + 8, cat_y + 36,
            PINK
        )

        arcade.draw_circle_filled(cat_x - 8, cat_y + 22, 5, WHITE)
        arcade.draw_circle_filled(cat_x + 8, cat_y + 22, 5, WHITE)
        arcade.draw_circle_filled(cat_x - 8, cat_y + 22, 2, BLACK)
        arcade.draw_circle_filled(cat_x + 8, cat_y + 22, 2, BLACK)

        arcade.draw_triangle_filled(
            cat_x, cat_y + 15,
                   cat_x - 4, cat_y + 10,
                   cat_x + 4, cat_y + 10,
            PINK
        )

        arcade.draw_arc_outline(cat_x - 20, cat_y - 5, 30, 20, DARK_ORANGE, 30, 150, 5)

        arcade.draw_line(cat_x - 10, cat_y + 15, cat_x - 25, cat_y + 10, BLACK, 2)
        arcade.draw_line(cat_x - 10, cat_y + 13, cat_x - 25, cat_y + 5, BLACK, 2)
        arcade.draw_line(cat_x + 10, cat_y + 15, cat_x + 25, cat_y + 10, BLACK, 2)
        arcade.draw_line(cat_x + 10, cat_y + 13, cat_x + 25, cat_y + 5, BLACK, 2)

        for i in range(5):
            fish_x = 150 + i * 120
            fish_y = 120
            arcade.draw_ellipse_filled(fish_x, fish_y, 25, 12, YELLOW)
            arcade.draw_circle_filled(fish_x + 8, fish_y + 2, 3, BLACK)
            arcade.draw_triangle_filled(
                fish_x - 15, fish_y,
                fish_x - 22, fish_y + 6,
                fish_x - 22, fish_y - 6,
                YELLOW
            )

        arcade.draw_lbwh_rectangle_filled(SCREEN_WIDTH // 2 - 120, 70, 240, 60, GREEN)
        self.start_text.draw()

    def on_mouse_press(self, x, y, button, modifiers):
        if (SCREEN_WIDTH // 2 - 120 < x < SCREEN_WIDTH // 2 + 120 and
                70 < y < 130):
            game_view = GameView()
            self.window.show_view(game_view)


class GameOverView(arcade.View):
    def __init__(self, fish_collected, birds_killed, won):
        super().__init__()
        self.fish_collected = fish_collected
        self.birds_killed = birds_killed
        self.won = won

        if won:
            self.result_text = arcade.Text("🎉 ТЫ ВЫИГРАЛ! 🎉",
                                           SCREEN_WIDTH // 2, 400,
                                           GREEN, 50, anchor_x="center")
        else:
            self.result_text = arcade.Text("😿 ИГРА ОКОНЧЕНА 😿",
                                           SCREEN_WIDTH // 2, 400,
                                           RED, 50, anchor_x="center")

        self.score_text = arcade.Text(f"🐟 Рыбок собрано: {fish_collected}",
                                      SCREEN_WIDTH // 2, 300,
                                      BLACK, 30, anchor_x="center")
        self.birds_text = arcade.Text(f"🐦 Птичек убито: {birds_killed}",
                                      SCREEN_WIDTH // 2, 250,
                                      BLACK, 30, anchor_x="center")
        self.restart_text = arcade.Text("🔄 ИГРАТЬ СНОВА 🔄",
                                        SCREEN_WIDTH // 2, 150,
                                        BLACK, 25, anchor_x="center")
        self.exit_text = arcade.Text("❌ ВЫХОД ❌",
                                     SCREEN_WIDTH // 2, 70,
                                     BLACK, 25, anchor_x="center")

    def on_show(self):
        arcade.set_background_color(LIGHT_PINK)

    def on_draw(self):
        self.clear()
        self.result_text.draw()
        self.score_text.draw()
        self.birds_text.draw()

        arcade.draw_lbwh_rectangle_filled(SCREEN_WIDTH // 2 - 150, 120, 300, 60, GREEN)
        self.restart_text.draw()

        arcade.draw_lbwh_rectangle_filled(SCREEN_WIDTH // 2 - 120, 40, 240, 50, RED)
        self.exit_text.draw()

    def on_mouse_press(self, x, y, button, modifiers):
        if (SCREEN_WIDTH // 2 - 150 < x < SCREEN_WIDTH // 2 + 150 and
                120 < y < 180):
            game_view = GameView()
            self.window.show_view(game_view)

        if (SCREEN_WIDTH // 2 - 120 < x < SCREEN_WIDTH // 2 + 120 and
                40 < y < 90):
            arcade.exit()


class GameView(arcade.View):
    def __init__(self):
        super().__init__()
        arcade.set_background_color(SKY_BLUE)

        self.cat = None
        self.platforms = []
        self.birds = []
        self.fishes = []
        self.waters = []
        self.milk_bowl = None

        self.fish_collected = 0
        self.birds_killed = 0
        self.current_level = 1
        self.total_levels = 3

        self.camera_x = 0
        self.camera_y = 0

        self.game_over = False
        self.level_complete = False

        self.setup_level()

    def setup_level(self):
        self.platforms = []
        self.birds = []
        self.fishes = []
        self.waters = []

        if self.current_level == 1:
            self.setup_level_1()
        elif self.current_level == 2:
            self.setup_level_2()
        elif self.current_level == 3:
            self.setup_level_3()

    def setup_level_1(self):
        self.cat = Cat(100, 300)
        self.platforms.append(Platform(0, 50, 1000, 50))
        self.platforms.append(Platform(200, 200, 100, 20))
        self.platforms.append(Platform(400, 300, 100, 20))
        self.platforms.append(Platform(600, 200, 100, 20))
        self.platforms.append(Platform(800, 300, 100, 20))

        self.birds.append(Bird(250, 230))
        self.birds.append(Bird(450, 330))

        self.fishes.append(Fish(250, 250))
        self.fishes.append(Fish(450, 350))
        self.fishes.append(Fish(650, 250))

        self.waters.append(Water(300, 0, 100, 50))
        self.waters.append(Water(500, 0, 100, 50))

        self.milk_bowl = MilkBowl(900, 350)

    def setup_level_2(self):
        self.cat = Cat(100, 300)
        self.platforms.append(Platform(0, 50, 1000, 50))
        self.platforms.append(Platform(150, 200, 80, 20))
        self.platforms.append(Platform(300, 300, 80, 20))
        self.platforms.append(Platform(450, 200, 80, 20))
        self.platforms.append(Platform(600, 350, 80, 20))
        self.platforms.append(Platform(750, 250, 80, 20))

        self.birds.append(Bird(180, 230))
        self.birds.append(Bird(330, 330))
        self.birds.append(Bird(480, 230))
        self.birds.append(Bird(630, 380))

        self.fishes.append(Fish(180, 250))
        self.fishes.append(Fish(330, 350))
        self.fishes.append(Fish(480, 250))
        self.fishes.append(Fish(630, 400))
        self.fishes.append(Fish(780, 300))

        self.waters.append(Water(200, 0, 80, 50))
        self.waters.append(Water(400, 0, 80, 50))
        self.waters.append(Water(600, 0, 80, 50))

        self.milk_bowl = MilkBowl(850, 350)

    def setup_level_3(self):
        self.cat = Cat(150, 550)

        self.waters.append(Water(0, 0, 1000, 100))

        self.platforms.append(Platform(100, 400, 80, 20))
        self.platforms.append(Platform(250, 500, 80, 20))
        self.platforms.append(Platform(400, 400, 80, 20))
        self.platforms.append(Platform(550, 500, 80, 20))
        self.platforms.append(Platform(700, 400, 80, 20))
        self.platforms.append(Platform(850, 500, 80, 20))

        self.birds.append(Bird(150, 430))
        self.birds.append(Bird(300, 530))
        self.birds.append(Bird(450, 430))
        self.birds.append(Bird(600, 530))
        self.birds.append(Bird(750, 430))

        for i in range(6):
            self.fishes.append(Fish(150 + i * 120, 450))

        self.milk_bowl = MilkBowl(900, 550)

    def update_camera(self):
        target_x = self.cat.center_x - SCREEN_WIDTH // 2
        target_y = self.cat.center_y - SCREEN_HEIGHT // 2

        self.camera_x += (target_x - self.camera_x) * 0.1
        self.camera_y += (target_y - self.camera_y) * 0.1

        self.camera_x = max(0, min(self.camera_x, 1000 - SCREEN_WIDTH))
        self.camera_y = max(0, min(self.camera_y, 600 - SCREEN_HEIGHT))

    def check_collisions(self):
        if not self.cat or self.game_over or self.level_complete:
            return

        self.cat.on_ground = False
        for platform in self.platforms:
            if (self.cat.change_y <= 0 and
                    abs(self.cat.center_x - (platform.left + platform.width // 2)) < platform.width // 2 + 15 and
                    self.cat.center_y - 15 < platform.top and
                    self.cat.center_y + 15 > platform.top - 10):
                self.cat.center_y = platform.top + 15
                self.cat.change_y = 0
                self.cat.on_ground = True
                break

        for fish in self.fishes:
            if not fish.collected:
                if (abs(self.cat.center_x - fish.center_x) < 30 and
                        abs(self.cat.center_y - fish.center_y) < 30):
                    fish.collected = True
                    self.fish_collected += 1

        if self.cat.attacking:
            for bird in self.birds:
                if bird.alive:
                    distance = abs(self.cat.center_x - bird.center_x)
                    if distance < ATTACK_RANGE and abs(self.cat.center_y - bird.center_y) < 40:
                        if (self.cat.direction == 1 and bird.center_x > self.cat.center_x) or \
                                (self.cat.direction == -1 and bird.center_x < self.cat.center_x):
                            bird.alive = False
                            self.birds_killed += 1

        for bird in self.birds:
            if bird.alive:
                if (abs(self.cat.center_x - bird.center_x) < 30 and
                        abs(self.cat.center_y - bird.center_y) < 30):
                    self.game_over = True

        for water in self.waters:
            if water.check_collision(self.cat):
                self.game_over = True

        if self.milk_bowl and not self.milk_bowl.reached:
            if (abs(self.cat.center_x - self.milk_bowl.center_x) < 40 and
                    abs(self.cat.center_y - self.milk_bowl.center_y) < 40):
                self.milk_bowl.reached = True
                self.level_complete = True

    def on_update(self, delta_time):
        if self.game_over or self.level_complete:
            return

        self.cat.update()

        for bird in self.birds:
            bird.update()

        for fish in self.fishes:
            fish.update()

        for water in self.waters:
            water.update()

        self.check_collisions()
        self.update_camera()

        if self.level_complete:
            if self.current_level < self.total_levels:
                self.current_level += 1
                self.setup_level()
                self.level_complete = False
            else:
                game_over_view = GameOverView(self.fish_collected, self.birds_killed, True)
                self.window.show_view(game_over_view)

        if self.game_over:
            game_over_view = GameOverView(self.fish_collected, self.birds_killed, False)
            self.window.show_view(game_over_view)

    def on_draw(self):
        self.clear()

        for i in range(0, 1000, 100):
            arcade.draw_circle_filled(i + 50 - self.camera_x, 500 - self.camera_y, 30, WHITE, 150)
            arcade.draw_circle_filled(i + 80 - self.camera_x, 520 - self.camera_y, 30, WHITE, 150)

        for water in self.waters:
            water.draw(self.camera_x, self.camera_y)

        for platform in self.platforms:
            platform.draw(self.camera_x, self.camera_y)

        for fish in self.fishes:
            fish.draw(self.camera_x, self.camera_y)

        for bird in self.birds:
            bird.draw(self.camera_x, self.camera_y)

        if self.milk_bowl:
            self.milk_bowl.draw(self.camera_x, self.camera_y)

        if self.cat:
            self.cat.draw(self.camera_x, self.camera_y)

        arcade.draw_lbwh_rectangle_filled(10, SCREEN_HEIGHT - 70, 200, 60, BLACK_TRANSPARENT)
        arcade.draw_text(f"🐟: {self.fish_collected}", 20, SCREEN_HEIGHT - 50, WHITE, 20)
        arcade.draw_text(f"🐦: {self.birds_killed}", 20, SCREEN_HEIGHT - 75, WHITE, 20)
        arcade.draw_text(f"Уровень: {self.current_level}/{self.total_levels}", 20, SCREEN_HEIGHT - 100, WHITE, 16)

    def on_key_press(self, key, modifiers):
        if self.game_over or self.level_complete:
            return

        if key == arcade.key.LEFT:
            self.cat.change_x = -PLAYER_MOVEMENT_SPEED
            self.cat.direction = -1
        elif key == arcade.key.RIGHT:
            self.cat.change_x = PLAYER_MOVEMENT_SPEED
            self.cat.direction = 1
        elif key == arcade.key.SPACE:
            if self.cat.on_ground:
                self.cat.change_y = PLAYER_JUMP_SPEED
        elif key == arcade.key.A:
            self.cat.attack()

    def on_key_release(self, key, modifiers):
        if key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.cat.change_x = 0


def main():
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    start_view = StartView()
    window.show_view(start_view)
    arcade.run()


if __name__ == "__main__":
    main()