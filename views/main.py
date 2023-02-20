from typing import TypedDict

from .root import Root
from .home import HomeView
from .signin import SignInView
from .signup import SignUpView


class Frames(TypedDict):
    signup: SignUpView
    signin: SignInView
    home: HomeView


class View:
    def __init__(self):
        self.root = Root()
        self.frames: Frames = {}  # type: ignore

        self._add_frame(SignUpView, "signup")
        self._add_frame(SignInView, "signin")
        self._add_frame(HomeView, "home")

    def _add_frame(self, Frame, name: str) -> None:
        self.frames[name] = Frame(self.root)
        self.frames[name].grid(row=0, column=0, sticky="nsew")
        self.frames[name].bind('<<ShowFrame>>', self.printMessage)

    def printMessage(self, event):
        print('Hello!')        

    def switch(self, name: str) -> None:
        frame = self.frames[name]
        frame.tkraise()
        frame.event_generate('<<ShowFrame>>')

    def start_mainloop(self) -> None:
        self.root.mainloop()