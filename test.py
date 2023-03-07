import tkinter as tk

root = tk.Tk()

class MyClass:
    def __init__(self, root) -> None:
        self.root = root

    def UI(self):
        self.e = tk.Entry(self.root, font = 20,borderwidth=5)
        self.e.pack()
        self.button = tk.Button(self.root, text="Click Me!")
        self.button['state'] = 'disabled'
        self.button.pack()

        self.e.bind('<KeyRelease>',lambda e: self.capture()) # Bind keyrelease to the function

    def capture(self):
        if self.e.get():
            self.button['state'] = 'normal'
        else:
            self.button['state'] = 'disabled'


myclass = MyClass(root)
myclass.UI()

root.mainloop()