import random
import time
import sys

# Safe Hardware / Environment Detection
USING_EMULATOR = False

try:
    from sense_hat import SenseHat
    sense = SenseHat()
except (ImportError, RuntimeError):
    try:
        from sense_hat_virtual import SenseHat
        sense = SenseHat()
    except (ImportError, RuntimeError, Exception):
        USING_EMULATOR = True

# Fallback Console Interface for Windows testing without GUI crashes
if USING_EMULATOR:
    class ConsoleSenseHat:
        def __init__(self):
            print("\n--- Running in Windows Console Simulation Mode ---")
            print("Controls: Type 'u' (Up/Red), 'd' (Down/Green), 'l' (Left/Blue), 'r' (Right/Yellow) and press Enter.\n")

        def clear(self, color=None):
            pass

    sense = ConsoleSenseHat()

# Color Definitions (RGB)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
OFF = (0, 0, 0)

COLOR_NAMES = {RED: "RED (Up)", GREEN: "GREEN (Down)", BLUE: "BLUE (Left)", YELLOW: "YELLOW (Right)"}
COLORS = [RED, GREEN, BLUE, YELLOW]
DIRECTIONS = {'up': RED, 'down': GREEN, 'left': BLUE, 'right': YELLOW}
KEY_MAP = {'u': RED, 'd': GREEN, 'l': BLUE, 'r': YELLOW}

# Increased flash duration for longer LED lighting
def flash_color(color, duration=1.0):
    if USING_EMULATOR:
        print(f"[DISPLAY] FLASH -> {COLOR_NAMES.get(color, 'OFF')}")
        time.sleep(duration)
    else:
        sense.clear(color)
        time.sleep(duration)
        sense.clear(OFF)
        time.sleep(0.3)

def get_player_input():
    if USING_EMULATOR:
        while True:
            move = input("Your turn (u/d/l/r): ").strip().lower()
            if move in KEY_MAP:
                return KEY_MAP[move]
            print("Invalid key! Use 'u' for Up, 'd' for Down, 'l' for Left, 'r' for Right.")
    else:
        # Clear residual events before checking new input
        _ = sense.sticky_events
        while True:
            events = sense.sticky_events
            for event in events:
                if event.action in ['pressed', 'held'] and event.direction in DIRECTIONS:
                    user_color = DIRECTIONS[event.direction]
                    # Show user's input choice on matrix
                    flash_color(user_color, duration=0.5)
                    return user_color
            time.sleep(0.05)

# Game Engine
sequence = []
print("Game Started!")

try:
    while True:
        # Add a new color step to the sequence
        sequence.append(random.choice(COLORS))
        
        round_passed = False
        while not round_passed:
            print(f"\n--- Round {len(sequence)}: Watch the pattern ---")
            time.sleep(0.5)
            for color in sequence:
                flash_color(color, duration=0.8)

            print("--- Your Turn: Repeat the pattern ---")
            failed_attempt = False
            
            for target_color in sequence:
                user_choice = get_player_input()
                
                if user_choice != target_color:
                    print("\n❌ Wrong input! Replaying sequence, try again...")
                    if not USING_EMULATOR:
                        # Flash RED once to signal mistake
                        sense.clear(RED)
                        time.sleep(0.5)
                        sense.clear(OFF)
                        time.sleep(0.3)
                    failed_attempt = True
                    break  # Break input loop to replay the current round sequence
                else:
                    print("Correct step!")
            
            if not failed_attempt:
                round_passed = True

        print("Round cleared!")
        time.sleep(1.0)

except KeyboardInterrupt:
    print("\nGame exited.")
    if not USING_EMULATOR:
        sense.clear()