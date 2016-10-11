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

function writeRGBA(fb, offset, value)
{
    i = offset*4;
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

function getDrawImageFunc(canvas, image, scalex, scaley) {
    return function () {
	context = canvas.getContext("2d");
	context.clearRect(0, 0, canvas.width, canvas.height);
	context.scale(scalex, scaley);
	context.imageSmoothingEnabled = false;
	context.mozImageSmoothingEnabled = false;
	context.webkitImageSmoothingEnabled = false;
	context.drawImage(image, 0, 0);
    }
}

function startExercise1b_canvas() {
    var imgData;
    // Create small offscreen canvas
    var canvas = document.getElementById("fb1");
    var context = canvas.getContext("2d");
    var scalex = 20, scaley = 20;
    var canvasSmall = createImageData(canvas.width/scalex, canvas.height/scaley);

    // Get this data as byte array
    imgData = getFrameBufferFromCanvas_ex(canvasSmall);

    // "Draw" something
    clearFrameBuffer(imgData);
    writeRGBA(imgData, 95, [255, 0, 0, 255]);
    writeRGBA(imgData, 218, [0, 255, 0, 255]);
    var contextSmall = canvasSmall.getContext("2d");
    contextSmall.putImageData(imgData, 0, 0);

    // Write from small canvas to Image,
    // Then draw this image upscaled to large canvas
    var image = new Image();
    image.onload = getDrawImageFunc(canvas, image, scalex, scaley);
    image.src = canvasSmall.toDataURL();
    
    // Create new offscreen canvas (size w*h x 1)
    canvasSmall = createImageData(canvasSmall.width*canvasSmall.height, 1);
    contextSmall = canvasSmall.getContext("2d");
    // Again create image data
    imgData = getFrameBufferFromCanvas_ex(canvasSmall);
    // "Draw" same thing
    clearFrameBuffer(imgData);
    writeRGBA(imgData, 95, [255, 0, 0, 255]);
    writeRGBA(imgData, 218, [0, 255, 0, 255]);

    contextSmall.putImageData(imgData, 0, 0);
    canvas = document.getElementById("fb2");
    context = canvas.getContext("2d");

    // Again, small canvas to Image, then image to on screen canvas
    image = new Image();
    image.onload = getDrawImageFunc(canvas, image, 1, canvas.height);
    image.src = canvasSmall.toDataURL();  

    
    // Draw random dots
    imgData = getFrameBufferFromCanvas("fb3");
    clearFrameBuffer(imgData);
    for (var i=0; i<100; i++) {
	putPixel(imgData, getRandomInt(imgData.width), getRandomInt(imgData.height), gray(getRandomInt(255)));
    }
    putFrameBufferToCanvas("fb3", imgData);

    // Now draw directly using some high level API
    var canvas = document.getElementById("fb3");
    var context = canvas.getContext("2d");
    var startx = 10.5, starty = 20.5;
    var endx = 500.5, endy = 280.5;
    
    for (var i=0; i<100; i++) {
	context.beginPath();
	context.strokeStyle = "rgb(" + (i+10) + ", " + (i+30) + ", " + (i+50) + ")";
	context.moveTo(startx, starty);
	context.lineTo(endx, endy);
	context.stroke();
	startx += 5; starty += 5;
	endx -= 3; endy -= 2;
    }

}


