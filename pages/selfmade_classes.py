import dominate
from dominate.tags import *
from sanic import Sanic

from config import APP_NAME


class tournament:
    def __init__(self, name, contestant, matches, description):
        self.name = name
        self.contestant = contestant
        self.matches = matches
        self.description = description 
        
    def show_tournaments(self):
        print("...")
        with div(cls="banner"):
            h1(self.name)
            p("contestants:"+ self.contestant, )
            p("matches:" + self.matches)
            p("description:"+ self.description)
            with div(cls="button"):
                a("view more", cls='button', href="/editor")


class matches:
    def __init__(self, contestant_A,contestant_B, ):
        self.contestant_A = contestant_A
        self.contestant_B = contestant_B
