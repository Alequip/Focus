import pytest
from app.services.game_service import GameService
from app.services.user_service import UserService

def test_games_list(client, db):
    """Test games list view."""
    # Create and login a test user
    UserService.create_user('testuser', 'testpass', 'student')
    client.post('/auth/login', data={
        'username': 'testuser',
        'password': 'testpass'
    })
    
    # Create a test game
    GameService.create_game(
        title='Test Game',
        description='A test game',
        age_group='7-8'
    )
    
    # Try to access games list
    response = client.get('/games/7-8')
    assert response.status_code == 200
    assert b'Test Game' in response.data

def test_game_creation(client, db):
    """Test game creation."""
    # Create and login an admin user
    UserService.create_user('admin', 'adminpass', 'admin')
    client.post('/auth/login', data={
        'username': 'admin',
        'password': 'adminpass'
    })
    
    # Try to create a game
    response = client.post('/admin/add_game', data={
        'title': 'New Game',
        'description': 'A new test game',
        'age_group': '9-10'
    }, follow_redirects=True)
    assert response.status_code == 200
    
    game = GameService.get_games_by_age_group('9-10')[0]
    assert game.title == 'New Game'
    assert game.description == 'A new test game'
