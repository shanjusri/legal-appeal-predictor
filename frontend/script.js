document.getElementById("predictBtn").addEventListener("click", function () {

const caseText = document.getElementById("caseText").value.trim();

if(caseText === ""){
document.getElementById("label").innerText = "Please enter case description";
return;
}

/* Fake prediction logic for demo */

let label;
let category;
let duration;
let confidence;

if(caseText.length % 2 === 0){
label = "Accepted";
category = "Civil Case";
duration = "1 - 2 Years";
confidence = "87%";
}
else{
label = "Rejected";
category = "Criminal Case";
duration = "6 Months";
confidence = "78%";
}

document.getElementById("label").innerText = label;
document.getElementById("category").innerText = category;
document.getElementById("duration").innerText = duration;
document.getElementById("confidence").innerText = confidence;

});
