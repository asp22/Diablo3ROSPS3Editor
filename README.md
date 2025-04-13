# Diablo 3 ROS PS3 Save Editor 

A small `python` tool to help you modify your PS3 Save Data.

## Newest Feature
- Create Horadric Caches
  - Under the Hero Inventory Menu there is an option to fill all unused inventory slots with a Horadric Cache (Torment 6)
  - Level of Cache is set to be the same as the Hero's level

## Quick Start
- Install `python3`
  - developed using `3.13.2` but I don't use any fancy features so an older version will probably work
- Install `window-curses`; only required for Windows; lib is needed for User Interface
   ```bash
   pip3 install window-curses
   ```
- Install `cryptography`; lib is needed to decrypt PS3 Save
   ```bash
   pip3 install cryptography
   ```
- Get your Saved Game from your PS3
- Create a backup
- `git clone` or download this project
- Open `command prompt` and navigate to the clone/downloaded location and run
  ```
  python3 ./app.py --in_dir <path to your saved PS3 Dir>
  e.g. 
  python3 ./app.py --in_dir c:\Users\asp22\Desktop\PS3\SAVEDATA\BLES02035-AUTOSAVE
- Interface

  | Key | Action |
  |----------|----------|
  | `Up`/`Down Arrow` | Menu Navigation / Increment or Decrement Value|
  | `Left Arrow` | Navigate to Submenu |
  | `Right Arrow` | Return to previous menu |
  | `Q` | Return to previous menu / Exit Application |
  | `Enter` | Accept modified Value |
  | `Ctrl + c` | Abort - Force app to restore files to state at start up |

## Various Screen Shots

### Main Menu
When you run the app, you'll be shown an `Account` entry and all of your `Heros` listed. At the bottom there is a `Savable` item that will allow you to save when an edit is made

![main menu](https://github.com/asp22/Diablo3ROSPS3Editor/blob/main/images/main_menu.png)

### Account
Within the account menu, you can 
- update shared currencies like gold and blood shards
- change paragon level
- update stash items

![account menu](https://github.com/asp22/Diablo3ROSPS3Editor/blob/main/images/account_menu.png)

### Stash

![stash menu](https://github.com/asp22/Diablo3ROSPS3Editor/blob/main/images/stash_menu.png)

### Item Edit

![stash](https://github.com/asp22/Diablo3ROSPS3Editor/blob/main/images/item_edit_menu.png)

### Add New Effect

![effect_selection](https://github.com/asp22/Diablo3ROSPS3Editor/blob/main/images/effect_selection_menu.png)

### Edits Savable
After making an edit, note that in the Main Menu, the option to Save is now enabled. If you're happy with your edits.
- naviagte to `Saveable`
- press `Left Arrow` or `Return`.
- Exit the application with `Q`.

You can press `Ctrl+c` at any time to discard any changes and exit the applicaiton.

![main_menu_savable](https://github.com/asp22/Diablo3ROSPS3Editor/blob/main/images/main_menu_savable.png)


## Limitations
- No item creation or duplication; Except for the Fill Empty Inventory Slots with a Horadric Cache 
- No hero creation.
- Paragon Levels: If you edit the paragon level the app will update all Heros and reset allocated paragon points. i.e. you'll have to reallocate in game
- Sockets. I've not spent time to understand how items with sockets and gems are representing in save game data. If you want to remove a socket affix from an item, I would recommend that you remove the gems in game first and then use the editor to change the socket affix for something else.
- Clearly, I've not tested all the possible affix values. If you find one that doesn't work raise an issue and I'll mark it as dead
- Item limits. I do not know what the various item stack size limits are. In code, I've limited it to 1000 but I do not know if this is safe for all items.

## Credits
GoobyCorp - GBIDs/AFFIX json files - and XOR logic for decrypting and encrypting
