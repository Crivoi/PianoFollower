try:
    import Tkinter as tk
except ImportError:
    import tkinter as tk


class DefaultToplevel(tk.Toplevel):
    def __init__(self, parent):
        self.height = 50
        self.width = parent.width
        self.bg = 'darkgrey'
        tk.Toplevel.__init__(self, height=self.height, width=self.width, bg=self.bg)
        self.resizable(False, False)
        self.parent = parent
        self.x = int(parent.x)
        self.y = int(parent.y)
        self.geometry('{}x{}+{}+{}'.format(self.width, self.height, self.x, self.y))
        self.init_ui()

    def init_ui(self):
        pass


if __name__ == '__main__':
    pass
