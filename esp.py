import cv2
import numpy as np

# Constants for the ESP
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
FOV = 90

class Player:
    def __init__(self, name, position):
        self.name = name
        self.position = position

def draw_esp(frame, player):
    # Calculate the center of the window
    center_x = WINDOW_WIDTH // 2
    center_y = WINDOW_HEIGHT // 2

    # Calculate the player's position on the screen
    player_x = int(center_x + (player.position[0] * (WINDOW_WIDTH / FOV)))
    player_y = int(center_y - (player.position[1] * (WINDOW_HEIGHT / FOV)))

    # Draw the player ESP
    cv2.circle(frame, (player_x, player_y), 5, (0, 255, 0), -1)
    cv2.putText(frame, player.name, (player_x + 10, player_y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

def main():
    # Create a blank frame for visualization
    frame = np.zeros((WINDOW_HEIGHT, WINDOW_WIDTH, 3), dtype=np.uint8)

    # Example players
    players = [Player('Player1', (10, 5)), Player('Player2', (-5, 3))]

    for player in players:
        draw_esp(frame, player)

    # Show the frame with ESP
    cv2.imshow('ESP', frame)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()