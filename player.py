class Player():
    def __init__(self, id) -> None:
        self._id = id
        self._side = None
    
    @property
    def id(self):
        return(self._id)
    
    @property
    def side(self):
        return(self._side)

    @side.setter
    def side(self, side_):
        if side_ == True:
            self._side = 'Good'
        elif side_ == False:
            self._side = 'Evil'

    @property
    def role(self):
        return(self._role)

    @role.setter
    def role(self, role_):
        self._role = role_
