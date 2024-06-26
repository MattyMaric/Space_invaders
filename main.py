import random
import time
import turtle

FRAME_RATE = 30  # Frames per second
TIME_FOR_1_FRAME = 1 / FRAME_RATE  # Seconds

CANNON_STEP = 12.5
LASER_SPEED = 20
ALIEN_SPAWN_INTERVAL = 1.2  # Seconds
BASE_ALIEN_SPEED = 3.5
ALIEN_SPEED_INCREMENT = 0.1  # Speed increment per score point

window = turtle.Screen()
window.tracer(0)
window.setup(0.5, 0.75)
window.bgcolor(0.2, 0.2, 0.2)
window.title("The Real Python Space Invaders")

# Register custom shapes
window.addshape("cannon.gif")
window.addshape("laser.gif")
alien_shapes = ["alien1.gif", "alien2.gif", "alien3.gif", "alien4.gif"]
for shape in alien_shapes:
    window.addshape(shape)

LEFT = -window.window_width() / 2
RIGHT = window.window_width() / 2
TOP = window.window_height() / 2
BOTTOM = -window.window_height() / 2
FLOOR_LEVEL = 0.9 * BOTTOM
GUTTER = 0.025 * window.window_width()

# Create laser cannon
cannon = turtle.Turtle()
cannon.penup()
cannon.shape("cannon.gif")
cannon.setposition(0, FLOOR_LEVEL)
cannon.cannon_movement = 0  # -1, 0 or 1 for left, stationary, right

# Create turtle for writing text
text = turtle.Turtle()
text.penup()
text.hideturtle()
text.setposition(LEFT * 0.8, TOP * 0.8)
text.color(1, 1, 1)

lasers = []
aliens = []
game_running = True  # Initialize game_running as a global variable

# Initialize splash_text
splash_text = turtle.Turtle()
splash_text.hideturtle()
splash_text.color(1, 1, 1)

def draw_cannon():
    cannon.setposition(cannon.xcor(), FLOOR_LEVEL)

def move_left():
    cannon.cannon_movement = -1

def move_right():
    cannon.cannon_movement = 1

def stop_cannon_movement():
    cannon.cannon_movement = 0

def create_laser():
    laser = turtle.Turtle()
    laser.penup()
    laser.shape("laser.gif")
    laser.setposition(cannon.xcor(), cannon.ycor() + 20)  # Position just above cannon tip
    lasers.append(laser)

def move_laser(laser):
    laser.setheading(90)  # Ensure laser moves upwards
    laser.forward(LASER_SPEED)

def create_alien():
    alien = turtle.Turtle()
    alien.penup()
    alien.shape(random.choice(alien_shapes))  # Randomly choose an alien shape
    alien.setposition(
        random.randint(
            int(LEFT + GUTTER),
            int(RIGHT - GUTTER),
        ),
        TOP,
    )
    alien.setheading(-90)
    aliens.append(alien)

def remove_sprite(sprite, sprite_list):
    sprite.hideturtle()
    window.update()
    sprite_list.remove(sprite)

def restart_game():
    global lasers, aliens, alien_timer, game_timer, score, game_running, splash_text
    # Clear all existing sprites
    for laser in lasers.copy():
        remove_sprite(laser, lasers)
    for alien in aliens.copy():
        remove_sprite(alien, aliens)
    # Reset game state
    lasers = []
    aliens = []
    alien_timer = time.time()
    game_timer = time.time()
    score = 0
    game_running = True
    splash_text.clear()
    game_loop()

def game_loop():
    global alien_timer, game_timer, score, game_running, splash_text, BASE_ALIEN_SPEED
    alien_timer = time.time()
    game_timer = time.time()
    score = 0
    game_running = True

    while game_running:
        timer_this_frame = time.time()

        time_elapsed = time.time() - game_timer
        text.clear()
        text.write(
            f"Time: {time_elapsed:5.1f}s\nScore: {score:5}",
            font=("Courier", 20, "bold"),
        )
        # Move cannon
        new_x = cannon.xcor() + CANNON_STEP * cannon.cannon_movement
        if LEFT + GUTTER <= new_x <= RIGHT - GUTTER:
            cannon.setx(new_x)
            draw_cannon()
        # Move all lasers
        for laser in lasers.copy():
            move_laser(laser)
            # Remove laser if it goes off screen
            if laser.ycor() > TOP:
                remove_sprite(laser, lasers)
                break
            # Check for collision with aliens
            for alien in aliens.copy():
                if laser.distance(alien) < 20:
                    remove_sprite(laser, lasers)
                    remove_sprite(alien, aliens)
                    score += 1
                    break
        # Spawn new aliens when time interval elapsed
        if time.time() - alien_timer > ALIEN_SPAWN_INTERVAL:
            create_alien()
            alien_timer = time.time()

        # Calculate current alien speed based on score
        current_alien_speed = BASE_ALIEN_SPEED + score * ALIEN_SPEED_INCREMENT

        # Move all aliens
        for alien in aliens:
            alien.forward(current_alien_speed)
            # Check for game over
            if alien.ycor() < FLOOR_LEVEL:
                game_running = False
                break

        time_for_this_frame = time.time() - timer_this_frame
        if time_for_this_frame < TIME_FOR_1_FRAME:
            time.sleep(TIME_FOR_1_FRAME - time_for_this_frame)
        window.update()

    splash_text.clear()
    splash_text.write("GAME OVER\nPress 'R' to Restart", font=("Courier", 40, "bold"), align="center")

# Key bindings
window.onkeypress(move_left, "Left")
window.onkeypress(move_right, "Right")
window.onkeyrelease(stop_cannon_movement, "Left")
window.onkeyrelease(stop_cannon_movement, "Right")
window.onkeypress(create_laser, "space")
window.onkeypress(turtle.bye, "q")
window.onkeypress(restart_game, "r")
window.listen()

draw_cannon()
game_loop()

turtle.done()
