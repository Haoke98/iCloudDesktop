window.addEventListener('pywebviewready', function () {
    var container = document.getElementById('pywebview-status')
    container.innerHTML = '<i>pywebview</i> is ready'
})

function showResponse(response) {
    var container = document.getElementById('response-container')

    container.innerText = response.message
    container.style.display = 'block'
}

function initialize() {
    pywebview.api.init().then(showResponse)
}

function login() {
    username
}

function doHeavyStuff() {
    var btn = document.getElementById('heavy-stuff-btn')

    pywebview.api.heavy_stuff.doHeavyStuff().then(function (response) {
        showResponse(response)
        btn.onclick = doHeavyStuff
        btn.innerText = 'Perform a heavy operation'
    })

    showResponse({message: 'Working...'})
    btn.innerText = 'Cancel the heavy operation'
    btn.onclick = cancelHeavyStuff
}

function cancelHeavyStuff() {
    pywebview.api.heavy_stuff.cancelHeavyStuff()
}

function getRandomNumber() {
    pywebview.api.getRandomNumber().then(showResponse)
}

function greet() {
    var name_input = document.getElementById('name_input').value;
    pywebview.api.sayHelloTo(name_input).then(showResponse)
}

function catchException() {
    pywebview.api.error().catch(showResponse)
}