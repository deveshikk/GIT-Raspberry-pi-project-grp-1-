# 🎮 Raspberry Pi Sense HAT - Color Memory Game

A memory game built in Python for the Raspberry Pi using the Sense HAT LED matrix and physical joystick.

The game flashes a growing pattern of colors on the LED matrix. The player must use the joystick to repeat the exact sequence in order to advance to the next round.

---

## 🕹️ Color & Direction Mapping

| Joystick Direction | LED Color | RGB Value | Terminal Key (Windows Simulation) |
| :--- | :--- | :--- | :--- |
| **UP** | 🔴 **Red** | `(255, 0, 0)` | `u` + `Enter` |
| **DOWN** | 🟢 **Green** | `(0, 255, 0)` | `d` + `Enter` |
| **LEFT** | 🔵 **Blue** | `(0, 0, 255)` | `l` + `Enter` |
| **RIGHT** | 🟡 **Yellow** | `(255, 255, 0)` | `r` + `Enter` |

---

## 🌟 Key Features

* **Hardware & Emulator Support:** Automatically detects whether physical Sense HAT hardware is present. Fallback mode allows testing on Windows via terminal inputs (`u`, `d`, `l`, `r`) without GUI crash errors.
* **Practice Mode (Retry Logic):** Making a mistake flashes the LED matrix **Red** and replays the current round's pattern instead of abruptly ending the game.
* **Visual Signals:**
  * **Round Clear:** Matrix flashes **Green** twice.
  * **Incorrect Input:** Matrix flashes **Red** once.
  * **Pattern Flash:** Displays full matrix color corresponding to the current step.

---

## 🚀 Getting Started

### Prerequisites (Raspberry Pi)

Ensure system packages are up to date and the Sense HAT library is installed:

```bash
sudo apt update
sudo apt install sense-hat
