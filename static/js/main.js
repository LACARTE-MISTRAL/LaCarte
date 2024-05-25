document.addEventListener('DOMContentLoaded', event => {

    const initialDisplay = document.getElementById('initial');
    const flashCardsDisplay = document.getElementById('flash-cards');
    const form = document.getElementById('generate-button');
    const cardFront = document.getElementById('card-front-text');
    const cardBack = document.getElementById('card-back-text');

    
    form.addEventListener('submit', event =>
    {
        event.preventDefault();
        console.log("Event started");
        initialDisplay.style.display = 'none';
        flashCardsDisplay.style.display = 'block';

        fetch (form.action, {
            method: form.method,
            body: new FormData(form)
        }).then(response => response.json())
        .then(data => {
            console.log(data);
            cardFront.innerHTML = data[0].front;
            cardBack.innerHTML = data[0].back;
            darcBack.style.display = 'none';

            
        });
    });
});