def draw_table(stdscr, title: str, rows: list[str]) -> None:
    stdscr.clear()
    h, w = stdscr.getmaxyx()

    stdscr.addstr(1, w // 2 - len(title) // 2, title)

    y = 3
    if not rows:
        stdscr.addstr(y, 2, "(empty)")
        y += 1
    else:
        for row in rows:
            stdscr.addstr(y, 2, row)
            y += 1

    stdscr.addstr(h - 2, 2, "Press any key to return...")
    stdscr.refresh()
    stdscr.getch()


def show_message(stdscr, msg: str) -> None:
    stdscr.clear()
    stdscr.addstr(3, 3, msg)
    stdscr.addstr(5, 3, "Press any key to return...")
    stdscr.refresh()
    stdscr.getch()
    
    