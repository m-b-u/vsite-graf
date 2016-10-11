function getFrameBufferFromCanvas(id) {
    var canvas = document.getElementById(id);
    var ctx = canvas.getContext("2d");
    return ctx.getImageData(0, 0, canvas.width, canvas.height);
}

function getFrameBufferFromCanvas_ex(canvas) {
    var ctx = canvas.getContext("2d");
    return ctx.getImageData(0, 0, canvas.width, canvas.height);
}


function putFrameBufferToCanvas(id, data) {
    var canvas = document.getElementById(id);
    var ctx = canvas.getContext("2d");
    ctx.putImageData(data, 0, 0);
}

function putCanvasToCanvas_ex(canvas, canvasData) {
    var ctx = canvas.getContext("2d");
    // ctx.putImageData(data, 0, 0, 0, 0, canvas.width, canvas.height);
    var ctx2 = canvasData.getContext("2d");
    ctx.drawImage(ctx2, 0, 0, canvas.width, canvas.height);
}


function clearFrameBuffer(fb) {
    for (var i=0; i<fb.data.length; ) {
	fb.data[i++]=0;
	fb.data[i++]=0;
	fb.data[i++]=0;
	fb.data[i++]=255;
    }
}

function putPixel(fb, x, y, value)
{
    i = (fb.width * y + x) * 4;
    fb.data[i++] = value[0];
    fb.data[i++] = value[1];
    fb.data[i++] = value[2];
    fb.data[i++] = value[3];
}

function gray(val) {
    return [val, val, val, 255];
}

function getRandomInt(val) {
    return Math.floor(Math.random()*val);
}

function createImageData(width, height) {
    var canvas = document.createElement('canvas');
    canvas.width = width;
    canvas.height = height;
    return canvas;
}

function startExercise1b_canvas() {
    var imgData;
    
    var canvas = document.getElementById("fb1");
    var context = canvas.getContext("2d");
    var canvasSmall = createImageData(canvas.width/20, canvas.height/20);
    imgData = getFrameBufferFromCanvas_ex(canvasSmall);
    clearFrameBuffer(imgData);
    putPixel(imgData, 5, 3, [255, 0, 0, 255]);
    putPixel(imgData, 8, 7, [0, 255, 0, 255]);
    var contextSmall = canvasSmall.getContext("2d");
    contextSmall.putImageData(imgData, 0, 0);

    var image = new Image();
    image.onload = function() {
	context.clearRect(0, 0, canvas.width, canvas.height);
	context.scale(20,20);
	context.imageSmoothingEnabled = false;
	context.drawImage(image, 0, 0);
    }
    image.src = canvasSmall.toDataURL();
    
    imgData = getFrameBufferFromCanvas("fb3");
    clearFrameBuffer(imgData);
    for (var i=0; i<100; i++) {
	putPixel(imgData, getRandomInt(imgData.width), getRandomInt(imgData.height), gray(getRandomInt(255)));
    }
    
    putFrameBufferToCanvas("fb3", imgData);
}




// https://stackoverflow.com/questions/19129644/how-to-pixelate-an-image-with-canvas-and-javascript
