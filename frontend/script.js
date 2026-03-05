document.getElementById("predictBtn").addEventListener("click", async function () {

    const caseText = document.getElementById("caseText").value.trim();

    if(caseText === ""){
        alert("Please enter case description");
        return;
    }

    try{

        const response = await fetch("/predict",{
            method:"POST",
            headers:{
                "Content-Type":"application/json"
            },
            body: JSON.stringify({
                text: caseText
            })
        });

        const data = await response.json();

        document.getElementById("label").innerText = data.label;
        document.getElementById("category").innerText = data.category;
        document.getElementById("duration").innerText = data.duration;
        document.getElementById("confidence").innerText = data.confidence;

        document.getElementById("resultCard").style.display="block";

    }
    catch(error){
        console.error(error);
        alert("Prediction failed");
    }

});
