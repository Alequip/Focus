# Documentación de la API de Focus

## Servicios

### UserService (Servicio de Usuario)

#### Métodos

##### `create_user(username, password, role='student')`
Crea un nuevo usuario en el sistema.
- **Parámetros:**
  - `username` (str): El nombre de usuario para el nuevo usuario
  - `password` (str): La contraseña para el nuevo usuario
  - `role` (str, opcional): El rol del usuario. Por defecto es 'student'
- **Devuelve:** Objeto Usuario

##### `get_user_by_id(user_id)`
Obtiene un usuario por su ID.
- **Parámetros:**
  - `user_id` (int): El ID del usuario a obtener
- **Devuelve:** Objeto Usuario o None

##### `get_user_by_username(username)`
Obtiene un usuario por su nombre de usuario.
- **Parámetros:**
  - `username` (str): El nombre de usuario a buscar
- **Devuelve:** Objeto Usuario o None

### GameService (Servicio de Juegos)

#### Métodos

##### `create_game(title, description, age_group)`
Crea un nuevo juego.
- **Parámetros:**
  - `title` (str): El título del juego
  - `description` (str): Una descripción del juego
  - `age_group` (str): El grupo de edad al que va dirigido el juego
- **Devuelve:** Objeto Juego

##### `get_game_by_id(game_id)`
Obtiene un juego por su ID.
- **Parámetros:**
  - `game_id` (int): El ID del juego a obtener
- **Devuelve:** Objeto Juego o None

##### `get_games_by_age_group(age_group)`
Obtiene todos los juegos de un grupo de edad específico.
- **Parámetros:**
  - `age_group` (str): El grupo de edad por el cual filtrar
- **Devuelve:** Lista de objetos Juego

### StatsService (Servicio de Estadísticas)

#### Métodos

##### `record_game_play(user_id, game_id, score=None, duration=None)`
Registra una sesión de juego.
- **Parámetros:**
  - `user_id` (int): El ID del usuario que jugó
  - `game_id` (int): El ID del juego que se jugó
  - `score` (int, opcional): La puntuación obtenida
  - `duration` (int, opcional): La duración del juego en segundos
- **Devuelve:** Objeto GamePlay (Juego Jugado)

##### `get_user_stats(user_id)`
Obtiene estadísticas de un usuario específico.
- **Parámetros:**
  - `user_id` (int): El ID del usuario
- **Devuelve:** Diccionario que contiene:
  - `total_games_played` (int): Total de juegos jugados
  - `favorite_game` (str): Juego favorito
  - `best_scores` (dict): Mejores puntuaciones
  - `total_time_played` (int): Tiempo total jugado

##### `get_game_stats(game_id)`
Obtiene estadísticas de un juego específico.
- **Parámetros:**
  - `game_id` (int): El ID del juego
- **Devuelve:** Diccionario que contiene:
  - `times_played` (int): Veces jugado
  - `average_score` (float): Puntuación promedio
  - `average_duration` (float): Duración promedio
  - `top_players` (list): Mejores jugadores
