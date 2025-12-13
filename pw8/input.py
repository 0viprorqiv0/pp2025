import curses
from curses import textpad

def curses_input(stdscr, prompt):
    stdscr.clear()
    h, w = stdscr.getmaxyx()

    stdscr.addstr(h // 2 - 2, w // 2 - len(prompt) // 2, prompt)

    edit_win = curses.newwin(1, 30, h // 2, w // 2 - 15)
    textpad.rectangle(stdscr, h // 2 - 1, w // 2 - 16, h // 2 + 1, w // 2 + 14)
    stdscr.refresh()

    box = textpad.Textbox(edit_win)
    box.edit(lambda x: x)
    content = edit_win.getstr().decode().strip()
    return content

