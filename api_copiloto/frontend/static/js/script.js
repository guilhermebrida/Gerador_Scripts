
function obterClientes(hardware) {
    if (hardware.checked) {
        var xhr = new XMLHttpRequest();
        if (hardware.value == 1) {
            url = 'https://api.github.com/repos/CreareSistemas/iot-virtec-scripts/contents/Virtec/Virloc8/Cliente';
        } else if (hardware.value == 2) {
            url = 'https://api.github.com/repos/CreareSistemas/iot-virtec-scripts/contents/Virtec/Vircom5/Cliente';
        } else if (hardware.value == 3) {
            url = 'https://api.github.com/repos/CreareSistemas/iot-virtec-scripts/contents/Virtec/Vircom5/Cliente';
        } else if (hardware.value == 4) {
            url = 'https://api.github.com/repos/CreareSistemas/iot-virtec-scripts/contents/Virtec/Virloc10/Cliente';
        } else if (hardware.value == 5) {
            url = 'https://api.github.com/repos/CreareSistemas/iot-virtec-scripts/contents/Virtec/Virloc12/Cliente';
        }
        xhr.open('GET', url);
        xhr.setRequestHeader('Authorization', 'Bearer ' + window.TOKEN_GITHUB);
        xhr.onreadystatechange = function () {
            if (xhr.readyState === XMLHttpRequest.DONE) {
                if (xhr.status === 200) {
                    var response = JSON.parse(xhr.responseText);
                    var nomes = response.map(function (item) {
                        return item.name;
                    });
                    console.log(nomes);
                    exibirClientes(nomes)
                } else {
                    console.log('Erro na solicitação: ' + xhr.status);
                }
            }
        };
        xhr.send();

    }
}
var campoCliente = document.getElementById('campo-cliente');

function exibirClientes(clientes) {
    var dropdownOptions = document.getElementById('clientes-dropdown');
    dropdownOptions.innerHTML = '';

    var columnDiv = document.createElement('div');
    columnDiv.classList.add('column');

    var ulElement = document.createElement('ul');

    for (var i = 0; i < clientes.length; i++) {
        var cliente = clientes[i];
        var liElement = document.createElement('li');
        var aElement = document.createElement('a');
        aElement.href = '#';
        aElement.textContent = cliente;

        aElement.addEventListener('click', function (e) {
            campoCliente.value = e.target.textContent;
        });

        liElement.appendChild(aElement);
        ulElement.appendChild(liElement);

        // Adicionar uma nova lista a cada 5 clientes
        if ((i + 1) % 5 === 0) {
            columnDiv.appendChild(ulElement);
            ulElement = document.createElement('ul');
        }
    }
    if (ulElement.childNodes.length > 0) {
        columnDiv.appendChild(ulElement);
    }
    dropdownOptions.appendChild(columnDiv);
    console.log('Dropdown atualizado:', dropdownOptions.innerHTML);
}