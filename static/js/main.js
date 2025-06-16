document.addEventListener('DOMContentLoaded', function() {
            const cards = document.querySelectorAll('.card-hover');
            
            cards.forEach(card => {
                card.addEventListener('mouseenter', function() {
                    this.classList.add('scale-105');
                });
                
                card.addEventListener('mouseleave', function() {
                    this.classList.remove('scale-105');
                });
                
                card.addEventListener('click', function() {
                    // Aggiunge effetto di click
                    this.classList.add('scale-95');
                    setTimeout(() => {
                        this.classList.remove('scale-95');
                    }, 150);
                });
            });
        });