// scripts.js
let currentFlashcardIndex = 0;
const flashcards = document.querySelectorAll('.flashcard');

function flipCard(card) {
    card.classList.toggle('flipped');
}

function toggleLanguage() {
    const languageToggles = document.querySelectorAll('.language-toggle');
    languageToggles.forEach(toggle => {
        toggle.innerText = toggle.innerText === 'English' ? 'Hindi' : 'English';
    });

    const fronts = document.querySelectorAll('.front');
    const backs = document.querySelectorAll('.back');
    fronts.forEach(front => front.style.display = front.style.display === 'none' ? 'flex' : 'none');
    backs.forEach(back => back.style.display = back.style.display === 'flex' ? 'none' : 'flex');
}

function markCorrect() {
    // Move to the next flashcard
    if (currentFlashcardIndex < flashcards.length - 1) {
        currentFlashcardIndex++;
        showFlashcard(currentFlashcardIndex);
    }
}

function markIncorrect() {
    // Move to the next flashcard
    if (currentFlashcardIndex < flashcards.length - 1) {
        currentFlashcardIndex++;
        showFlashcard(currentFlashcardIndex);
    }
}

function showFlashcard(index) {
    // Hide all flashcards except the one at the given index
    flashcards.forEach((flashcard, i) => {
        if (i === index) {
            flashcard.style.display = 'block';
        } else {
            flashcard.style.display = 'none';
        }
    });
}

function shuffleFlashcards() {
    // Implement shuffling of flashcards
}
