const display = document.getElementById("display");

function appendValue(value){
    display.value += value;
}

function clearDisplay(){
    display.value = "";
}

function calculate(){
    try{
        display.value = eval(display.value);
    }
    catch{
        display.value = "Error";
    }
}

function scientific(type){

    let value = parseFloat(display.value);

    switch(type){

        case "sin":
            display.value = Math.sin(value);
            break;

        case "cos":
            display.value = Math.cos(value);
            break;

        case "tan":
            display.value = Math.tan(value);
            break;

        case "log":
            display.value = Math.log10(value);
            break;

        case "ln":
            display.value = Math.log(value);
            break;

        case "sqrt":
            display.value = Math.sqrt(value);
            break;
    }
}

function insertConstant(type){

    if(type==="PI")
        display.value += Math.PI;

    if(type==="E")
        display.value += Math.E;
}

function calculateStats(){

    let data =
    document.getElementById("statsInput")
    .value
    .split(",")
    .map(Number);

    let mean =
    data.reduce((a,b)=>a+b,0)/data.length;

    let variance =
    data.reduce((a,b)=>a+(b-mean)**2,0)
    /data.length;

    let std =
    Math.sqrt(variance);

    document.getElementById("statsResult")
    .innerHTML =
    `
    Mean: ${mean}<br>
    Variance: ${variance}<br>
    Std Dev: ${std}
    `;
}

function parseMatrix(text){

    return text.trim()
    .split("\n")
    .map(row =>
    row.split(",").map(Number));
}

function matrixAdd(){

    let A = parseMatrix(
    document.getElementById("matrixA").value);

    let B = parseMatrix(
    document.getElementById("matrixB").value);

    let result =
    A.map((row,i)=>
    row.map((v,j)=>v+B[i][j]));

    document.getElementById("matrixResult")
    .innerText =
    JSON.stringify(result);
}

function matrixSubtract(){

    let A = parseMatrix(
    document.getElementById("matrixA").value);

    let B = parseMatrix(
    document.getElementById("matrixB").value);

    let result =
    A.map((row,i)=>
    row.map((v,j)=>v-B[i][j]));

    document.getElementById("matrixResult")
    .innerText =
    JSON.stringify(result);
}

function matrixMultiply(){

    let A = parseMatrix(
    document.getElementById("matrixA").value);

    let B = parseMatrix(
    document.getElementById("matrixB").value);

    let result = [];

    for(let i=0;i<A.length;i++){

        result[i]=[];

        for(let j=0;j<B[0].length;j++){

            let sum=0;

            for(let k=0;k<B.length;k++){

                sum+=A[i][k]*B[k][j];
            }

            result[i][j]=sum;
        }
    }

    document.getElementById("matrixResult")
    .innerText =
    JSON.stringify(result);
}