ddocument.getElementById("predictBtn").onclick = async function () {

let text = document.getElementById("caseText").value
let language = document.getElementById("language").value


let response = await fetch("http://127.0.0.1:8000/predict", {

method: "POST",

headers: {
"Content-Type": "application/json"
},

body: JSON.stringify({
text: text,
language: language
})

})

let data = await response.json()


document.getElementById("label").innerText = data.label
document.getElementById("category").innerText = data.category
document.getElementById("duration").innerText = data.duration
document.getElementById("confidence").innerText = data.confidence

}