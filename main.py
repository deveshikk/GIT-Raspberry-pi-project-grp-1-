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

def flash_color(color, duration=0.8):
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
            move = input("Your move (u/d/l/r): ").strip().lower()
            if move in KEY_MAP:
                return KEY_MAP[move]
            print("Invalid key! Use 'u' (Up), 'd' (Down), 'l' (Left), 'r' (Right).")
    else:
        # Flush queue before reading
        sense.stick.get_events()
        while True:
            events = sense.stick.get_events()
            for event in events:
                if event.action in ['pressed', 'held'] and event.direction in DIRECTIONS:
                    user_color = DIRECTIONS[event.direction]
                    # Brief visual feedback on matrix without blocking event loop
                    sense.clear(user_color)
                    time.sleep(0.3)
                    sense.clear(OFF)
                    return user_color
            time.sleep(0.05)

# Game Engine
sequence = []
print("\n🎮 Game Started!")

try:
    while True:
        # Add a new color step to the sequence for the next round
        sequence.append(random.choice(COLORS))
        
        round_passed = False
        while not round_passed:
            print(f"\n==========================================")
            print(f"       ROUND {len(sequence)}: Watch the pattern!")
            print(f"==========================================")
            time.sleep(0.6)

            # Display full sequence
            for step_num, color in enumerate(sequence, start=1):
                print(f"Step {step_num}: {COLOR_NAMES[color]}")
                flash_color(color, duration=0.8)

            print("\n👉 Your Turn: Repeat the pattern!")
            failed_attempt = False
            
            for index, target_color in enumerate(sequence, start=1):
                user_choice = get_player_input()
                
                if user_choice != target_color:
                    print(f"\n❌ Wrong move on step {index}! Replaying Round {len(sequence)}...")
                    if not USING_EMULATOR:
                        sense.clear(RED)
                        time.sleep(0.5)
                        sense.clear(OFF)
                        time.sleep(0.3)
                    failed_attempt = True
                    break  # Replay this round's sequence
                else:
                    print(f"✓ Step {index}/{len(sequence)} correct!")
            
            if not failed_attempt:
                round_passed = True

        print(f"\n🎉 Round {len(sequence)} Cleared! Moving to Round {len(sequence) + 1}...")
        if not USING_EMULATOR:
            # Flash GREEN twice to signal round clear
            for _ in range(2):
                sense.clear(GREEN)
                time.sleep(0.2)
                sense.clear(OFF)
                time.sleep(0.1)
        time.sleep(1.0)

except KeyboardInterrupt:
    print("\nGame exited.")
    if not USING_EMULATOR:
        sense.clear()