

import itertools
import os
import platform
import pygame
import random
import tkinter as tk


class GameOfLife:
    """
    The code to run a Game of Life where the user can (de)activate,
    draw and randomize cells.
    Percentage randomness can be changed.
    Cell color and figure can be changed.
    """

    def __init__(self):
        """Initializing the tkinter windows.
        Places the tkinter window in the middle of the screen.
        Defines the buttons, slider and instruction screen.
        Defines a dropdown button for cell color and figure.
        Embeds the pygame window into the tkinter frame.
        Defines the cell and grid properties.
        Initializes two generations: current and next generation.
        Initializes the pygame window and fps clock.
        """
        # Initializing the interpreter and creating a root window and title.
        self.root = tk.Tk()
        self.root.title("Game of Life - Created by Fabio Melis - Have fun")

        # Defining the main frame, left-side frame and right-side frame.
        self.frame = tk.Frame(self.root, width=1000,
                              height=1000, highlightbackground='red')
        self.menu_frame = tk.Frame(self.frame,
                                   width=250, height=1000,
                                   highlightbackground='#595959', highlightthickness=10)
        self.game_border = tk.Frame(self.frame,
                                    width=750, height=1000,
                                    highlightbackground='green', highlightthickness=10)

        # Packing the windows.
        self.frame.pack()
        self.frame.pack_propagate(0)
        self.menu_frame.pack(side="left")
        self.menu_frame.pack_propagate(0)
        self.game_border.pack()

        # Define the pixel width and height of the user's screen.
        self.pixel_width = self.root.winfo_screenwidth()
        self.pixel_height = self.root.winfo_screenheight()

        # Calculate x and y coordinates for the Tk root window
        self.cor_x = (self.pixel_width / 2) - (1000 / 2)  # tk.Frame width = 1000
        self.cor_y = (self.pixel_height / 2) - (1000 / 2)  # tk.Frame height = 1000

        # Set the location to the middle of the screen.
        self.root.geometry('%dx%d+%d+%d' % (1000, 1000, self.cor_x, self.cor_y))

        # Defining the buttons in the GUI.
        self.button_start = tk.Button(self.menu_frame,
                                      text="Start", height=5, width=20, fg="black",
                                      activeforeground="red", background="grey80", activebackground="grey80",
                                      command=self.start_button)
        self.button_stop = tk.Button(self.menu_frame,
                                     text="Stop", height=5, width=20, fg="black",
                                     activeforeground="red", background="grey80", activebackground="grey80",
                                     command=self.stop_button)
        self.button_iteration = tk.Button(self.menu_frame,
                                          text="Next iteration", height=5, width=20, fg="black",
                                          activeforeground="red", background="grey80", activebackground="grey80",
                                          command=self.create_next_gen)
        self.button_random = tk.Button(self.menu_frame,
                                       text="Random", height=5, width=20, fg="black",
                                       activeforeground="red", background="grey80", activebackground="grey80",
                                       command=self.random_grid)
        self.button_reset = tk.Button(self.menu_frame,
                                      text="Reset", height=5, width=20, fg="black",
                                      activeforeground="red", background="grey80", activebackground="grey80",
                                      command=self.reset_button)
        self.button_quit = tk.Button(self.menu_frame,
                                     text="Quit", height=5, width=20, fg="black",
                                     activeforeground="red", background="grey80", activebackground="grey80",
                                     command=self.quit_button)

        # Packing the buttons.
        self.button_start.pack()
        self.button_stop.pack()
        self.button_iteration.pack()
        self.button_random.pack()
        self.button_reset.pack()
        self.button_quit.pack()

        # Placing the buttons.
        self.button_start.place(x=40, y=50)
        self.button_stop.place(x=40, y=200)
        self.button_iteration.place(x=40, y=350)
        self.button_random.place(x=40, y=500)
        self.button_reset.place(x=40, y=650)
        self.button_quit.place(x=40, y=800)

        # Defining, packing and placing the slider.
        self.slider_random = tk.Scale(self.menu_frame, from_=0, to=100,
                                      orient="horizontal", command=self.slider_value)
        self.slider_random.set(50)
        self.slider_random.pack()
        self.slider_random.place(x=62, y=590)

        # Defining a dropdown menu for the cell figure.
        self.options_figures = [
            "circles", "squares", "surprise"
        ]
        self.var_figure = tk.StringVar(self.root)
        self.dropdown_figure = tk.OptionMenu(self.menu_frame, self.var_figure,
                                             self.options_figures[0], self.options_figures[1],
                                             self.options_figures[2])
        self.var_figure.set(self.options_figures[0])
        self.dropdown_figure.place(x=115, y=10)

        # Defining a dropdown menu for the cell color.
        self.options_colors = [
            "blue", "red", "white", "green",
            "yellow", "purple", "grey", "pink"
        ]
        self.var_color = tk.StringVar(self.root)
        self.dropdown_colors = tk.OptionMenu(self.menu_frame, self.var_color,
                                             self.options_colors[0], self.options_colors[1],
                                             self.options_colors[2], self.options_colors[3],
                                             self.options_colors[4], self.options_colors[5],
                                             self.options_colors[6], self.options_colors[7])
        self.var_color.set(self.options_colors[0])
        self.dropdown_colors.place(x=40, y=10)

        # Defining the menu with the instructions.
        self.menu_bar = tk.Menu(self.root)
        self.dropdown_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Menu", menu=self.dropdown_menu)
        self.dropdown_menu.add_command(label="Instructions",
                                       command=self.create_window)
        self.root.config(menu=self.menu_bar)

        # This embeds the pygame window in the tkinter frame.
        os.environ['SDL_WINDOWID'] = str(self.game_border.winfo_id())
        system = platform.system()
        if system == "Windows":
            os.environ['SDL_VIDEODRIVER'] = 'windib'
        elif system == "Linux":
            os.environ['SDL_VIDEODRIVER'] = 'x11'

        # Defining the grid dimensions.
        self.GRID_SIZE = self.WIDTH, self.HEIGHT = 750, 1000

        # Defining the cell size and the number of cells in the X and Y direction.
        self.CELL_SIZE = 10
        self.X_CELLS = int(self.WIDTH / self.CELL_SIZE)
        self.Y_CELLS = int(self.HEIGHT / self.CELL_SIZE)

        # Defining the number and color for dead and living cells.
        self.COLOR_DEAD = 0
        self.COLOR_ALIVE = 1
        self.colors = []
        self.colors.append((0, 0, 0))  # Black
        self.colors.append((0, 128, 128))  # blue

        # Defining two lists: current generation and next generation.
        self.current_generation = [[self.COLOR_DEAD
                                    for col in range(self.Y_CELLS)]
                                   for row in range(self.X_CELLS)]
        self.next_generation = [[self.COLOR_DEAD
                                 for col in range(self.Y_CELLS)]
                                for row in range(self.X_CELLS)]

        # Defining the max frames per second/speed of the game.
        self.FPS_MAX = 10

        # Initializing pygame.
        pygame.init()
        self.screen = pygame.display.set_mode(self.GRID_SIZE)

        # Initializing the current generation.
        self.init_gen(self.current_generation, self.COLOR_DEAD)

        # Defining a clock to set the FPS.
        self.fps_clock = pygame.time.Clock()

        # Setting variables for later use.
        self.next_iteration = False
        self.game_over = False

    def create_window(self):
        """Creates and places the instruction window from a dropdown menu."""
        self.instruction_window = tk.Toplevel(self.root, background="LightCyan3")
        self.instruction_window.title("Instructions")
        tk.Label(self.instruction_window, text='Welcome to this version of the Game of Life.'
                                               '\nThe on-screen buttons can be used to play the game.'
                                               '\nAlternatively, you can press:'
                                               '\nspace for the next generation'
                                               '\na to automate the game'
                                               '\ns to stop the game'
                                               '\nr to empty the grid'
                                               '\nq to quit the game'
                                               '\n\nThe slider below random can be used to change'
                                               ' the percentage of randomly activated cells.',
                 background="LightCyan3").pack(padx=30, pady=30)  # padx=30, pady=30

        tk.Button(self.instruction_window, text="Understood, let's play!", background="LightCyan4",
                  activebackground="LightCyan4", command=self.instruction_window.destroy).pack()
        self.x_loc = self.root.winfo_x()
        self.y_loc = self.root.winfo_y()
        self.instruction_window.geometry("+%d+%d" % (self.x_loc + 295, self.y_loc + 450))

    def options_shape(self, value):
        """Returns the cell-figure that the user chose."""
        return self.var_figure.get()

    def options_color(self, value):
        """Returns the cell-color that the user chose. """
        return self.var_color.get()

    def slider_value(self, value):
        """Returns the slider value."""
        self.value = value

    def start_button(self):
        """Button to create the next generation."""
        self.next_iteration = True

    def stop_button(self):
        """Button to stop creating the next generations."""
        self.next_iteration = False

    def reset_button(self):
        """Button to reset the grid by creating an empty generation."""
        self.next_iteration = False
        self.init_gen(self.next_generation, self.COLOR_DEAD)

    def quit_button(self):
        """Button to quit the game."""
        self.game_over = True

    def init_gen(self, generation, c):
        """Initializing the cells."""
        for row in range(self.Y_CELLS):
            for col in range(self.X_CELLS):
                generation[col][row] = c

    def random_grid(self):
        """Randomly activates cells in the grid based on the slider value.
        The slider value equals the percentage of cells randomly activated.
        """
        self.next_iteration = False
        self.percentage_zero = list(
            itertools.repeat(0, (100 - self.slider_random.get()))
        )
        self.percentage_one = list(
            itertools.repeat(1, (self.slider_random.get()))
        )

        for col in range(self.X_CELLS):
            for row in range(self.Y_CELLS):
                self.next_generation[col][row] = random.choice(self.percentage_zero
                                                               + self.percentage_one)

    def draw_cell(self, x, y, c):
        """Drawing the cell in a specific location.
        Three figure options: circles, squares and hollow circles.
        Eight color options: blue, red, white, green, yellow, purple, grey and pink.
        """
        pos = (int(x * self.CELL_SIZE + self.CELL_SIZE / 2),
               int(y * self.CELL_SIZE + self.CELL_SIZE / 2))
        if c == 1:
            if self.options_shape(self) == "circles":
                if self.options_color(self) == "blue":
                    pygame.draw.circle(self.screen, (0, 128, 128), pos, 5, 0)
                if self.options_color(self) == "red":
                    pygame.draw.circle(self.screen, (255, 0, 0), pos, 5, 0)
                if self.options_color(self) == "white":
                    pygame.draw.circle(self.screen, (255, 255, 255), pos, 5, 0)
                if self.options_color(self) == "green":
                    pygame.draw.circle(self.screen, (0, 255, 0), pos, 5, 0)
                if self.options_color(self) == "yellow":
                    pygame.draw.circle(self.screen, (255, 255, 0), pos, 5, 0)
                if self.options_color(self) == "purple":
                    pygame.draw.circle(self.screen, (255, 0, 255), pos, 5, 0)
                if self.options_color(self) == "grey":
                    pygame.draw.circle(self.screen, (155, 155, 155), pos, 5, 0)
                if self.options_color(self) == "pink":
                    pygame.draw.circle(self.screen, (255, 75, 150), pos, 5, 0)

            elif self.options_shape(self) == "squares":
                if self.options_color(self) == "blue":
                    pygame.draw.rect(self.screen, (0, 128, 128),
                                     pygame.Rect(x * self.CELL_SIZE, y * self.CELL_SIZE,
                                                 self.CELL_SIZE - 1, self.CELL_SIZE - 1))
                if self.options_color(self) == "red":
                    pygame.draw.rect(self.screen, (255, 0, 0),
                                     pygame.Rect(x * self.CELL_SIZE, y * self.CELL_SIZE,
                                                 self.CELL_SIZE - 1, self.CELL_SIZE - 1))
                if self.options_color(self) == "white":
                    pygame.draw.rect(self.screen, (255, 255, 255),
                                     pygame.Rect(x * self.CELL_SIZE, y * self.CELL_SIZE,
                                                 self.CELL_SIZE - 1, self.CELL_SIZE - 1))
                if self.options_color(self) == "green":
                    pygame.draw.rect(self.screen, (0, 255, 0),
                                     pygame.Rect(x * self.CELL_SIZE, y * self.CELL_SIZE,
                                                 self.CELL_SIZE - 1, self.CELL_SIZE - 1))
                if self.options_color(self) == "yellow":
                    pygame.draw.rect(self.screen, (255, 255, 0),
                                     pygame.Rect(x * self.CELL_SIZE, y * self.CELL_SIZE,
                                                 self.CELL_SIZE - 1, self.CELL_SIZE - 1))
                if self.options_color(self) == "purple":
                    pygame.draw.rect(self.screen, (255, 0, 255),
                                     pygame.Rect(x * self.CELL_SIZE, y * self.CELL_SIZE,
                                                 self.CELL_SIZE - 1, self.CELL_SIZE - 1))
                if self.options_color(self) == "grey":
                    pygame.draw.rect(self.screen, (155, 155, 155),
                                     pygame.Rect(x * self.CELL_SIZE, y * self.CELL_SIZE,
                                                 self.CELL_SIZE - 1, self.CELL_SIZE - 1))
                if self.options_color(self) == "pink":
                    pygame.draw.rect(self.screen, (255, 75, 150),
                                     pygame.Rect(x * self.CELL_SIZE, y * self.CELL_SIZE,
                                                 self.CELL_SIZE - 1, self.CELL_SIZE - 1))

            elif self.options_shape(self) == "surprise":
                if self.options_color(self) == "blue":
                    pygame.draw.circle(self.screen, (0, 128, 128), pos, 5, 2)
                if self.options_color(self) == "red":
                    pygame.draw.circle(self.screen, (255, 0, 0), pos, 5, 2)
                if self.options_color(self) == "white":
                    pygame.draw.circle(self.screen, (255, 255, 255), pos, 5, 2)
                if self.options_color(self) == "green":
                    pygame.draw.circle(self.screen, (0, 255, 0), pos, 5, 2)
                if self.options_color(self) == "yellow":
                    pygame.draw.circle(self.screen, (255, 255, 0), pos, 5, 2)
                if self.options_color(self) == "purple":
                    pygame.draw.circle(self.screen, (255, 0, 255), pos, 5, 2)
                if self.options_color(self) == "grey":
                    pygame.draw.circle(self.screen, (155, 155, 155), pos, 5, 2)
                if self.options_color(self) == "pink":
                    pygame.draw.circle(self.screen, (255, 75, 150), pos, 5, 2)

    def update_gen(self):
        """Draws the cells in the next generation.
        Switches the next generation with the current generation.
        This updates the game.
        """
        for row in range(self.Y_CELLS):
            for col in range(self.X_CELLS):
                c = self.next_generation[col][row]
                self.draw_cell(col, row, c)
                self.current_generation[col][row] = self.next_generation[col][row]  # assign element by element

    def activate_living_cell(self, x, y):
        """Activates a cell in the next generation."""
        self.next_generation[x][y] = self.COLOR_ALIVE

    def deactivate_living_cell(self, x, y):
        """Deactivates a cell in the next generation."""
        self.next_generation[x][y] = self.COLOR_DEAD

    # Function to check neighbor cells.
    def check_cells(self, x, y):
        """Function to check the edges.
            Cells outside the grid are considered dead.
            This function gives a 1 for living cells, 0 for dead cells.
            This is used to determine if a neighbor is alive or dead.
        """
        if (x < 0) or (y < 0):
            return 0
        if (x >= self.X_CELLS) or (y >= self.Y_CELLS):
            return 0
        if self.current_generation[x][y] == self.COLOR_ALIVE:
            return 1
        else:
            return 0

    def check_cell_neighbors(self, row_index, col_index):
        """Returns the number of living neighbors."""
        # Get the number of alive cells surrounding the current cell.
        num_alive_neighbors = 0
        num_alive_neighbors += self.check_cells(row_index - 1, col_index - 1)
        num_alive_neighbors += self.check_cells(row_index - 1, col_index)
        num_alive_neighbors += self.check_cells(row_index - 1, col_index + 1)
        num_alive_neighbors += self.check_cells(row_index, col_index - 1)
        num_alive_neighbors += self.check_cells(row_index, col_index + 1)
        num_alive_neighbors += self.check_cells(row_index + 1, col_index - 1)
        num_alive_neighbors += self.check_cells(row_index + 1, col_index)
        num_alive_neighbors += self.check_cells(row_index + 1, col_index + 1)
        return num_alive_neighbors

    def create_next_gen(self):
        """This function sets the game rules:
        1. Underpopulation: living cell dies if <2 neighbors.
        2. Living cell remains alive with exactly 2 or 3 neighbors.
        3. Overpopulation: living cell dies if >3 neighbors.
        4. Dead cell becomes alive with exactly 3 living neighbors.
        Cells are checked in the current generation.
        Cells are changed in the next generation.
        """
        for row in range(self.Y_CELLS):
            for col in range(self.X_CELLS):
                num_neighbors = self.check_cell_neighbors(col, row)
                current_cell = self.current_generation[col][row]
                if current_cell == self.COLOR_ALIVE:
                    if (num_neighbors < 2):  # Rule number 1.
                        self.next_generation[col][row] = self.COLOR_DEAD
                    elif (num_neighbors > 3):  # Rule number 3.
                        self.next_generation[col][row] = self.COLOR_DEAD
                    else:  # Rule number 2.
                        self.next_generation[col][row] = self.COLOR_ALIVE
                elif current_cell == self.COLOR_DEAD:
                    if (num_neighbors == 3):  # Rule number 4.
                        self.next_generation[col][row] = self.COLOR_ALIVE
                    else:
                        self.next_generation[col][row] = self.COLOR_DEAD

    def handle_events(self):
        """This function handles all the mouse and keyboard presses.
        Quitting the window stops the game.
        The left mouse-button is used to (de)activate cells.
        The right mouse-button is used to draw on the grid while pressed.
        Keyboard keys:
        q = quit the game and close the window.
        space = creates the next iteration manually.
        a = creates the next iteration automatically.
        s = pauses the game.
        r = resets the grid by emptying the next generation.
        """
        for event in pygame.event.get():
            posn = pygame.mouse.get_pos()
            x = int(posn[0] / self.CELL_SIZE)
            y = int(posn[1] / self.CELL_SIZE)

            if event.type == pygame.QUIT:
                self.game_over = True

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if self.current_generation[x][y] == self.COLOR_DEAD:
                        self.activate_living_cell(x, y)
                    else:
                        self.deactivate_living_cell(x, y)
                    self.update_gen()  # Cells can now be activated or deactivated when the game is running.

            if event.type == pygame.MOUSEMOTION and event.buttons[2]:
                self.activate_living_cell(x, y)

            if event.type == pygame.KEYDOWN:
                if event.unicode == 'q':
                    self.game_over = True
                elif event.key == pygame.K_SPACE:
                    self.create_next_gen()
                elif event.unicode == 'a':
                    self.next_iteration = True
                elif event.unicode == 's':
                    self.next_iteration = False
                elif event.unicode == 'r':
                    self.next_iteration = False
                    self.init_gen(self.next_generation, self.COLOR_DEAD)

    def run(self):
        """Runs the game loop.
        Handles all the events (mouse and keyboard presses).
        Fills the screen with black cells,
        to prevent overlap when switching between figures and colors.
        Creates the next generation from the current generation.
        Overwrites the current generation with the next generation.
        Updates the contents of the game window.
        Uses the previously specified frames per second/gamespeed.
        Stops the game if game_over = TRUE.
        """
        while not self.game_over:
            self.handle_events()
            self.screen.fill((0, 0, 0))
            if self.next_iteration:
                self.create_next_gen()
            self.update_gen()
            pygame.display.flip()
            self.fps_clock.tick(self.FPS_MAX)
            self.root.update()