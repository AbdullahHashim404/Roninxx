let board = [
    [null, null, null],
    [null, null, null],
    [null, null, null]
];
let currentPlayer = 'X';  // X always starts
let gameOver = false;

const squares = document.querySelectorAll('.square');
const statusBar = document.getElementById('status-bar');

function restartGame() {
    board = [
        [null, null, null],
        [null, null, null],
        [null, null, null]
    ];
    currentPlayer = 'X';
    gameOver = false;
    statusBar.textContent = "Player 1's Turn (X)";
    squares.forEach(square => {
        square.textContent = '';
        square.classList.remove('X', 'O');
        square.style.pointerEvents = 'auto';
    });
}

function checkWin() {
    for (let i = 0; i < 3; i++) {
        // Check rows and columns
        if (board[i][0] === currentPlayer && board[i][1] === currentPlayer && board[i][2] === currentPlayer) {
            return true;
        }
        if (board[0][i] === currentPlayer && board[1][i] === currentPlayer && board[2][i] === currentPlayer) {
            return true;
        }
    }
    // Check diagonals
    if (board[0][0] === currentPlayer && board[1][1] === currentPlayer && board[2][2] === currentPlayer) {
        return true;
    }
    if (board[0][2] === currentPlayer && board[1][1] === currentPlayer && board[2][0] === currentPlayer) {
        return true;
    }
    return false;
}

function handleMove(e) {
    const row = e.target.dataset.row;
    const col = e.target.dataset.col;

    if (board[row][col] !== null || gameOver) return;

    board[row][col] = currentPlayer;
    e.target.textContent = currentPlayer;
    e.target.classList.add(currentPlayer);

    if (checkWin()) {
        gameOver = true;
        statusBar.textContent = `${currentPlayer} Wins!`;
        squares.forEach(square => {
            square.style.pointerEvents = 'none'; // Disable further moves
        });
    } else if (board.flat().every(cell => cell !== null)) {
        gameOver = true;
        statusBar.textContent = "It's a Draw!";
    } else {
        currentPlayer = currentPlayer === 'X' ? 'O' : 'X';
        statusBar.textContent = currentPlayer === 'X' ? "Player 1's Turn (X)" : "Player 2's Turn (O)";
    }
}

squares.forEach(square => {
    square.addEventListener('click', handleMove);
});
