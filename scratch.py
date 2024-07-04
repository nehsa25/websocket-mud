class Npc:
    name = ""
    def __init__(self, name=""):
        print("So am I!!!")
        if name != "":
            self.name = name

        print(f"And my name is: {self.name}")

class Guard(Npc):
    def __init__(self):
        print("I'm being constructed baby!")
        super().__init__(name="Maximus")

bob_the_guard = Guard()