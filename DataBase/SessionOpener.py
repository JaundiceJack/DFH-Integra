from DataBase import Session

#-----------------------------------------------------------------------------#

class OpenSession:
    def __enter__(self):
        self.session = Session()
        return self.session
    def __exit__(self, ex, exc, exce):
        self.session.close()