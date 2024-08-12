# m2-fish

A little fishbot for the old Metin2 fishing system

## Requirements

- cv2
- numpy
- pygetwindow
- pynput
- Pillow

## How it works

- OpenCV (cv2) is used for image processing and detection in the current game window
- numpy is used for data arrays manipulation, useful for processing captured images and pattern matching results
- pygetwindow is used to interact with application windows, in particular to ensure that the game window is active when sending inputs
- Pillow is used to capture screenshots (via ImageGrab) and manipulate images
- pynput is used to simulate keyboard and mouse actions

### Functions detail

`focus_game_window()`:  
This function finds and activates the "Metin2" game window to ensure that keyboard and mouse actions are directed to the correct window.

`get_window_dimensions(game_window)`:  
This function returns the dimensions of the game window and its coordinates on the screen.

`send_key(key)`:  
This function simulates the pressing and releasing of a key on the keyboard, with a pause in between.

`check_for_screenshot()`:  
This function captures a specific part of the screen and uses OpenCV to check whether a predefined fish image appears in this capture.

`check_inventory_for_minnow()`:  
This function captures a part of the screen corresponding to the player's inventory and detects the presence of minnows. If found, it returns the bait's coordinates.

`use_minnow(x, y)`:  
This function moves the mouse to the coordinates of a found minnow and clicks to use it.

`Style`:  
This class is used to define text styles for console messages (colors and formatting).

`main()`:  
This main function executes an infinite loop that :
- Checks inventory for a minnow and uses it if found (if not, it uses the regular bait)
- Simulates keystrokes to attach bait and start fishing
- Monitors the presence of a fish on the screen, attempts to catch it and restarts the process after a pause

If OpenCV did not detect any fish, it will restart process after 60 seconds.

## How to use it

Make sure you have Python installed on your system. Here is the link for [Windows downloads](https://www.python.org/downloads/release/python-3125/).
Install `pip`. Here is the command you have to execute on Windows inside an admin powershell :
```
python -m ensurepip --default-pip
```

1. Install the requirements with `pip install` :
```
pip install opencv-python numpy pygetwindow pynput Pillow
```

2. Clone this repository by downloading [zip](https://github.com/sptaule/m2-fish/archive/refs/heads/main.zip) directly or with :
```
git clone https://github.com/sptaule/m2-fish.git
```
  
3. Open the Metin2 game at 1024 x 768 resolution (this is important for now)
4. Place the game window at (0, 0) which corresponds to the top left corner as accurately as you can (this is important for now)
5. Make sure the game window's title is "METIN2", otherwise add its name to "servers" block inside the script and use it inside "params" block
6. Zoom the camera so the character's feet are barely visible on the screen (it might requires multiple adjustments from you)
7. Put fishing action button on `F3` and your baits (paste or worms) on `F4` actionbar shortcuts
8. Launch the script with `python ./fishbot.py`

*Important*  
- Don't minimize the game window
- Don't hide the game window with any other window
- Don't move your mouse or type when the character is using bait or using fishing rod
- Your game's inventory must be at its original postion (bottom-right)
- It is strongly recommended that your active inventory page is empty (room to fish, using and detecting minnows, etc)

## Todo-list
- [ ] make it works with multiple game clients
- [ ] make it works with any window dimensions and positions
- [ ] make the camera zoom level more clear
- [ ] make it works with hidden (or even minimized?) windows with the help of `PrintWindow` function from the Windows API
