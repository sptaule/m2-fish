import time
import random
import cv2
import numpy as np
import pygetwindow as gw
from PIL import ImageGrab, Image
from pynput.keyboard import Key, Controller as KeyboardController
from pynput.mouse import Button as MouseButton, Controller as MouseController


# Servers
METIN2 = "METIN2"

# Params
GAME_WINDOW_NAME = METIN2
DELAY_BEFORE_HOOK = 2.55
DELAY_BEFORE_RESTART = 5
DELAY_FOR_IMAGE_CHECK = 0.1
CV_THRESHOLD = 0.75
MAX_IMAGE_CHECK_TIME = 60

# Load template
template_fish = cv2.imread('fish.png', cv2.IMREAD_GRAYSCALE)
template_minnow = cv2.imread('minnow.png', cv2.IMREAD_COLOR)
minnow_w, minnow_h = template_minnow.shape[:2]

# Coordinates of detection on the screen
bubble_x1, bubble_x2 = 200, 700
bubble_y1, bubble_y2 = 50, 400

# Inventory coordinates
inventory_x1, inventory_x2 = 858, 1018
inventory_y1, inventory_y2 = 443, 731

# Initialize keyboard and mouse
keyboard = KeyboardController()
mouse = MouseController()


def focus_game_window():
    game_windows = gw.getWindowsWithTitle(GAME_WINDOW_NAME)
    if game_windows:
        game_windows[0].activate()
        time.sleep(0.05)
    else:
        print(f"{Style.FAIL}Game window not found{Style.END}")


def get_window_dimensions(game_window):
    window_width, window_height = game_window.size
    left, top, right, bottom = game_window.box
    return window_width, window_height, left, top, right, bottom


def send_key(key):
    keyboard.press(key)
    time.sleep(0.05)
    keyboard.release(key)
    
    
def random_delay(delay):
    random_value = random.uniform(0.01, 0.25)
    if random.choice([True, False]):
        delay += random_value
    else:
        delay -= random_value
    delay = round(delay, 2)
    return delay


def check_for_screenshot():
    img = ImageGrab.grab(bbox=(bubble_x1, bubble_y1, bubble_x2, bubble_y2))
    img_gray = cv2.cvtColor(np.array(img), cv2.COLOR_BGR2GRAY)
    result = cv2.matchTemplate(img_gray, template_fish, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, _ = cv2.minMaxLoc(result)
    return max_val >= CV_THRESHOLD


def check_inventory_for_minnow():
    img = ImageGrab.grab(bbox=(inventory_x1, inventory_y1, inventory_x2, inventory_y2))
    img_rgb = np.array(img)

    # Perform model matching
    result = cv2.matchTemplate(img_rgb, template_minnow, cv2.TM_CCOEFF_NORMED)
    threshold = 0.8
    loc = np.where(result >= threshold)

    # If matches are found
    if len(loc[0]) > 0:
        minnow_points = list(zip(*loc[::-1]))

        # Select a random match
        random_minnow = random.choice(minnow_points)

        # Convert local ROI coordinates to global coordinates
        minnow_x, minnow_y = random_minnow[0] + inventory_x1, random_minnow[1] + inventory_y1

        return minnow_x, minnow_y
    else:
        return None


def use_minnow(x, y):
    focus_game_window()
    time.sleep(0.25)
    mouse.position = (x + 13, y + 13)
    time.sleep(0.25)
    mouse.click(MouseButton.right, 1)
    time.sleep(0.25)


def main():
    fish_counter = 0
    bait_counter = 0
    minnow_counter = 0
    try:
        while True:
            minnow_coordinates = check_inventory_for_minnow()
            if minnow_coordinates:
                minnow_location_x, minnow_location_y = minnow_coordinates
                print(f"{Style.CYAN}Using minnow as a bait{Style.END}")
                use_minnow(minnow_location_x, minnow_location_y)
                minnow_counter += 1
                time.sleep(0.5)
            else:
                # Fix bait (F4)
                print("Fixing bait on fishing rod")
                focus_game_window()
                send_key(Key.f4)
                bait_counter += 1
                time.sleep(0.5)

            # Put the bait in the water (F3)
            print("Fishing...")
            focus_game_window()
            send_key(Key.f3)
            time.sleep(0.5)

            start_time = time.time()
            while True:
                # Check if image appears
                if check_for_screenshot():
                    print(f"{Style.GREEN}Fish detected{Style.END}")
                    delay_before_hook = random_delay(DELAY_BEFORE_HOOK)
                    time.sleep(delay_before_hook)
                    print(f"Trying to pull out the fish ({delay_before_hook}s)")
                    focus_game_window()
                    send_key(Key.f3)
                    time.sleep(DELAY_BEFORE_RESTART)
                    fish_counter += 1
                    message = "Restart fishing "
                    message += f"(bait {Style.BOLD}{bait_counter}{Style.END}, "
                    message += f"minnows {Style.BOLD}{minnow_counter}{Style.END}, "
                    message += f"total {Style.BOLD}{fish_counter}{Style.END})"
                    print(message)
                    break
                elif time.time() - start_time >= MAX_IMAGE_CHECK_TIME:
                    print(f"{Style.FAIL}No image detected in 30 seconds, restarting the process{Style.END}")
                    focus_game_window()
                    send_key(Key.f4)
                    send_key(Key.f3)
                    time.sleep(DELAY_BEFORE_RESTART)
                    break
                else:
                    time.sleep(DELAY_FOR_IMAGE_CHECK)
    except KeyboardInterrupt:
        print(f"{Style.CYAN}Script halted by the user{Style.END}")


class Style:
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    FAIL = '\033[91m'
    BOLD = '\033[1m'
    END = '\033[0m'


if __name__ == "__main__":
    main()
