import pytest
from app.services.user_service import UserService

def test_user_registration(client, db):
    """Test user registration."""
    response = client.post('/auth/register', data={
        'username': 'testuser',
        'password': 'testpass'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b'Login' in response.data
    
    user = UserService.get_user_by_username('testuser')
    assert user is not None
    assert user.role == 'student'

def test_user_login(client, db):
    """Test user login."""
    # Create a test user
    UserService.create_user('testuser', 'testpass', 'student')
    
    # Try to login
    response = client.post('/auth/login', data={
        'username': 'testuser',
        'password': 'testpass'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b'Games Selection' in response.data

def test_user_logout(client, db):
    """Test user logout."""
    # Create and login a test user
    UserService.create_user('testuser', 'testpass', 'student')
    client.post('/auth/login', data={
        'username': 'testuser',
        'password': 'testpass'
    })
    
    # Try to logout
    response = client.get('/auth/logout', follow_redirects=True)
    assert response.status_code == 200
    assert b'Login' in response.data
