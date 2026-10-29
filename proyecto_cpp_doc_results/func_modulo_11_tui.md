# MODULE: tui

## 1. PURPOSE
The `tui` module is responsible for handling the user interface and terminal interactions in the system. It provides functions for setting text colors, styles, moving the cursor, and managing terminal input.

## 2. CORE COMPONENTS
- `textcolor(int attr, int fg, int bg)`: Sets the text attributes and colors for terminal output.
- `textcolor_fg(int fg)`: Sets the foreground color of the text.
- `textcolor_bg(int bg)`: Sets the background color of the text.
- `textstyle(int attr)`: Sets the text style attributes.
- `reset_term(void)`: Resets the terminal settings to default.
- `moveto(int x, int y)`: Moves the cursor to the specified coordinates.
- `move(int which, int n)`: Moves the cursor by a specified number of positions in a given direction.
- `erase_display(int n)`: Erases a specified part of the display.
- `erase_line(int n)`: Erases a specified part of the current line.
- `textcolor_normal(void)`: Resets the text color and style to normal.
- `hide_cursor(void)`: Hides the terminal cursor.
- `show_cursor(void)`: Shows the terminal cursor.
- `mygetch(void)`: Reads a single character from the terminal without echoing it to the screen.
- `console_utf8_enable(void)`: Ensures the terminal is using UTF-8 encoding.

## 3. OUTGOING DEPENDENCIES (Calls/Uses)
- `console.h`: This module includes header files necessary for terminal control.
- `termios.h`: Used for terminal I/O operations.
- `unistd.h`: Used for system calls like `read` and `sleep`.

## 4. INCOMING DEPENDENCIES (Used By)
- `main.cpp`: Calls functions like `console_utf8_enable()` and `mygetch()` to handle terminal interactions.