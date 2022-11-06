from player import Player
import random

class Game():
    max_player = 10
    min_player = 5
    roles = {
        5: ['Merlin','Assassin','Loyal Servant of Arthur','Loyal Servant of Arthur','Minion of Mordred'],
        6: ['Merlin','Assassin','Loyal Servant of Arthur','Loyal Servant of Arthur','Loyal Servant of Arthur','Minion of Mordred'],
        7: ['Merlin','Assassin','Loyal Servant of Arthur','Loyal Servant of Arthur','Loyal Servant of Arthur','Minion of Mordred','Minion of Mordred'],
        8: ['Merlin','Assassin','Loyal Servant of Arthur','Loyal Servant of Arthur','Loyal Servant of Arthur','Loyal Servant of Arthur','Minion of Mordred','Minion of Mordred'],
        9: ['Merlin','Assassin','Loyal Servant of Arthur','Loyal Servant of Arthur','Loyal Servant of Arthur','Loyal Servant of Arthur','Loyal Servant of Arthur','Minion of Mordred','Minion of Mordred'],
        10: ['Merlin','Assassin','Loyal Servant of Arthur','Loyal Servant of Arthur','Loyal Servant of Arthur','Loyal Servant of Arthur','Loyal Servant of Arthur','Minion of Mordred','Minion of Mordred','Minion of Mordred']
    }
    players_needed = {5:[2,3,2,3,3], 6:[2,3,4,3,4], 7:[2,3,3,4,4], 8:[3,4,4,5,5], 9:[3,4,4,5,5], 10:[3,4,4,5,5]}
    
    def __init__(self, id) -> None:
        self._number_of_players = 0
        self.quest_count = [None,None,None,None,None]
        self._players = []
        self.game_phase = None

    @property
    def players(self):
        return(self._players)

    @property
    def number_of_players(self):
        return(len(self.players))

    def add_player(self,id, name):
        # 0 = Added, 1 = Already in Game 2 = Max Player count
        if self.number_of_players == Game.max_player:
            return(2) 
        new_player = Player(id, name)
        for player in self._players:
            if player.id == new_player.id:
                # player in already in game
                return(1)
        self._players.append(new_player)
        return(0)
    
    def remove_player(self,id):
        # True = Removed, False = Not in Game
        for player in self._players:
            if player.id == id:
                self._players.remove(player)
                return(True)
        # player not in game
        return(False)

    @property
    def game_phase(self):
        return(self._game_phase)

    @game_phase.setter
    def game_phase(self, value):
        self._game_phase = value

    @property
    def reject_count(self):
        return(self._reject)
    
    @property
    def failure_needed(self):
        if self.game_phase == 3 and self.number_of_players > 7:
            return(2)
        return(1)

    @property
    def player_needed(self):
        return(Game.players_needed[self.number_of_players][self.game_phase])

    @property
    def current_leader(self):
        return(self._current_leader)

    @current_leader.setter
    def current_leader(self, player_object):
        self._current_leader = player_object

    @property
    def assassin(self):
        return(self._assassin)
    
    @assassin.setter
    def assassin(self, player_object):
        self._assassin = player_object

    def start_game(self):
        # True = started False = Not enough players
        if self.number_of_players < Game.min_player:
            return(False)
        # randomize players and assign roles
        self._players = random.sample(self.players, self.number_of_players)
        for index, role in enumerate(Game.roles[self.number_of_players]):
            self.players[index].role = role
            if role == 'Merlin' or role == 'Loyal Servant of Arthur':
                self.players[index].side = True
            else:
                if role == 'Assassin':
                    self.assassin = self.players[index]
                self.players[index].side = False
        # since players has been randomized, follow the random order for leader
        self.game_phase = 0
        self._votes = [None for i in self.players]
        self._reject = 0
        self.winner = None
        return(True)
    
    def determine_leader(self, index):
        if self.reject_count == 5 or self.quest_count.count(0) == 3:
                print('Evil Win!')
                self.winner = 'Evil'
                return(True)
        if self.quest_count.count(1) == 3:
            # self.assassin_trigger()
            return(False)
        self.current_leader = self.players[index]
        self.chosen_players = []
        print(f'{self.current_leader.id} is the Leader!')
    
    def choose_player(self, newly_chosen):
        # newly_chosen = input('Player:')
        # jus hardcode in telegram to not display repeat characters?
        newly_chosen = self.players[newly_chosen]
        self.chosen_players.append(newly_chosen)
        if len(self.chosen_players) == (self.player_needed):
            print(f'{self.current_leader.id} has chosen {[player.name for player in self.chosen_players]}')
            print('Please vote for the choice')
            # wait for voting

    @property
    def votes(self):
        return(self._votes)

    def voting(self, index, vote_):
        # vote_ will be 1/0
        # 1->Approve, 0->Reject
        self._votes[index] = vote_
        # After the vote, check if everyone voted
        # if everyone voted, reset votes and call next function
        # else continue
        if None not in self.votes:
            if sum(self.votes)/len(self.votes) > 0.5:
                print(self._votes)
                # self._votes = [None for i in self.players]
                self._reject = 0
                print('Vote passed!')
                # quest start
                print(f'Starting Quest {self.game_phase + 1}')
                self._quest_success = []
                # wait for choose_success_failure
            else:
                print(self._votes)
                # self._votes = [None for i in self.players]
                self._reject += 1

    def choose_success_failure(self, success):
        self._quest_success.append(success)
        if len(self._quest_success) == self.player_needed:
            if self._quest_success.count(0) >= self.failure_needed:
                print(self._quest_success)
                print(f'Quest {self.game_phase + 1} Failed')
                # move on to next leader voting and quest
                self.quest_count[self.game_phase] = 0
                self.game_phase += 1
            else:
                print(self._quest_success)
                print(f'Quest {self.game_phase + 1} Succeeded')
                self.quest_count[self.game_phase] = 1
                self.game_phase += 1

    def assassin_trigger(self, index):
        if self.players[int(index)].role == 'Merlin':
            print('The Assassin killed Merlin')
            print('Evil Wins')
            self.winner = 'Evil'
            return(True)
        else:
            print('Good Wins')
            self.winner = 'Good'
            return(False)
    
    @property
    def winner(self):
        return(self._winner)

    @winner.setter
    def winner(self,value):
        self._winner = value


    

    