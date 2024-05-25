

document.addEventListener('DOMContentLoaded', event => {

    const initialDisplay = document.getElementById('initial');
    const flashCardsDisplay = document.getElementById('flash-cards');
    const submitTextForm = document.getElementById('submit-text');
    const cardContent = document.getElementById('card-content');
    const flashCardsForm = document.getElementById('flash-cards-form');
    let cards = [];


    submitTextForm.addEventListener('submit', event =>
    {
        event.preventDefault();
        console.log("Event started");
        initialDisplay.style.display = 'none';
        flashCardsDisplay.style.display = 'block';

        fetch (submitTextForm.action, {
            method: submitTextForm.method,
            body: new FormData(submitTextForm)
        }).then(response => response.json())
        .then(data => {
            
            let cardIndex = 0;
            let cards = data;
            let maxCardValue = cards.length;

            cardContent.innerHTML = data[cardIndex].front;
            
            flashCardsForm.addEventListener('click', event => {
    
                event.preventDefault();
                if (event.target.value == 'prev' && cardIndex > 0)
                {
                    cardIndex--;
                    cardContent.innerHTML = data[cardIndex].front;
                }
                else if (event.target.value == 'next' && cardIndex < maxCardValue - 1)        
                {
                    cardIndex++;
                    cardContent.innerHTML = data[cardIndex].front;
                }
                else if(event.target.value == 'flip')
                {
                    if (cardContent.innerHTML == data[cardIndex].front)
                    {
                        cardContent.innerHTML = data[cardIndex].back;
                    }
                    else
                    {
                        cardContent.innerHTML = data[cardIndex].front;
                    }
                }
                
            });
        });
    });
});