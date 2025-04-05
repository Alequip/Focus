# Focus API Documentation

## Services

### UserService

#### Methods

##### `create_user(username, password, role='student')`
Creates a new user in the system.
- **Parameters:**
  - `username` (str): The username for the new user
  - `password` (str): The password for the new user
  - `role` (str, optional): The role for the user. Defaults to 'student'
- **Returns:** User object

##### `get_user_by_id(user_id)`
Retrieves a user by their ID.
- **Parameters:**
  - `user_id` (int): The ID of the user to retrieve
- **Returns:** User object or None

##### `get_user_by_username(username)`
Retrieves a user by their username.
- **Parameters:**
  - `username` (str): The username to search for
- **Returns:** User object or None

### GameService

#### Methods

##### `create_game(title, description, age_group)`
Creates a new game.
- **Parameters:**
  - `title` (str): The title of the game
  - `description` (str): A description of the game
  - `age_group` (str): The target age group for the game
- **Returns:** Game object

##### `get_game_by_id(game_id)`
Retrieves a game by its ID.
- **Parameters:**
  - `game_id` (int): The ID of the game to retrieve
- **Returns:** Game object or None

##### `get_games_by_age_group(age_group)`
Retrieves all games for a specific age group.
- **Parameters:**
  - `age_group` (str): The age group to filter by
- **Returns:** List of Game objects

### StatsService

#### Methods

##### `record_game_play(user_id, game_id, score=None, duration=None)`
Records a game session.
- **Parameters:**
  - `user_id` (int): The ID of the user who played
  - `game_id` (int): The ID of the game that was played
  - `score` (int, optional): The score achieved
  - `duration` (int, optional): The duration of play in seconds
- **Returns:** GamePlay object

##### `get_user_stats(user_id)`
Gets statistics for a specific user.
- **Parameters:**
  - `user_id` (int): The ID of the user
- **Returns:** Dictionary containing:
  - `total_games_played` (int)
  - `favorite_game` (str)
  - `best_scores` (dict)
  - `total_time_played` (int)

##### `get_game_stats(game_id)`
Gets statistics for a specific game.
- **Parameters:**
  - `game_id` (int): The ID of the game
- **Returns:** Dictionary containing:
  - `times_played` (int)
  - `average_score` (float)
  - `average_duration` (float)
  - `top_players` (list)
