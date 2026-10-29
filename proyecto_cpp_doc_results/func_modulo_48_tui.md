# MODULE: tui

## 1. PURPOSE
The tui module provides functions for creating a text-based user interface (TUI) in a terminal, including functions for text styling, cursor movement, and terminal manipulation.

## 2. CORE COMPONENTS
- `void textcolor(int attr, int fg, int bg)`: Changes the styling, foreground, and background character colors.
- `void textcolor_fg(int fg)`: Changes the foreground character color.
- `void textcolor_bg(int bg)`: Changes the background character color.
- `void textcolor_normal(void)`: Switches to normal color or intensity.
- `void textstyle(int attr)`: Switches the styling applied to future written characters.
- `void moveto(int x, int y)`: Moves the cursor to specified column and row.
- `void move(int which, int n)`: Moves the cursor a specified number of positions in the specified direction.
- `void erase_display(int n)`: Erases a subset of the terminal display.
- `void erase_line(int n)`: Erases part of the line in the terminal.
- `void hide_cursor(void)`: Hides the cursor within the terminal.
- `void show_cursor(void)`: Shows the cursor within the terminal.
- `void reset_term(void)`: Resets the terminal display to a known working state.
- `int mygetch(void)`: Wrapper around `getch` to avoid displaying the character on the terminal.
- `void console_utf8_enable(void)`: Enables UTF-8 support in the console.
- `static inline void console_puts(const char * msg)`: Prints a message and erases the line.

## 3. OUTGOING DEPENDENCIES (Calls/Uses)
- None

## 4. INCOMING DEPENDENCIES (Used By)
- None