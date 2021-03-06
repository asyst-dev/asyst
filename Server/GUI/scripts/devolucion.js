document.addEventListener('DOMContentLoaded', e => { fetchData() }); //cuando se carga la pag. se lee el JSON
const templateCard = document.getElementById('bloque-lista').content //Traigo el Template de los items de lista busqueda
const panel = document.getElementById('panel-busqueda') // Declaro el "padre", es decir el panel busqueda que busca los items
const fragment = document.createDocumentFragment() // Declaro el fragment, que uso para evitar el Reflow
const boton = document.getElementById('Devolbutton')
const observacion = document.querySelector('textarea.is-success')
// const data = document.getElementById('pedido-db').value
let data = []

const fetchData = async () => {
    // const res = await fetch('scripts/ejemploBase.json');
    // data = await res.json()
    data = JSON.parse(document.getElementById('pedido-db').value)
    console.log(data)
    pintarCards(data)
}

const pintarCards = data => {
    panel.innerHTML = ""
    data.forEach(item => {
        // item.cantidad = 11 //borrar despues, solo de prueba
        templateCard.querySelector('.nombre-herr').textContent = item.nombre
        // templateCard.querySelector('a.panel-block').dataset.id = item.id
        templateCard.querySelector('i').classList.remove('fa-toolbox'); 
        templateCard.querySelector('i').classList.remove('fa-tools'); 
        templateCard.querySelector('i').classList.remove('fa-question-circle'); 
        templateCard.querySelector('.itemnum').value = item.cantidad
        if      (item.clase == 1){templateCard.querySelector('i').classList.add('fa-toolbox');         }
        else if (item.clase == 2){templateCard.querySelector('i').classList.add('fa-tools');           }  
        else {                    templateCard.querySelector('i').classList.add('fa-question-circle'); }
        // if(item.selected){templateCard.querySelector('a.panel-block').classList.add('tool-selected')}
        // else{templateCard.querySelector('a.panel-block').classList.remove('tool-selected')}

        const clone = templateCard.cloneNode(true)
        fragment.appendChild(clone)
    })
    panel.appendChild(fragment)}

// boton.addEventListener('click',()=>{
//     // console.log(observacion)
//     const texto = observacion.value
//     console.log(texto)
//     data.push(texto)
//     console.log(data)    
    
//     const csrftoken = getCookie('csrftoken');
//     console.log(csrftoken)
//     var http = new XMLHttpRequest();
//     var url = "/user/devolver/";
//     http.open("POST", url, true);
//     http.setRequestHeader('X-CSRFToken', csrftoken);

//     http.onreadystatechange = function() {
//         if(http.readyState == 4 && http.status == 200) { 
//         //aqui obtienes la respuesta de tu peticion
//         alert(texto);
//         }
//     }
//     http.send(JSON.stringify(texto));
// })
boton.addEventListener('click',()=>{document.getElementById('msgform').submit()})

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
