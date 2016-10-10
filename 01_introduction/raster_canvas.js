function getFrameBufferFromCanvas(id) {
    var canvas = document.getElementById(id);
    var ctx = canvas.getContext("2d");
    return ctx.getImageData(0, 0, canvas.width, canvas.height);
}

function putFrameBufferToCanvas(id, data) {
    var canvas = document.getElementById(id);
    var ctx = canvas.getContext("2d");
    ctx.putImageData(data, 0, 0);
}

function startExercise1b_canvas() {
    var imgData = getFrameBufferFromCanvas("fb");
    for (var i=1000; i<1200; i+=4) {
	imgData.data[i]=100;
	imgData.data[i+1]=150;
	imgData.data[i+2]=200;
	imgData.data[i+3]=255;
    }
    
    putFrameBufferToCanvas("fb", imgData);
    putFrameBufferToCanvas("fb2", imgData);
}

