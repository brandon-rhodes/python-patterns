from tkinter import Tk, Frame, Button

# Our routine, that gets to treat all widgets the same.

def print_tree(widget, indent=0):
    """Print a hierarchy of Tk widgets in the terminal."""
    print('{:<{}} * {!r}'.format('', indent * 4, widget))
    for child in widget.winfo_children():
        print_tree(child, indent + 1)

# A small sample GUI application with several widgets.

root = Tk()
f = Frame(master=root)
f.pack()

tree_button = Button(f)
tree_button['text'] = 'Print widget tree'
tree_button['command'] = lambda: print_tree(f)
tree_button.pack({'side': 'left'})

quit_button = Button(f)
quit_button['text'] = 'Quit Tk application'
quit_button['command'] =  f.quit
quit_button.pack({'side': 'left'})

f.mainloop()
root.destroy()
