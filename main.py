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
            # simple sticky events queue to mimic SenseHat API
            self.sticky_events = []

        def clear(self, color=None):
            pass

        # Minimal event object to mimic sense_hat event interface
        class Event:
            def __init__(self, action, direction):
                self.action = action
                self.direction = direction

        # helper to push a simulated event into the sticky queue
        def push_event(self, action, direction):
            self.sticky_events.append(ConsoleSenseHat.Event(action, direction))

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

def flash_color(color, duration=0.5):
    if USING_EMULATOR:
        print(f"[DISPLAY] FLASH -> {COLOR_NAMES.get(color, 'OFF')}")
        time.sleep(duration)
    else:
        sense.clear(color)
        time.sleep(duration)
        sense.clear(OFF)
        time.sleep(0.2)

def get_player_input():
    if USING_EMULATOR:
        while True:
            move = input("Your turn (u/d/l/r): ").strip().lower()
            if move in KEY_MAP:
                return KEY_MAP[move]
            print("Invalid key! Use 'u' for Up, 'd' for Down, 'l' for Left, 'r' for Right.")
    else:
        sticky_events = getattr(sense, "sticky_events", [])
        stick = getattr(sense, "stick", None)

        while True:
            # Consume any queued sticky events first.
            while sticky_events:
                event = sticky_events.pop(0)
                action = getattr(event, "action", None)
                direction = getattr(event, "direction", None)
                if action in ["pressed", "held"] and direction in DIRECTIONS:
                    return DIRECTIONS[direction]

            # When no queued events remain, wait for a real joystick event.
            if stick is not None:
                try:
                    event = stick.wait_for_event()
                except Exception:
                    time.sleep(0.05)
                    continue

                action = getattr(event, "action", None)
                direction = getattr(event, "direction", None)
                if action in ["pressed", "held"] and direction in DIRECTIONS:
                    return DIRECTIONS[direction]

            time.sleep(0.05)

# Game Engine
sequence = []
print("Game Started!")

try:
    while True:
        # Add random color to pattern
        sequence.append(random.choice(COLORS))
        
        print(f"\n--- Round {len(sequence)}: Watch the pattern ---")
        for color in sequence:
            flash_color(color)

        print("--- Your Turn: Repeat the pattern ---")
        for target_color in sequence:
            user_choice = get_player_input()
            
            if user_choice != target_color:
                print(f"\n❌ Wrong pattern! Game Over. Final Score: {len(sequence) - 1}")
                if not USING_EMULATOR:
                    for _ in range(3):
                        flash_color(RED, 0.2)
                    sense.clear()
                sys.exit()
            else:   
                print("Correct step!")
        
        print("Round cleared!")
        time.sleep(0.8)

except KeyboardInterrupt:
    print("\nGame exited.")
    sense.clear()