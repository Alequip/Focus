const colors = {
    '#FF0000': 'rojo',
    '#0000FF': 'azul',
    '#FFFF00': 'amarillo',
    '#008000': 'verde',
    '#FFA500': 'naranja',
    '#800080': 'morado'
};

const hexColors = Object.keys(colors);
let score = 0;
let level = 1;
let timeLeft = 0;
let timerInterval;
const scoreElement = document.getElementById('score');
const levelElement = document.getElementById('level');
const timerElement = document.getElementById('timer');
const timerBar = document.getElementById('timer-bar');
const colorDisplay = document.getElementById('color-display');
const colorOptions = document.getElementById('color-options');
const resultDisplay = document.getElementById('result');
const popupContainer = document.getElementById('popup-container');
const popupMessage = document.getElementById('popup-message');
const restartButton = document.getElementById('restart-button');
const menuButton = document.getElementById('menu-button'); // Agregado

function startGame() {
    generateColor();
    generateOptions();
    updateTimer();
}

function generateColor() {
    const randomHexColor = hexColors[Math.floor(Math.random() * hexColors.length)];
    colorDisplay.style.backgroundColor = randomHexColor;
    colorDisplay.dataset.color = randomHexColor;
}

function generateOptions() {
    colorOptions.innerHTML = '';
    const correctHexColor = colorDisplay.dataset.color;
    let options = shuffleArray(hexColors.filter(color => color !== correctHexColor)).slice(0, 3);
    options.push(correctHexColor);
    options = shuffleArray(options);

    for (let i = 0; i < options.length; i++) {
        const hexColor = options[i];
        const colorName = colors[hexColor];
        const option = document.createElement('button');
        option.textContent = colorName;
        option.addEventListener('click', checkAnswer);
        colorOptions.appendChild(option);
    }
}

function checkAnswer(event) {
    const selectedColorName = event.target.textContent;
    const correctHexColor = colorDisplay.dataset.color;
    const correctColorName = colors[correctHexColor];
    if (selectedColorName === correctColorName) {
        score++;
        scoreElement.textContent = `Puntos: ${score}`;
        if (score % 5 === 0) {
            level++;
            levelElement.textContent = `Nivel: ${level}`;
            if (level > 5) {
                endGame('¡Has ganado!');
                return;
            }
            updateTimer();
        }
    } else {
        endGame('¡Tiempo agotado o respuesta incorrecta!');
        return;
    }
    generateColor();
    generateOptions();
}

function shuffleArray(array) {
    for (let i = array.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [array[i], array[j]] = [array[j], array[i]];
    }
    return array;
}

function updateTimer() {
    console.log("updateTimer llamado, nivel:", level);
    clearInterval(timerInterval);
    if (level === 1) {
        timeLeft = 0;
        if (timerBar) {
            timerBar.style.width = '100%';
        }
        console.log("Nivel 1, temporizador desactivado");
        return;
    }

    switch (level) {
        case 2:
            timeLeft = 40;
            break;
        case 3:
            timeLeft = 35;
            break;
        case 4:
            timeLeft = 30;
            break;
        case 5:
            timeLeft = 25;
            break;
    }

    console.log("Tiempo restante:", timeLeft);
    if (timerBar) {
        timerBar.style.width = '100%';
        const widthPerSecond = 100 / timeLeft;
        let currentWidth = 100;
        timerInterval = setInterval(() => {
            currentWidth -= widthPerSecond;
            timerBar.style.width = `${currentWidth}%`;
            if (currentWidth <= 0) {
                endGame('¡Tiempo agotado!');
            }
        }, 1000);
    }
}

function endGame(message) {
    clearInterval(timerInterval);
    colorOptions.innerHTML = '';
    popupMessage.textContent = message;
    popupContainer.style.display = 'flex';
}

restartButton.addEventListener('click', () => {
    popupContainer.style.display = 'none';
    score = 0;
    level = 1;
    scoreElement.textContent = `Puntos: ${score}`;
    levelElement.textContent = `Nivel: ${level}`;
    startGame();
});

// Agregado
menuButton.addEventListener('click', () => {
    window.location.href = '/games/7-8'; // Redirige al menú de juegos
});

document.addEventListener('DOMContentLoaded', () => {
    startGame();
});