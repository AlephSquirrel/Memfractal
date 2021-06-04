import sys, argparse, re

def ErrMessage(e):
    sys.stderr.write('Error: ' + e)
    sys.exit(1)

def Memfractal(program):
    p = program.split('\n')
    top, bottom = None, None
    for i in range(len(p)):
        if re.search('^#+v#+$', p[i]):
            if top == None:
                top = i
            else:
                ErrMessage('Unexpected top edge at line %d' % (i + 1))
        if re.search('^#+\^#+$', p[i]):
            if bottom == None:
                bottom = i
            else:
                ErrMessage('Unexpected bottom edge at line %d' % (i + 1))
    if top == None:
        ErrMessage('Top edge not found')
    elif bottom == None:
        ErrMessage('Bottom edge not found')
    elif top > bottom:
        ErrMessage('Unexpected bottom edge at line %d' % (bottom + 1))
    north_arrow = p[top].find('v')
    south_arrow = p[bottom].find('^')
    width = len(p[top])
    if len(p[bottom]) != width:
        ErrMessage('Program is not a rectangle')
    
    west_arrow, east_arrow = None, None
    for i in range(top + 1, bottom):
        if len(p[i]) != width:
            ErrMessage('Program is not a rectangle')
        if p[i][0] == '>':
            if west_arrow == None:
                west_arrow = i
            else:
                ErrMessage('Unexpected > at line %d, column 0' % (i + 1))
        elif p[i][0] != '#':
            ErrMessage('Program is not enclosed')
        if p[i][-1] == '<':
            if east_arrow == None:
                east_arrow = i
            else:
                ErrMessage('Unexpected < at line %d, column %d' % (i + 1, width))
        elif p[i][-1] != '#':
            ErrMessage('Program is not enclosed')
    if west_arrow == None:
        ErrMessage('> not found')
    elif east_arrow == None:
        ErrMessage('< not found')
    
    ip_x = 0
    ip_y = west_arrow   # Start at the west arrow, facing east
    ip_dir = 0          # 0=east, 1=north, 2=west, 3=south
    data = set()        # Set of cells containing a 1
    curr_cell = []      # A list of locations where we have 'zoomed in'
    
    while(True):
        if ip_dir == 0: # Update ip position
            ip_x += 1
        elif ip_dir == 1:
            ip_y -= 1
        elif ip_dir == 2:
            ip_x -= 1
        else:
            ip_y += 1
            
        command = p[ip_y][ip_x]
        if command == ' ': # Check commands in order of likelyhood (roughly speaking)
            continue
        
        elif command == '/': # Reflections
            ip_dir = (1, 0, 3, 2)[ip_dir]
            
        elif command == '\\':
            ip_dir = (3, 2, 1, 0)[ip_dir]
            
        elif command == 'X':
            if tuple(curr_cell) in data:
                ip_dir = [1, 0, 3, 2][ip_dir]
            else:
                ip_dir = [3, 2, 1, 0][ip_dir]
        
        elif command == '+': # Enter a smaller copy of the code
            curr_cell.append((ip_x, ip_y))
            if ip_dir == 0:
                ip_x, ip_y = 0, west_arrow
            elif ip_dir == 1:
                ip_x, ip_y = south_arrow, bottom
            elif ip_dir == 2:
                ip_x, ip_y = width - 1, east_arrow
            else:
                ip_x, ip_y = north_arrow, top
        
        elif command == '*': # Toggle
            if tuple(curr_cell) in data:
                data.remove(tuple(curr_cell))
            else:
                data.add(tuple(curr_cell))
        
        elif command == '$': # Print
            print(1 if tuple(curr_cell) in data else 0, end='')
        
        elif command in '^v<>': # Exit this copy of the code
            if ip_x in range(1, width - 1) and ip_y in range(top + 1, bottom):
                ErrMessage('Unexpected %c at line %d, column %d' % (command, ip_y + 1, ip_x + 1))
            if not curr_cell:
                print('\nExited outer cell, leaving behind %d 1s' % len(data))
                sys.exit(0)
            else:
                (ip_x, ip_y) = curr_cell.pop()
            
        elif command == '#': # Wall
            if ip_x in range(1, width - 1) and ip_y in range(top + 1, bottom):
                ErrMessage('Unexpected # at line %d, column %d' % (ip_y + 1, ip_x + 1))
            ErrMessage('Crashed into the wall at line %d, column %d' % (ip_y + 1, ip_x + 1))
        
        else:
            ErrMessage('Invalid character %c at line %d, column %d' % (command, ip_y + 1, ip_x + 1))

try:
    parser = argparse.ArgumentParser(description='Run a Memfractal program')
    parser.add_argument('progname', metavar='progtorun', type=str,
        help='the filename of the Memfractal program to run')
    args = parser.parse_args()
    
    f = open(args.progname)
    prog = f.read()
    f.close()
    Memfractal(prog)
except IOError:
    ErrMessage("Can't open file '%s'" % args.progname)