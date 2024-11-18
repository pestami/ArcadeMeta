from curses import wrapper

from curses.textpad import Textbox, rectangle
import curses

def mainroutine(stdscr):
    # Clear screen

    stdscr.clear()
    
  
    
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLUE)
    curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_RED)
    curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_GREEN)

    # This raises ZeroDivisionError when i == 10.

 ##=====================================================================     
    largewin = curses.newwin(600,800, 1,1)
    largewin.bkgd(' ', curses.color_pair(1) | curses.A_BOLD)
    #----------------------
    largewin.addstr(0, 0, "Enter IM message: (hit Ctrl-G to send)")
    for i in range(1, 110):
            largewin.addstr(i,1,'10 divided by')     
    #-----------------------    
    largewin.refresh()
    largewin.getkey()
  ##=====================================================================  

    editwin = curses.newwin(5,30, 2,40)
    rectangle(largewin, 1,0, 1+5+1, 1+30+1)
    editwin.bkgd(' ', curses.color_pair(1) | curses.A_BOLD)
    
    largewin.refresh()

    box = Textbox(editwin)

    # Let the user edit until Ctrl-G is struck.
    box.edit()

    # Get resulting contents
    message = box.gather()  
    
    begin_x = 20
    begin_y = 7
    height = 5
    width = 40
    
    win2 = curses.newwin(height, width, begin_y, begin_x)
    
    win2.addstr(message)
    win2.addstr("WINDOW")

    win2.refresh()
    win2.getkey()
    
    editwin.addstr("WINDOW")

    editwin.refresh()
    editwin.getkey()
    
    largewin.addstr(0,0,"LARGE WINDOW")
    largewin.refresh()
    largewin.getkey()
    
    
if __name__ == '__main__':
    

    wrapper(mainroutine)
    
    S=2