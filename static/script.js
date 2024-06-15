function processarUrls() {
    console.log("Processar URLs iniciado");
    
    var urls = document.getElementById("txtUrls").value.split("\n");
    var keyword = document.getElementById("txtPalavraChave").value;
    
    console.log("URLs:", urls);
    console.log("Palavra-chave:", keyword);

    fetch('/processar', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ urls: urls, keyword: keyword }),
    })
    .then(response => response.json())
    .then(data => {
        console.log("Resposta recebida:", data);
        exibirResultados(data);
    })
    .catch((error) => {
        console.error('Erro:', error);
        alert('Erro ao processar as URLs.');
    });
}

function exibirResultados(resultados) {
    var divResultados = document.getElementById("divResultados");
    divResultados.innerHTML = "";

    if (resultados.length > 0) {
        var html = "<h2>Resultados da Busca:</h2>";
        resultados.forEach(function (resultado) {
            html += `<div><strong>URL:</strong> ${resultado.url}<br><strong>Texto Limpo:</strong><br>${resultado.texto_limpo}</div><hr>`;
        });
        divResultados.innerHTML = html;
    } else {
        divResultados.innerHTML = "<p>Nenhum resultado encontrado.</p>";
    }
}
