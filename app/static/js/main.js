

document.addEventListener('DOMContentLoaded', event => {

    const initialDisplay = document.getElementById('initial');
    const flashCardsDisplay = document.getElementById('flash-cards');
    const submitTextForm = document.getElementById('submit-text');
    const cardContent = document.getElementById('card-content');
    const flashCardsForm = document.getElementById('flash-cards-form');
    const loadingContainer = document.getElementById('loading-container');
    let cards = [];

    submitTextForm.addEventListener('submit', event =>
    {
        event.preventDefault();

        initialDisplay.style.display = 'none';
        
        let loadingDiv = document.getElementById('loading');
        
        loadingDiv.textContent = 'Loading';

        let loadingDots = 0;
        let loadingInterval = setInterval(() => {
            loadingDiv.textContent = 'Loading' + '.'.repeat(loadingDots);
            loadingDots = (loadingDots + 1) % 4; 
        }, 500); 

        fetch (submitTextForm.action, {
            method: submitTextForm.method,
            body: new FormData(submitTextForm)
        }).then(response => response.json())
        .then(data => {
            
            clearInterval(loadingInterval);
            loadingDiv.textContent = '';
            loadingContainer.style.display = 'none';

            if (Object.keys(data).length === 0 && data.constructor === Object)
            {
                alert('We can\'t make flashcards with that input, please try again')
                location.reload();
                return;
            }


            flashCardsDisplay.style.display = 'flex';

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