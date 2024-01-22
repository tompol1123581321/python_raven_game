import concurrent.futures
import pygame
from constans import *
from parts.menu import Menu
from parts.arrows.arrow_manager import Arrows
from parts.healthbar import Health
from parts.raven import Raven
from parts.score import Score
from utils import Time_Manager,License_Manager
import sys


# import tkinter as tk
# from tkinter import messagebox

# # Create a tkinter window (it won't be visible)
# root = tk.Tk()
# root.withdraw()  # Hide the main window

# # Show a message box
# messagebox.showinfo("Message Box Title", "This is a message box!")

# You can also use other messagebox functions like showwarning, showerror, etc.
# messagebox.showwarning("Warning", "This is a warning message.")
# messagebox.showerror("Error", "This is an error message.")

# Run the tkinter main loop (needed to show the message box)
#root.mainloop()





# Using ThreadPoolExecutor to run license check in a separate thread
with concurrent.futures.ThreadPoolExecutor() as executor:
    future = executor.submit(License_Manager.checkLicense)
    license_valid = future.result()

# Proceed only if the license is valid
if not license_valid:
    sys.exit("License check failed. Exiting the game.")


pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT),)
pygame.display.set_caption("Raven Flight")
font = pygame.font.Font('freesansbold.ttf', 32)


arrows = Arrows()
health_bar = Health()
score = Score(font)
raven = Raven()


def handle_fire_arrow():
    arrows.add_arrow(raven.current_position)


def reset():
    arrows.reset()
    health_bar.reset()
    score.reset()
    raven.reset()
    time_manager.reset()


menu = Menu(reset, font)
menu.show_initial_menu(screen)

time_manager = Time_Manager(
    handle_fire_arrow, raven.change_sprite_frame, score.increase_score)


run = True
while run and menu.run:
    screen.fill(BG)

    arrows.render_arrows(screen)
    health_bar.show_healthbars(screen)
    score.show_score(screen)
    raven.show_raven(screen)

    health_bar.check_collision_and_lower_hp(
        arrows.on_move_arrows(raven.current_position))
    raven.change_position()

    time_manager.tick()

    if health_bar.hps == 0:
        menu.show_played_menu(screen, score.score)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
            raven.change_directions(event)
    pygame.display.update()
pygame.quit()