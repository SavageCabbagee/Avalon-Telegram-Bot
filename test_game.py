import pytest
from game import Game
'''
This test is not really correct testing procedures and more of me simulating games
so it doesnt adhere to testing convention
'''
@pytest.fixture(scope='class', autouse=True)
def setUpGame(request):
    request.cls.game = Game(1)

class TestGame_EvilWinby3QuestFails():
    def test_init_game(self):
        '''
        Test that the game is initialised
        '''
        assert isinstance(self.game, Game)
        assert self.game.number_of_players == 0
    
    def test_adding_players(self,setUpGame):
        '''
        Test adding players
        '''
        assert self.game.number_of_players == 0
        self.game.add_player('0')
        assert self.game.number_of_players == 1
    
    def test_adding_same_player(self):
        '''
        Test adding same id for player which should fail and return 1
        '''
        assert self.game.number_of_players == 1
        assert self.game.add_player('0') == 1
        assert self.game.number_of_players == 1

    def test_removing_player(self):
        '''
        Test removing players
        '''
        assert self.game.number_of_players == 1
        self.game.remove_player('0')
        assert self.game.number_of_players == 0

    def test_adding_11th_player(self):
        '''
        Test adding more than >10 players which should fail
        '''
        assert self.game.number_of_players == 0
        self.game.add_player('0')
        self.game.add_player('1')
        self.game.add_player('2')
        self.game.add_player('3')
        self.game.add_player('4')
        self.game.add_player('5')
        self.game.add_player('6')
        self.game.add_player('7')
        self.game.add_player('8')
        self.game.add_player('9')
        assert self.game.number_of_players == 10
        before_adding = self.game.players
        assert self.game.add_player(10) == 2
        assert before_adding == self.game.players

    def test_adding_player_after_removing_one(self):
        '''
        Test that adding players works after removing one
        '''
        assert self.game.number_of_players == 10
        self.game.remove_player('2')
        assert self.game.number_of_players == 9
        self.game.add_player('11')
        assert self.game.number_of_players == 10

    def test_removing_non_existent_player(self):
        '''
        Test that removing a non-existent player works
        '''
        assert not self.game.remove_player(111)

    def test_start_game(self):
        '''
        Test that start_game starts the games properly
        and proper values are set
        '''
        self.game.start_game()
        good_players = 0
        evil_players = 0
        merlin = 0
        assassin = 0
        for player in self.game.players:
            if player.role == 'Merlin':
                merlin += 1
            if player.role == 'Assassin':
                assassin += 1
            if player.side == 'Good':
                good_players += 1
            else:
                evil_players += 1
        print([player.id for player in self.game.players])
        assert evil_players == 4
        assert good_players == 6
        assert merlin == 1
        assert evil_players == 4
        assert assassin == 1
        assert self.game.game_phase == 0
        assert self.game._votes == [None,None,None,None,None,None,None,None,None,None]
        assert self.game._reject == 0

    def test_game_fail_via_3_fails(self,monkeypatch):
        '''
        Test leader choosing players for 1st quest
        '''
        monkeypatch.setattr('builtins.input', lambda _:'3')
        self.game.choose_player()
        assert self.game.chosen_players == ['3']
        monkeypatch.setattr('builtins.input', lambda _:'6')
        self.game.choose_player()
        assert self.game.chosen_players == ['3','6']
        monkeypatch.setattr('builtins.input', lambda _:'5')
        self.game.choose_player()
        assert self.game.chosen_players == ['3','6','5']
        '''
        Test voting succeed for 1st quest
        '''
        self.game.voting(0,1)
        self.game.voting(1,1)
        self.game.voting(2,1)
        self.game.voting(3,1)
        self.game.voting(4,1)
        self.game.voting(5,1)
        self.game.voting(6,1)
        self.game.voting(7,1)
        self.game.voting(8,1)
        self.game.voting(9,0)
        # ensure votes are reset
        assert self.game.votes == [None,None,None,None,None,None,None,None,None,None]
        self.game.choose_success_failure(0)
        self.game.choose_success_failure(1)
        self.game.choose_success_failure(1)
        assert self.game.quest_count[0] == 0
        assert self.game.quest_count[1] == 1
        '''
        Test leader choosing players for 2nd quest
        '''
        monkeypatch.setattr('builtins.input', lambda _:'3')
        self.game.choose_player()
        assert self.game.chosen_players == ['3']
        monkeypatch.setattr('builtins.input', lambda _:'6')
        self.game.choose_player()
        assert self.game.chosen_players == ['3','6']
        monkeypatch.setattr('builtins.input', lambda _:'5')
        self.game.choose_player()
        assert self.game.chosen_players == ['3','6','5']
        monkeypatch.setattr('builtins.input', lambda _:'7')
        self.game.choose_player()
        assert self.game.chosen_players == ['3','6','5','7']
        '''
        Test voting succeed for 2nd quest
        '''
        self.game.voting(0,1)
        self.game.voting(1,1)
        self.game.voting(2,1)
        self.game.voting(3,1)
        self.game.voting(4,1)
        self.game.voting(5,1)
        self.game.voting(6,1)
        self.game.voting(7,1)
        self.game.voting(8,1)
        self.game.voting(9,0)
        # ensure votes are reset
        assert self.game.votes == [None,None,None,None,None,None,None,None,None,None]
        self.game.choose_success_failure(0)
        self.game.choose_success_failure(1)
        self.game.choose_success_failure(1)
        self.game.choose_success_failure(1)
        assert self.game.quest_count[0] == 0
        assert self.game.quest_count[1] == 2
        '''
        Test leader choosing players for 3rd quest
        '''
        monkeypatch.setattr('builtins.input', lambda _:'3')
        self.game.choose_player()
        assert self.game.chosen_players == ['3']
        monkeypatch.setattr('builtins.input', lambda _:'6')
        self.game.choose_player()
        assert self.game.chosen_players == ['3','6']
        monkeypatch.setattr('builtins.input', lambda _:'5')
        self.game.choose_player()
        assert self.game.chosen_players == ['3','6','5']
        monkeypatch.setattr('builtins.input', lambda _:'7')
        self.game.choose_player()
        assert self.game.chosen_players == ['3','6','5','7']
        '''
        Test voting succeed for 3rd quest
        '''
        self.game.voting(0,1)
        self.game.voting(1,1)
        self.game.voting(2,1)
        self.game.voting(3,1)
        self.game.voting(4,1)
        self.game.voting(5,1)
        self.game.voting(6,1)
        self.game.voting(7,1)
        self.game.voting(8,1)
        self.game.voting(9,0)
        # ensure votes are reset
        assert self.game.votes == [None,None,None,None,None,None,None,None,None,None]
        self.game.choose_success_failure(0)
        self.game.choose_success_failure(1)
        self.game.choose_success_failure(1)
        self.game.choose_success_failure(1)
        assert self.game.quest_count[0] == 0
        assert self.game.quest_count[1] == 3
        assert self.game.winner == 'Evil'       

class TestGame_EvilWinby3QuestFailsWith4thQuestRequiring2Fails():
    def test_init_game(self):
        '''
        Test that the game is initialised
        '''
        assert isinstance(self.game, Game)
        assert self.game.number_of_players == 0
    
    def test_adding_players(self,setUpGame):
        '''
        Test adding players
        '''
        assert self.game.number_of_players == 0
        self.game.add_player('0')
        assert self.game.number_of_players == 1
    
    def test_adding_same_player(self):
        '''
        Test adding same id for player which should fail and return 1
        '''
        assert self.game.number_of_players == 1
        assert self.game.add_player('0') == 1
        assert self.game.number_of_players == 1

    def test_removing_player(self):
        '''
        Test removing players
        '''
        assert self.game.number_of_players == 1
        self.game.remove_player('0')
        assert self.game.number_of_players == 0

    def test_adding_11th_player(self):
        '''
        Test adding more than >10 players which should fail
        '''
        assert self.game.number_of_players == 0
        self.game.add_player('0')
        self.game.add_player('1')
        self.game.add_player('2')
        self.game.add_player('3')
        self.game.add_player('4')
        self.game.add_player('5')
        self.game.add_player('6')
        self.game.add_player('7')
        self.game.add_player('8')
        self.game.add_player('9')
        assert self.game.number_of_players == 10
        before_adding = self.game.players
        assert self.game.add_player(10) == 2
        assert before_adding == self.game.players

    def test_adding_player_after_removing_one(self):
        '''
        Test that adding players works after removing one
        '''
        assert self.game.number_of_players == 10
        self.game.remove_player('2')
        assert self.game.number_of_players == 9
        self.game.add_player('11')
        assert self.game.number_of_players == 10

    def test_removing_non_existent_player(self):
        '''
        Test that removing a non-existent player works
        '''
        assert not self.game.remove_player(111)

    def test_start_game(self):
        '''
        Test that start_game starts the games properly
        and proper values are set
        '''
        self.game.start_game()
        good_players = 0
        evil_players = 0
        merlin = 0
        assassin = 0
        for player in self.game.players:
            if player.role == 'Merlin':
                merlin += 1
            if player.role == 'Assassin':
                assassin += 1
            if player.side == 'Good':
                good_players += 1
            else:
                evil_players += 1
        print([player.id for player in self.game.players])
        assert evil_players == 4
        assert good_players == 6
        assert merlin == 1
        assert evil_players == 4
        assert assassin == 1
        assert self.game.game_phase == 0
        assert self.game._votes == [None,None,None,None,None,None,None,None,None,None]
        assert self.game._reject == 0

    def test_game_fail_via_3_fails(self,monkeypatch):
        '''
        Test leader choosing players for 1st quest
        '''
        monkeypatch.setattr('builtins.input', lambda _:'3')
        self.game.choose_player()
        assert self.game.chosen_players == ['3']
        monkeypatch.setattr('builtins.input', lambda _:'6')
        self.game.choose_player()
        assert self.game.chosen_players == ['3','6']
        monkeypatch.setattr('builtins.input', lambda _:'5')
        self.game.choose_player()
        assert self.game.chosen_players == ['3','6','5']
        '''
        Test voting succeed for 1st quest
        '''
        self.game.voting(0,1)
        self.game.voting(1,1)
        self.game.voting(2,1)
        self.game.voting(3,1)
        self.game.voting(4,1)
        self.game.voting(5,1)
        self.game.voting(6,1)
        self.game.voting(7,1)
        self.game.voting(8,1)
        self.game.voting(9,0)
        # ensure votes are reset
        assert self.game.votes == [None,None,None,None,None,None,None,None,None,None]
        self.game.choose_success_failure(0)
        self.game.choose_success_failure(1)
        self.game.choose_success_failure(1)
        assert self.game.quest_count[0] == 0
        assert self.game.quest_count[1] == 1
        '''
        Test leader choosing players for 2nd quest
        '''
        monkeypatch.setattr('builtins.input', lambda _:'3')
        self.game.choose_player()
        assert self.game.chosen_players == ['3']
        monkeypatch.setattr('builtins.input', lambda _:'6')
        self.game.choose_player()
        assert self.game.chosen_players == ['3','6']
        monkeypatch.setattr('builtins.input', lambda _:'5')
        self.game.choose_player()
        assert self.game.chosen_players == ['3','6','5']
        monkeypatch.setattr('builtins.input', lambda _:'7')
        self.game.choose_player()
        assert self.game.chosen_players == ['3','6','5','7']
        '''
        Test voting succeed for 2nd quest
        '''
        self.game.voting(0,1)
        self.game.voting(1,1)
        self.game.voting(2,1)
        self.game.voting(3,1)
        self.game.voting(4,1)
        self.game.voting(5,1)
        self.game.voting(6,1)
        self.game.voting(7,1)
        self.game.voting(8,1)
        self.game.voting(9,0)
        # ensure votes are reset
        assert self.game.votes == [None,None,None,None,None,None,None,None,None,None]
        self.game.choose_success_failure(0)
        self.game.choose_success_failure(1)
        self.game.choose_success_failure(1)
        self.game.choose_success_failure(1)
        assert self.game.quest_count[0] == 0
        assert self.game.quest_count[1] == 2
        '''
        Test leader choosing players for 3rd quest
        '''
        monkeypatch.setattr('builtins.input', lambda _:'3')
        self.game.choose_player()
        assert self.game.chosen_players == ['3']
        monkeypatch.setattr('builtins.input', lambda _:'6')
        self.game.choose_player()
        assert self.game.chosen_players == ['3','6']
        monkeypatch.setattr('builtins.input', lambda _:'5')
        self.game.choose_player()
        assert self.game.chosen_players == ['3','6','5']
        monkeypatch.setattr('builtins.input', lambda _:'7')
        self.game.choose_player()
        assert self.game.chosen_players == ['3','6','5','7']
        '''
        Test voting succeed for 3rd quest
        '''
        self.game.voting(0,1)
        self.game.voting(1,1)
        self.game.voting(2,1)
        self.game.voting(3,1)
        self.game.voting(4,1)
        self.game.voting(5,1)
        self.game.voting(6,1)
        self.game.voting(7,1)
        self.game.voting(8,1)
        self.game.voting(9,0)
        # ensure votes are reset
        assert self.game.votes == [None,None,None,None,None,None,None,None,None,None]
        self.game.choose_success_failure(1)
        self.game.choose_success_failure(1)
        self.game.choose_success_failure(1)
        self.game.choose_success_failure(1)
        assert self.game.quest_count[0] == 1
        assert self.game.quest_count[1] == 2
        '''
        Test leader choosing players for 4th quest
        '''
        monkeypatch.setattr('builtins.input', lambda _:'3')
        self.game.choose_player()
        assert self.game.chosen_players == ['3']
        monkeypatch.setattr('builtins.input', lambda _:'6')
        self.game.choose_player()
        assert self.game.chosen_players == ['3','6']
        monkeypatch.setattr('builtins.input', lambda _:'5')
        self.game.choose_player()
        assert self.game.chosen_players == ['3','6','5']
        monkeypatch.setattr('builtins.input', lambda _:'7')
        self.game.choose_player()
        assert self.game.chosen_players == ['3','6','5','7']
        monkeypatch.setattr('builtins.input', lambda _:'8')
        self.game.choose_player()
        assert self.game.chosen_players == ['3','6','5','7','8']
        '''
        Test voting succeed for 3rd quest
        '''
        self.game.voting(0,1)
        self.game.voting(1,1)
        self.game.voting(2,1)
        self.game.voting(3,1)
        self.game.voting(4,1)
        self.game.voting(5,1)
        self.game.voting(6,1)
        self.game.voting(7,1)
        self.game.voting(8,1)
        self.game.voting(9,0)
        # ensure votes are reset
        assert self.game.votes == [None,None,None,None,None,None,None,None,None,None]
        self.game.choose_success_failure(0)
        self.game.choose_success_failure(0)
        self.game.choose_success_failure(1)
        self.game.choose_success_failure(1)
        self.game.choose_success_failure(1)
        assert self.game.quest_count[0] == 1
        assert self.game.quest_count[1] == 3
        assert self.game.winner == 'Evil'       

class TestGame_EvilWinby5Rejects():
    def test_init_game(self):
        '''
        Test that the game is initialised
        '''
        assert isinstance(self.game, Game)
        assert self.game.number_of_players == 0
    
    def test_adding_players(self,setUpGame):
        '''
        Test adding players
        '''
        assert self.game.number_of_players == 0
        self.game.add_player('0')
        assert self.game.number_of_players == 1
    
    def test_adding_same_player(self):
        '''
        Test adding same id for player which should fail and return 1
        '''
        assert self.game.number_of_players == 1
        assert self.game.add_player('0') == 1
        assert self.game.number_of_players == 1

    def test_removing_player(self):
        '''
        Test removing players
        '''
        assert self.game.number_of_players == 1
        self.game.remove_player('0')
        assert self.game.number_of_players == 0

    def test_adding_11th_player(self):
        '''
        Test adding more than >10 players which should fail
        '''
        assert self.game.number_of_players == 0
        self.game.add_player('0')
        self.game.add_player('1')
        self.game.add_player('2')
        self.game.add_player('3')
        self.game.add_player('4')
        self.game.add_player('5')
        self.game.add_player('6')
        self.game.add_player('7')
        self.game.add_player('8')
        self.game.add_player('9')
        assert self.game.number_of_players == 10
        before_adding = self.game.players
        assert self.game.add_player(10) == 2
        assert before_adding == self.game.players

    def test_adding_player_after_removing_one(self):
        '''
        Test that adding players works after removing one
        '''
        assert self.game.number_of_players == 10
        self.game.remove_player('2')
        assert self.game.number_of_players == 9
        self.game.add_player('11')
        assert self.game.number_of_players == 10

    def test_removing_non_existent_player(self):
        '''
        Test that removing a non-existent player works
        '''
        assert not self.game.remove_player(111)

    def test_start_game(self):
        '''
        Test that start_game starts the games properly
        and proper values are set
        '''
        self.game.start_game()
        good_players = 0
        evil_players = 0
        merlin = 0
        assassin = 0
        for player in self.game.players:
            if player.role == 'Merlin':
                merlin += 1
            if player.role == 'Assassin':
                assassin += 1
            if player.side == 'Good':
                good_players += 1
            else:
                evil_players += 1
        print([player.id for player in self.game.players])
        assert evil_players == 4
        assert good_players == 6
        assert merlin == 1
        assert evil_players == 4
        assert assassin == 1
        assert self.game.game_phase == 0
        assert self.game._votes == [None,None,None,None,None,None,None,None,None,None]
        assert self.game._reject == 0

    def test_game_fail_via_5_rejects(self,monkeypatch):
        '''
        Test leader choosing players 1st time
        '''
        monkeypatch.setattr('builtins.input', lambda _:'3')
        self.game.choose_player()
        assert self.game.chosen_players == ['3']
        monkeypatch.setattr('builtins.input', lambda _:'6')
        self.game.choose_player()
        assert self.game.chosen_players == ['3','6']
        monkeypatch.setattr('builtins.input', lambda _:'5')
        self.game.choose_player()
        assert self.game.chosen_players == ['3','6','5']
        '''
        Test voting fail 1st time
        '''
        self.game.voting(0,1)
        self.game.voting(1,1)
        self.game.voting(2,1)
        self.game.voting(3,1)
        self.game.voting(4,1)
        self.game.voting(5,0)
        self.game.voting(6,0)
        self.game.voting(7,0)
        self.game.voting(8,0)
        self.game.voting(9,0)
        assert self.game.reject_count == 1
        '''
        Test leader choosing players 2nd time
        '''
        monkeypatch.setattr('builtins.input', lambda _:'3')
        self.game.choose_player()
        assert self.game.chosen_players == ['3']
        monkeypatch.setattr('builtins.input', lambda _:'6')
        self.game.choose_player()
        assert self.game.chosen_players == ['3','6']
        monkeypatch.setattr('builtins.input', lambda _:'5')
        self.game.choose_player()
        assert self.game.chosen_players == ['3','6','5']
        '''
        Test voting fail 2nd time
        '''
        self.game.voting(0,1)
        self.game.voting(1,1)
        self.game.voting(2,1)
        self.game.voting(3,0)
        self.game.voting(4,0)
        self.game.voting(5,0)
        self.game.voting(6,0)
        self.game.voting(7,0)
        self.game.voting(8,0)
        self.game.voting(9,0)
        assert self.game.reject_count == 2
        '''
        Test leader choosing players 3rd time
        '''
        monkeypatch.setattr('builtins.input', lambda _:'3')
        self.game.choose_player()
        assert self.game.chosen_players == ['3']
        monkeypatch.setattr('builtins.input', lambda _:'6')
        self.game.choose_player()
        assert self.game.chosen_players == ['3','6']
        monkeypatch.setattr('builtins.input', lambda _:'5')
        self.game.choose_player()
        assert self.game.chosen_players == ['3','6','5']
        '''
        Test voting fail 3rd time
        '''
        self.game.voting(0,1)
        self.game.voting(1,1)
        self.game.voting(2,1)
        self.game.voting(3,1)
        self.game.voting(4,0)
        self.game.voting(5,0)
        self.game.voting(6,0)
        self.game.voting(7,0)
        self.game.voting(8,0)
        self.game.voting(9,0)
        assert self.game.reject_count == 3
        '''
        Test leader choosing players 4th time
        '''
        monkeypatch.setattr('builtins.input', lambda _:'3')
        self.game.choose_player()
        assert self.game.chosen_players == ['3']
        monkeypatch.setattr('builtins.input', lambda _:'6')
        self.game.choose_player()
        assert self.game.chosen_players == ['3','6']
        monkeypatch.setattr('builtins.input', lambda _:'5')
        self.game.choose_player()
        assert self.game.chosen_players == ['3','6','5']
        '''
        Test voting fail 4th time
        '''
        self.game.voting(0,1)
        self.game.voting(1,1)
        self.game.voting(2,1)
        self.game.voting(3,0)
        self.game.voting(4,0)
        self.game.voting(5,0)
        self.game.voting(6,0)
        self.game.voting(7,0)
        self.game.voting(8,0)
        self.game.voting(9,0)
        assert self.game.reject_count == 4
        '''
        Test leader choosing players 5th time
        '''
        monkeypatch.setattr('builtins.input', lambda _:'3')
        self.game.choose_player()
        assert self.game.chosen_players == ['3']
        monkeypatch.setattr('builtins.input', lambda _:'6')
        self.game.choose_player()
        assert self.game.chosen_players == ['3','6']
        monkeypatch.setattr('builtins.input', lambda _:'5')
        self.game.choose_player()
        assert self.game.chosen_players == ['3','6','5']
        '''
        Test voting fail 5th time
        '''
        self.game.voting(0,1)
        self.game.voting(1,1)
        self.game.voting(2,1)
        self.game.voting(3,1)
        self.game.voting(4,1)
        self.game.voting(5,0)
        self.game.voting(6,0)
        self.game.voting(7,0)
        self.game.voting(8,0)
        self.game.voting(9,0)
        assert self.game.reject_count == 5
        assert self.game.winner == 'Evil'    

class TestGame_EvilWinbyAssassinTrigger():
    def test_init_game(self):
        '''
        Test that the game is initialised
        '''
        assert isinstance(self.game, Game)
        assert self.game.number_of_players == 0
    
    def test_adding_players(self,setUpGame):
        '''
        Test adding players
        '''
        assert self.game.number_of_players == 0
        self.game.add_player('0')
        assert self.game.number_of_players == 1
    
    def test_adding_same_player(self):
        '''
        Test adding same id for player which should fail and return 1
        '''
        assert self.game.number_of_players == 1
        assert self.game.add_player('0') == 1
        assert self.game.number_of_players == 1

    def test_removing_player(self):
        '''
        Test removing players
        '''
        assert self.game.number_of_players == 1
        self.game.remove_player('0')
        assert self.game.number_of_players == 0

    def test_adding_11th_player(self):
        '''
        Test adding more than >10 players which should fail
        '''
        assert self.game.number_of_players == 0
        self.game.add_player('0')
        self.game.add_player('1')
        self.game.add_player('2')
        self.game.add_player('3')
        self.game.add_player('4')
        self.game.add_player('5')
        self.game.add_player('6')
        self.game.add_player('7')
        self.game.add_player('8')
        self.game.add_player('9')
        assert self.game.number_of_players == 10
        before_adding = self.game.players
        assert self.game.add_player(10) == 2
        assert before_adding == self.game.players

    def test_adding_player_after_removing_one(self):
        '''
        Test that adding players works after removing one
        '''
        assert self.game.number_of_players == 10
        self.game.remove_player('2')
        assert self.game.number_of_players == 9
        self.game.add_player('11')
        assert self.game.number_of_players == 10

    def test_removing_non_existent_player(self):
        '''
        Test that removing a non-existent player works
        '''
        assert not self.game.remove_player(111)

    def test_start_game(self):
        '''
        Test that start_game starts the games properly
        and proper values are set
        '''
        self.game.start_game()
        good_players = 0
        evil_players = 0
        merlin = 0
        assassin = 0
        for player in self.game.players:
            if player.role == 'Merlin':
                merlin += 1
            if player.role == 'Assassin':
                assassin += 1
            if player.side == 'Good':
                good_players += 1
            else:
                evil_players += 1
        print([player.id for player in self.game.players])
        assert evil_players == 4
        assert good_players == 6
        assert merlin == 1
        assert evil_players == 4
        assert assassin == 1
        assert self.game.game_phase == 0
        assert self.game._votes == [None,None,None,None,None,None,None,None,None,None]
        assert self.game._reject == 0

    def test_game_fail_via_3_fails(self,monkeypatch):
        '''
        Test leader choosing players for 1st quest
        '''
        monkeypatch.setattr('builtins.input', lambda _:'3')
        self.game.choose_player()
        assert self.game.chosen_players == ['3']
        monkeypatch.setattr('builtins.input', lambda _:'6')
        self.game.choose_player()
        assert self.game.chosen_players == ['3','6']
        monkeypatch.setattr('builtins.input', lambda _:'5')
        self.game.choose_player()
        assert self.game.chosen_players == ['3','6','5']
        '''
        Test voting succeed for 1st quest
        '''
        self.game.voting(0,1)
        self.game.voting(1,1)
        self.game.voting(2,1)
        self.game.voting(3,1)
        self.game.voting(4,1)
        self.game.voting(5,1)
        self.game.voting(6,1)
        self.game.voting(7,1)
        self.game.voting(8,1)
        self.game.voting(9,0)
        # ensure votes are reset
        assert self.game.votes == [None,None,None,None,None,None,None,None,None,None]
        self.game.choose_success_failure(1)
        self.game.choose_success_failure(1)
        self.game.choose_success_failure(1)
        assert self.game.quest_count[0] == 1
        assert self.game.quest_count[1] == 0
        '''
        Test leader choosing players for 2nd quest
        '''
        monkeypatch.setattr('builtins.input', lambda _:'3')
        self.game.choose_player()
        assert self.game.chosen_players == ['3']
        monkeypatch.setattr('builtins.input', lambda _:'6')
        self.game.choose_player()
        assert self.game.chosen_players == ['3','6']
        monkeypatch.setattr('builtins.input', lambda _:'5')
        self.game.choose_player()
        assert self.game.chosen_players == ['3','6','5']
        monkeypatch.setattr('builtins.input', lambda _:'7')
        self.game.choose_player()
        assert self.game.chosen_players == ['3','6','5','7']
        '''
        Test voting succeed for 2nd quest
        '''
        self.game.voting(0,1)
        self.game.voting(1,1)
        self.game.voting(2,1)
        self.game.voting(3,1)
        self.game.voting(4,1)
        self.game.voting(5,1)
        self.game.voting(6,1)
        self.game.voting(7,1)
        self.game.voting(8,1)
        self.game.voting(9,0)
        # ensure votes are reset
        assert self.game.votes == [None,None,None,None,None,None,None,None,None,None]
        self.game.choose_success_failure(1)
        self.game.choose_success_failure(1)
        self.game.choose_success_failure(1)
        self.game.choose_success_failure(1)
        assert self.game.quest_count[0] == 2
        assert self.game.quest_count[1] == 0
        '''
        Test leader choosing players for 3rd quest
        '''
        monkeypatch.setattr('builtins.input', lambda _:'3')
        self.game.choose_player()
        assert self.game.chosen_players == ['3']
        monkeypatch.setattr('builtins.input', lambda _:'6')
        self.game.choose_player()
        assert self.game.chosen_players == ['3','6']
        monkeypatch.setattr('builtins.input', lambda _:'5')
        self.game.choose_player()
        assert self.game.chosen_players == ['3','6','5']
        monkeypatch.setattr('builtins.input', lambda _:'7')
        self.game.choose_player()
        assert self.game.chosen_players == ['3','6','5','7']
        '''
        Test voting succeed for 3rd quest
        '''
        self.game.voting(0,1)
        self.game.voting(1,1)
        self.game.voting(2,1)
        self.game.voting(3,1)
        self.game.voting(4,1)
        self.game.voting(5,1)
        self.game.voting(6,1)
        self.game.voting(7,1)
        self.game.voting(8,1)
        self.game.voting(9,0)
        # ensure votes are reset
        assert self.game.votes == [None,None,None,None,None,None,None,None,None,None]
        for idx, player in enumerate(self.game.players):
            if player.role == 'Merlin':
                merlin_index = idx
        print(self.game.players[merlin_index].role)
        monkeypatch.setattr('builtins.input', lambda _: merlin_index)
        self.game.choose_success_failure(1)
        self.game.choose_success_failure(1)
        self.game.choose_success_failure(1)
        self.game.choose_success_failure(1)
        assert self.game.quest_count[0] == 3
        assert self.game.quest_count[1] == 0
        assert self.game.winner == 'Evil'  

class TestGame_GoodWinbyAssassinFailing():
    def test_init_game(self):
        '''
        Test that the game is initialised
        '''
        assert isinstance(self.game, Game)
        assert self.game.number_of_players == 0
    
    def test_adding_players(self,setUpGame):
        '''
        Test adding players
        '''
        assert self.game.number_of_players == 0
        self.game.add_player('0')
        assert self.game.number_of_players == 1
    
    def test_adding_same_player(self):
        '''
        Test adding same id for player which should fail and return 1
        '''
        assert self.game.number_of_players == 1
        assert self.game.add_player('0') == 1
        assert self.game.number_of_players == 1

    def test_removing_player(self):
        '''
        Test removing players
        '''
        assert self.game.number_of_players == 1
        self.game.remove_player('0')
        assert self.game.number_of_players == 0

    def test_adding_11th_player(self):
        '''
        Test adding more than >10 players which should fail
        '''
        assert self.game.number_of_players == 0
        self.game.add_player('0')
        self.game.add_player('1')
        self.game.add_player('2')
        self.game.add_player('3')
        self.game.add_player('4')
        self.game.add_player('5')
        self.game.add_player('6')
        self.game.add_player('7')
        self.game.add_player('8')
        self.game.add_player('9')
        assert self.game.number_of_players == 10
        before_adding = self.game.players
        assert self.game.add_player(10) == 2
        assert before_adding == self.game.players

    def test_adding_player_after_removing_one(self):
        '''
        Test that adding players works after removing one
        '''
        assert self.game.number_of_players == 10
        self.game.remove_player('2')
        assert self.game.number_of_players == 9
        self.game.add_player('11')
        assert self.game.number_of_players == 10

    def test_removing_non_existent_player(self):
        '''
        Test that removing a non-existent player works
        '''
        assert not self.game.remove_player(111)

    def test_start_game(self):
        '''
        Test that start_game starts the games properly
        and proper values are set
        '''
        self.game.start_game()
        good_players = 0
        evil_players = 0
        merlin = 0
        assassin = 0
        for player in self.game.players:
            if player.role == 'Merlin':
                merlin += 1
            if player.role == 'Assassin':
                assassin += 1
            if player.side == 'Good':
                good_players += 1
            else:
                evil_players += 1
        print([player.id for player in self.game.players])
        assert evil_players == 4
        assert good_players == 6
        assert merlin == 1
        assert evil_players == 4
        assert assassin == 1
        assert self.game.game_phase == 0
        assert self.game._votes == [None,None,None,None,None,None,None,None,None,None]
        assert self.game._reject == 0

    def test_game_fail_via_3_fails(self,monkeypatch):
        '''
        Test leader choosing players for 1st quest
        '''
        monkeypatch.setattr('builtins.input', lambda _:'3')
        self.game.choose_player()
        assert self.game.chosen_players == ['3']
        monkeypatch.setattr('builtins.input', lambda _:'6')
        self.game.choose_player()
        assert self.game.chosen_players == ['3','6']
        monkeypatch.setattr('builtins.input', lambda _:'5')
        self.game.choose_player()
        assert self.game.chosen_players == ['3','6','5']
        '''
        Test voting succeed for 1st quest
        '''
        self.game.voting(0,1)
        self.game.voting(1,1)
        self.game.voting(2,1)
        self.game.voting(3,1)
        self.game.voting(4,1)
        self.game.voting(5,1)
        self.game.voting(6,1)
        self.game.voting(7,1)
        self.game.voting(8,1)
        self.game.voting(9,0)
        # ensure votes are reset
        assert self.game.votes == [None,None,None,None,None,None,None,None,None,None]
        self.game.choose_success_failure(1)
        self.game.choose_success_failure(1)
        self.game.choose_success_failure(1)
        assert self.game.quest_count[0] == 1
        assert self.game.quest_count[1] == 0
        '''
        Test leader choosing players for 2nd quest
        '''
        monkeypatch.setattr('builtins.input', lambda _:'3')
        self.game.choose_player()
        assert self.game.chosen_players == ['3']
        monkeypatch.setattr('builtins.input', lambda _:'6')
        self.game.choose_player()
        assert self.game.chosen_players == ['3','6']
        monkeypatch.setattr('builtins.input', lambda _:'5')
        self.game.choose_player()
        assert self.game.chosen_players == ['3','6','5']
        monkeypatch.setattr('builtins.input', lambda _:'7')
        self.game.choose_player()
        assert self.game.chosen_players == ['3','6','5','7']
        '''
        Test voting succeed for 2nd quest
        '''
        self.game.voting(0,1)
        self.game.voting(1,1)
        self.game.voting(2,1)
        self.game.voting(3,1)
        self.game.voting(4,1)
        self.game.voting(5,1)
        self.game.voting(6,1)
        self.game.voting(7,1)
        self.game.voting(8,1)
        self.game.voting(9,0)
        # ensure votes are reset
        assert self.game.votes == [None,None,None,None,None,None,None,None,None,None]
        self.game.choose_success_failure(1)
        self.game.choose_success_failure(1)
        self.game.choose_success_failure(1)
        self.game.choose_success_failure(1)
        assert self.game.quest_count[0] == 2
        assert self.game.quest_count[1] == 0
        '''
        Test leader choosing players for 3rd quest
        '''
        monkeypatch.setattr('builtins.input', lambda _:'3')
        self.game.choose_player()
        assert self.game.chosen_players == ['3']
        monkeypatch.setattr('builtins.input', lambda _:'6')
        self.game.choose_player()
        assert self.game.chosen_players == ['3','6']
        monkeypatch.setattr('builtins.input', lambda _:'5')
        self.game.choose_player()
        assert self.game.chosen_players == ['3','6','5']
        monkeypatch.setattr('builtins.input', lambda _:'7')
        self.game.choose_player()
        assert self.game.chosen_players == ['3','6','5','7']
        '''
        Test voting succeed for 3rd quest
        '''
        self.game.voting(0,1)
        self.game.voting(1,1)
        self.game.voting(2,1)
        self.game.voting(3,1)
        self.game.voting(4,1)
        self.game.voting(5,1)
        self.game.voting(6,1)
        self.game.voting(7,1)
        self.game.voting(8,1)
        self.game.voting(9,0)
        # ensure votes are reset
        assert self.game.votes == [None,None,None,None,None,None,None,None,None,None]
        for idx, player in enumerate(self.game.players):
            if player.role == 'Merlin':
                merlin_index = idx
        print(self.game.players[merlin_index].role)
        monkeypatch.setattr('builtins.input', lambda _: merlin_index - 1)
        self.game.choose_success_failure(1)
        self.game.choose_success_failure(1)
        self.game.choose_success_failure(1)
        self.game.choose_success_failure(1)
        assert self.game.quest_count[0] == 3
        assert self.game.quest_count[1] == 0
        assert self.game.winner == 'Good'  