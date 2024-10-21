document.getElementById('preferences-form').addEventListener('submit', function(event) {
    event.preventDefault();

    const disabilityType = document.getElementById('disability-type').value;
    const destination = document.getElementById('destination').value;
    const travelDates = document.getElementById('travel-dates').value;

    // Simulação de geração de roteiro
    let itinerary = `Roteiro para ${destination} com acessibilidade para ${disabilityType}.<br>
                    Inclui transporte acessível e recomendações de locais acessíveis.`;

    // Exibir o roteiro
    document.getElementById('itinerary-content').innerHTML = itinerary;
    document.getElementById('itinerary').classList.remove('hidden');
});
