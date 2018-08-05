class Audit():

    count = 1

    def __init__(self,title, year):
        self.title = title
        self.year = year
        self.id = Audit.count
        Audit.count += 1
