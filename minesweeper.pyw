import random
import tkinter as tk

class Tile:
    def __init__(self):
        #n = nearby mines/if is a mine
        self.vis = False
        self.marked = False
        self.n = 0
    
    def make_label(self,where,x,y):
        #making label
        label = tk.Label(where,
                         text='?',
                         fg='black',
                         bg='white',
                         width=3)
        
        label.grid(row=x,
                   column=y,
                   padx=5,
                   pady=4)
        
        #let label affect gameplay
        label.bind('<Button-1>', self.reveal)
        label.bind('<Button-2>', self.mark)
        label.bind('<Button-3>', self.mark)

        self.label = label
    
    def update_label(self):
        #color
        colour = 'white'
        if (self.vis and self.n == 'm') or self.marked:
            colour = 'red'
        elif self.vis:
            colour = 'green'
        self.label.config(bg=colour)

        #text
        if self.marked:
            self.label.config(text='!')
            #cant reveal marked tile
            self.label.unbind('<Button-1>')

        elif self.vis:
            self.label.config(text=self.n)

        else:
            self.label.bind('<Button-1>', self.reveal)
            self.label.config(text='?')


    def mark(self,event):
        #marking tiles
        if self.marked:
            self.marked = False
        else:
            self.marked = True

            if self.n == 'm':
                self.wincheck()

        self.update_label()

    def wincheck(self):
        win = True
        #win condition: only all mine tiles marked
        for y in board:
            for x in y:
                #if non-mine tiles are marked, dont win
                if x.n != 'm' and x.marked:
                    win = False
                    break
                #if unmarked mine tiles
                elif x.n == 'm' and not x.marked:
                    win = False
                    break
        if win:
            game_end('YOU WIN!')

    def reveal(self,event):
        self.vis = True

        #if its a mine, lose
        if self.n == 'm':
            game_end('YOU LOSE!')
        else:
            global shownsafe
            shownsafe += 1
            if shownsafe == safe:
                game_end('YOU WIN!')

        self.update_label()

def generate_board(size):
    board = []
    frame = tk.Frame(root)
    frame.place(relx=0.5, rely=0.5, anchor='center')

    #generate empty board with no-value tiles
    for y in range(size):
        temp = []
        for x in range(size):
            temp.append(Tile())
        board.append(temp)

    #add mines
    #15-20% mines
    mines = random.randint(15,20)/100 * size**2
    #mines = 0
    placed = 0

    while mines > placed:
        #find where mine will be placed
        y = random.randint(0,size-1)
        x = random.randint(0,size-1)
        #done allow multiple mines on 1 tile
        if board[y][x].n == 'm':
            continue
        
        #place the mine
        board[y][x].n = 'm'
        placed += 1

        #add 1 value to adjacent tiles
        for a in range(-1,2):
            for b in range(-1,2):
                #dont add value to tiles with mines
                #dont add value to tiles outside the board
                try:
                    #extra check as -ve vals still work in lists
                    if y+a >= 0 and x+b >= 0:
                        board[y+a][x+b].n += 1
                except:
                    pass

    #make labels
    for y in board:
        for x in y:
            x.make_label(frame,y.index(x),board.index(y))
    
    return board, size**2-mines

def game_end(text):
    #reveal all tiles
    for y in board:
        for x in y:
            #show all tiles, dont let marking of tiles prevent seeing of whole board
            x.vis = True
            x.marked = False
            #dont allow clicking of tiles
            x.label.unbind('<Button-1>')
            x.label.unbind('<Button-2>')
            x.label.unbind('<Button-3>')
            
            x.update_label()

    #new screen thing saying u win or lose
    frame = tk.Frame(root)
    frame.place(relx=0.5, rely=0.5, anchor='center')
    #actual placing of text
    label = tk.Label(frame, text=text, font=('TkDefaultFont',20))
    label.bind('<Button-1>',lambda event: start_screen())
    label.pack()

def nvalid(entry):
    #basic number validation
    val = entry.get()
    try:
        val = int(val)
    except:
        return

    if val < 3:
        return

    #remove start screen
    for i in root.winfo_children():
        i.destroy()

    #start game
    global board,safe,shownsafe
    board, safe = generate_board(val)
    shownsafe = 0

def start_screen():
    #clear other frames
    for i in root.winfo_children():
        i.destroy()

    #start screen
    frame = tk.Frame(root)
    frame.pack(fill='both')

    tk.Label(frame,text='Size of board: ').pack()

    size_entry = tk.Entry(frame)
    size_entry.pack(pady=2)

    start_button = tk.Label(frame,text='START!',bg='white',fg='black')
    #can click button
    start_button.bind('<Button-1>',lambda event,entry = size_entry:nvalid(entry))
    start_button.pack(pady=2)

root = tk.Tk()
root.geometry('500x500')

start_screen()
root.mainloop()