import pygame
import sys
import obd

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

# Create the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Race Car Dashboard")

# Font setup
font = pygame.font.Font(None, 40)

# OBD-II connection setup
connection = obd.OBD()  # This initializes the OBD-II connection using default settings


# Function to read OBD-II data
def get_obd_data():
    try:
        rpm_response = connection.query(obd.commands.RPM)
        coolant_temp_response = connection.query(obd.commands.COOLANT_TEMP)
        dtc_response = connection.query(obd.commands.GET_DTC)

        rpm = rpm_response.value.magnitude if rpm_response.value else 0
        coolant_temp = coolant_temp_response.value.magnitude if coolant_temp_response.value else 0

        if dtc_response and not dtc_response.is_null():
            dtc_codes = [dtc.code for dtc in dtc_response]
        else:
            dtc_codes = []

        return rpm, coolant_temp, dtc_codes
    except Exception as e:
        print("Error reading OBD-II data:", e)
        return 0, 0, []


# Function to clear DTC
def clear_dtc():
    try:
        connection.query(obd.commands.CLEAR_DTC)
    except Exception as e:
        print("Error clearing DTC:", e)


def draw_text(text, x, y, color=WHITE):
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x, y))


def main():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                read_dtc_button = pygame.Rect(WIDTH - 200, 50, 150, 50)
                clear_dtc_button = pygame.Rect(WIDTH - 200, HEIGHT - 100, 150, 50)

                if read_dtc_button.collidepoint(mouse_x, mouse_y):
                    # Code to read DTC here
                    rpm, coolant_temp, dtc_codes = get_obd_data()
                    print("Read DTC:", dtc_codes)
                elif clear_dtc_button.collidepoint(mouse_x, mouse_y):
                    # Code to clear DTC here
                    clear_dtc()
                    print("DTCs cleared")

        # Clear the screen
        screen.fill(BLACK)

        # Draw race car elements
        pygame.draw.rect(screen, RED, (10, 10, WIDTH - 20, HEIGHT - 20), 5)
        pygame.draw.rect(screen, RED, (30, 30, WIDTH - 60, HEIGHT - 60), 5)
        pygame.draw.line(screen, YELLOW, (WIDTH // 2, 30), (WIDTH // 2, HEIGHT - 30), 5)

        # Display car data
        rpm, coolant_temp, dtc_codes = get_obd_data()  # Get OBD-II data

        draw_text(f"RPM: {rpm}", 50, 50)
        draw_text(f"Coolant Temp: {coolant_temp}°C", 50, HEIGHT - 100)

        dtc_x, dtc_y = WIDTH // 2 + 50, 50
        for code in dtc_codes:
            draw_text(f"DTC: {code}", dtc_x, dtc_y)
            dtc_y += 40

        # Draw buttons
        pygame.draw.rect(screen, YELLOW, (WIDTH - 200, 50, 150, 50))
        pygame.draw.rect(screen, YELLOW, (WIDTH - 200, HEIGHT - 100, 150, 50))

        draw_text("Read DTC", WIDTH - 190, 60, BLACK)
        draw_text("Clear DTC", WIDTH - 190, HEIGHT - 90, BLACK)

        # Update the display
        pygame.display.flip()


if __name__ == "__main__":
    main()
