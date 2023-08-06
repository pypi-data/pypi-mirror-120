class Hello:
    who:str

    def __init__(self,who):
        self.who = who
        
    def say(self):
        print(f"Hello, {self.who}")

    def get_who(self):
        return self.who