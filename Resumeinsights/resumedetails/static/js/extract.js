// ats.html file js 

// Animate the ATS score on page load
document.addEventListener("DOMContentLoaded", function () {
    const scoreText = document.getElementById('score').textContent;
    const scoreNumber = parseInt(scoreText.match(/\d+/)[0], 10); // Extract the score number
    let currentScore = 0; // Initialize the current score
    const scoreElement = document.getElementById('score');

    const interval = setInterval(() => {
        if (currentScore < scoreNumber) {
            currentScore++;
            scoreElement.textContent = `ATS Compatibility Score: ${currentScore}/80`; // Update the displayed score
        } else {
            clearInterval(interval); // Stop the interval when the score reaches the target
        }
    }, 30); // Update the score every 30 milliseconds
});