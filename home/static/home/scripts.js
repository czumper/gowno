document.addEventListener('DOMContentLoaded', function() {
    const greetingElement = document.getElementById('Siemanko');
    const now = new Date();
    const hours = now.getHours();
    let greeting;

    if (hours < 12) {
        greeting = 'Dzień kurwa dobry!';
    } else if (hours < 18) {
        greeting = 'Dobry kurwa wieczór!';
    } else {
        greeting = 'No elo!';
    }

    greetingElement.textContent = greeting;

    // Example: Add a button click event
    const button = document.getElementById('exampleButton');
    button.addEventListener('click', function() {
        alert('Button clicked!');
    });
});