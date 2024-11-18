from curses import wrapper
from curses.textpad import Textbox, rectangle
import curses
import sys
#class acursors:

#-------------------------------------------------------------------------------
def mainloop(stdscr):
    
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLUE)
    curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_RED)
    curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_GREEN)
    
    editwin = curses.newwin(5,10, 2,10)
    #rectangle(editwin, 1,1, 1+5+1, 1+5+1)
    editwin.bkgd(' ', curses.color_pair(1) | curses.A_BOLD)
     
    
    
    stdscr.bkgd(' ', curses.color_pair(1) | curses.A_BOLD)
    
    stdscr.refresh()
    
    X=5
    Y=5
    
    rows, cols = stdscr.getmaxyx()
    

    
    while True:
        
        curses.curs_set(1)
        
        

        
        k = stdscr.getkey()
        if k == "q":
            sys.exit(0)
            
        elif k == "KEY_UP":
            Y-=1
        elif k == "KEY_DOWN":
           Y+=1
        elif k == "KEY_LEFT":
            X-=1
        elif k == "KEY_RIGHT":
            X+=1
            
            
        sString='X'
        
        
        if X< 1:
            X=1
        if Y< 1:
            Y=1
        if Y> rows-1:
            Y=rows-1
            
        if X> cols-1 - len(sString):
            X=cols-1 - len(sString)
            
        stdscr.addstr(Y, X, " X ")
        stdscr.addstr(Y, X, "")     
        
            
        stdscr.addstr(1, 15, 'R=' + str(rows))
        stdscr.addstr(1, 20,  'C=' + str(cols))
        stdscr.addstr(1, 25, 'Ry=' + str(Y)+'  ')
        stdscr.addstr(1, 30,  'Cx=' + str(X)+ '  ')
        
        stdscr.addstr(10, 10, "hello  \n world")
        
        editwin.addstr(1, 1, "EDIT WIN")  
        editwin.refresh
        editwin.getkey
            
            
        curses.curs_set(1)

        stdscr.refresh()
       
#============================================================================
#============================================================================
        
###############################################################################
if __name__ == '__main__':
    
    print ("======================================================")
    print ("TEST CODE acursors.py=================================")
    print ("======================================================")
    

   
    curses.wrapper(mainloop)