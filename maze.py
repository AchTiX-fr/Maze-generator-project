import random
from PIL import Image, ImageDraw
import time
import sys
import webbrowser
import os

def display_text(text, end="\n"): 
    """Function for displaying text in a customized manner"""
    for i in range(len(text)):
        print(text[i], end="")
        sys.stdout.flush()
        time.sleep(0.012)
    print(end, end="")

class Maze:
    def __init__(self, num_rows, num_cols):
        """
        Use: 
            Initialization of the maze (presented in the form of a 3D table with the first two dimensions for the plane and the third to determine whether or not there are walls around each square)
        Input: 
            Self and the desired number of rows and columns
        Returns: 
            Returns nothing
        """
        self.r, self.c = num_rows, num_cols
        self.grid = [[[1]*4 for i in range(self.c)] for j in range(self.r)]
        self.visited = [[False for i in range(self.c)] for j in range(self.r)]

    def is_inside(self, i, j):
        """
        Use: 
            Allows you to know whether or not a square belongs to the maze.
        Input: 
            Self and the row “i” and column “j.”
        Returns: 
            Returns True if the square belongs to the maze and False otherwise.
        """
        return 0 <= i < self.c and 0 <= j < self.r

    def check_wall(self, cell, direction):
        """
        Use: 
            Checks whether there is a wall in the given direction (North, East, South, and West)
        Input: 
            Self and a box with coordinates (as a 2D array) and a direction (0 for North, 1 for East, 2 for South, and 3 for West)
        Returns: 
            Returns False if there is no wall in the given direction and True otherwise
        """
        if self.grid[cell[0]][cell[1]][direction] == 0:
            return False
        return True
    
    def reverse_direction(self, nb):
        """
        Use: 
            Reverses the direction
        Input: 
            Self and a direction (0 for North, 1 for East, 2 for South, and 3 for West)
        Returns: 
            Returns the number corresponding to the opposite direction of the one given
        """
        if nb == 0: return 2
        if nb == 1: return 3
        if nb == 2: return 0
        if nb == 3: return 1
    
    def remove_wall(self, cell, direction):
        """
        Use: 
            Allows you to remove a wall and update it in the adjacent square.
        Input: 
            Self and a square with coordinates (as it is a 2D array) and a direction (0 for North, 1 for East, 2 for South, and 3 for West).
        Returns: 
            Returns nothing.
        """
        i, j = cell
        if 0 <= i <= self.c - 1 and 0 <= j <= self.r - 1:
            if direction == 0 and i > 0:
                index = self.reverse_direction(direction)
                self.grid[i-1][j][index] = 0
            elif direction == 1 and j < self.c - 1:
                index = self.reverse_direction(direction)
                self.grid[i][j+1][index] = 0
            elif direction == 2 and i < self.r - 1:
                index = self.reverse_direction(direction)
                self.grid[i+1][j][index] = 0
            elif direction == 3 and j > 0:
                index = self.reverse_direction(direction)
                self.grid[i][j-1][index] = 0
            self.grid[i][j][direction] = 0

    def __str__(self):
        """
         Use: 
            Allows display in console mode.
        Input: 
            Self
        Returns: 
            Returns “s”, i.e., the maze.
        """
        s = ""
        for j in range(self.c):
            s += "+"
            if self.grid[0][j][0] == 1:
                 s += "-"
            if self.grid[0][j][0] == 0:
                s += " "
        s += "+\n"
        for i in range(self.r):
            for j in range(self.c):
                if self.grid[i][j][3] == 1:
                    s += "| "
                if self.grid[i][j][3] == 0:
                    s += "  "
            s += "|\n" if self.grid[i][self.c - 1][1] == 1 else " \n"
            for j in range(self.c):
                if self.grid[i][j][2] == 1:
                    s += "+-"
                if self.grid[i][j][2] == 0:
                    s += "+ "
            s += "+\n"
        return s

def save_image(maze, images):
    """
    Use: 
        Allows you to put all the steps of the maze in image mode in a list
    Input: 
        The maze, a list to append the images to
    Returns: 
        Returns nothing
    """
    cell_size = 40
    wall_thickness = 4
    img_width = maze.c * cell_size + wall_thickness # length of the maze is the cell size times the number of cells in a row
    img_height = maze.r * cell_size + wall_thickness # width of the maze is the cell size times the number of cells in a column
    wall_color = (75, 0, 130) # because Achille likes purple 
    img = Image.new("RGB", (img_width, img_height), "grey") # because Lucas likes grey
    draw = ImageDraw.Draw(img)
    
    for i in range(maze.r):
        for j in range(maze.c):
            x1 = j * cell_size # for starting x
            y1 = i * cell_size # for starting y
            x2 = x1 + cell_size # for ending x
            y2 = y1 + cell_size # for ending y
            
            if maze.grid[i][j][0] == 1: # top wall
                draw.line([(x1, y1), (x2, y1)], fill=wall_color, width=wall_thickness)
            if maze.grid[i][j][1] == 1: # right wall
                draw.line([(x2, y1), (x2, y2)], fill=wall_color, width=wall_thickness)
            if maze.grid[i][j][2] == 1: # bottom wall
                draw.line([(x1, y2), (x2, y2)], fill=wall_color, width=wall_thickness)
            if maze.grid[i][j][3] == 1: # left wall
                draw.line([(x1, y1), (x1, y2)], fill=wall_color, width=wall_thickness)
            
    images.append(img) # put the image in the images list

def create_gif(images, name):
    """
    Use: 
        Allows you to create a GIF
    Input: 
        Images, a name
    Returns: 
        Returns nothing, creates a GIF
    """
    images[0].save(name, save_all=True, append_images=images[1:], duration=100, loop=1)

def open_gif_browser(gif_path):
    """
    Use: 
        Opens a GIF file in the system's default browser.
    Input: 
        The path to the GIF file.
    Returns: 
        Nothing. Opens the GIF file in the default browser.
    """
    abs_path = os.path.abspath(gif_path)  # Get the absolute path of the GIF file
    url = f"file://{abs_path}"  # Create the local URL for the GIF file
    webbrowser.open(url)  # Opens the URL in the default browser

def generate_rec(maze, i, j, visited_cells, images):
    """
    Use: 
        allows the maze to generate itself recursively
    Input: 
        maze, (a square with coordinates i and j), and a set containing all squares already seen
    Returns: 
        returns nothing
    """
    if (i, j) in visited_cells:
        return
    else:
        visited_cells.append((i, j))
        directions = []
        if maze.is_inside(i-1, j):
            directions.append((-1, 0, 0)) # north
        if maze.is_inside(i, j+1):
            directions.append((0, 1, 1)) # east
        if maze.is_inside(i+1, j):
            directions.append((1, 0, 2)) # south
        if maze.is_inside(i, j-1):
            directions.append((0, -1, 3)) # west
        random.shuffle(directions)
        
        for d_info in directions:
            row_offset, col_offset, d = d_info
            n_row, n_col = row_offset + i, col_offset + j
            if (n_row, n_col) not in visited_cells:
                maze.remove_wall((i, j), d)
                save_image(maze, images)
                generate_rec(maze, n_row, n_col, visited_cells, images)

def generate(num_r, num_c, with_gif):
    """
    Use: 
        Manages the recursive call of the maze.
    Input: 
        The number of rows and columns desired for the maze and with_gif (0 if no GIF, 1 if yes).
    Returns: 
        The generated maze.
    """
    maze = Maze(num_r, num_c)
    visited_cells = []
    images = []
    generate_rec(maze, 0, 0, visited_cells, images)
    
    if with_gif == 1:
        """part done with chat gpt""" 
        create_gif(images, "maze.gif")  # Creates the GIF
        # Checks that the GIF file exists before trying to open it
        if os.path.exists("maze.gif"):
            open_gif_browser("maze.gif")  # Opens the GIF in the default browser
        else:
            print("Error: The GIF file could not be created.")
    else:
        return maze

def main_choice():
    """function for the user, nothing too complicated, just lots of IF statements"""
    display_text("Enter 1 if you want to create a maze and display it in the console interface.")
    display_text("Enter 2 if you want to create a maze and display it as a GIF.")
    display_text("Enter 3 if you want to quit.")
    choice = int(input("Your choice here: "))

    if choice == 1:
        display_text("You have chosen to create a maze in the console interface.")
        w = ask_width()
        h = ask_height()
        display_text("Your maze is being generated")
        maze = generate(h, w, 0)
        print(maze)
        restart()
        
    elif choice == 2:
        display_text("You have chosen to create a maze and display it using a GIF.")
        w = ask_width()
        h = ask_height()
        display_text("Your maze is being generated and will open once it is complete.")
        maze = generate(h, w, 1)
        restart()

    elif choice == 3:
        quit_program()
    else:
        display_text("Please enter a valid selection")
        main_choice()

def quit_program():
    display_text("Are you sure you want to leave??")
    display_text("enter 'Y' if you wish to exit")
    display_text("enter 'N' if you wish to stay")
    continue_choice = input("Y / N : ")
    
    if continue_choice.upper() == "Y":
        display_text("You should never have done that...")
        time.sleep(1)
        url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
        webbrowser.open(url)
    elif continue_choice.upper() == "N":
        main_choice()
    else: 
        display_text("Please select a valid option.")
        quit_program()

def restart():
    display_text("Would you like to start over?")
    display_text("enter 'Y' if you wish to stay")
    display_text("enter 'N' if you wish to quit")
    continue_choice = input("Y / N : ")
    
    if continue_choice.upper() == "Y":
        main_choice()
    elif continue_choice.upper() == "N":
        quit_program()
    else: 
        display_text("Please choose a valid option")
        restart()

def ask_width():
    display_text("Please indicate the width of your maze")
    w = int(input("Width of your maze: "))
    if w <= 0:
        display_text("Please enter a valid width")
        return ask_width()
    return w

def ask_height():
    display_text("Please indicate the height of your maze")
    h = int(input("Height of your maze: "))
    if h <= 0:
        display_text("Please enter a valid height")
        return ask_height()
    return h

display_text("Welcome!")
main_choice()
