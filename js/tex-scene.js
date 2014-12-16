var scene = function () {};

// General workflow with attributes.
// 1. Enable attribute arrays after the program is linked
// 2. Create buffers, bind them to fill data
// 3. Bind buffers, set vertexAttribPointers before the draw.
// Seems that buffer bound at the draw time is irrelevant, it should be picked up (by implicit VAO?) at the time of setting the pointer

function initShaders() {

    var fragmentShader = getShader("shader-frag", gl.FRAGMENT_SHADER);
    var vertexShader =   getShader("shader-vert", gl.VERTEX_SHADER);

    scene.shader = {};

    var program = gl.createProgram();
    scene.shader['default'] = program;
    gl.attachShader(program, vertexShader);
    gl.attachShader(program, fragmentShader);

    gl.linkProgram(program);

    program.vertexPositionAttribute = gl.getAttribLocation(program, "aVertPosition");

    program.texturePositionAttribute = gl.getAttribLocation(program, "aTexPosition");

    program.transformUniform = gl.getUniformLocation(program, "uTransform");
    program.samplerUniform = gl.getUniformLocation(program, "sampler");

    // it's the only one for now so we can use it immediately
    gl.useProgram(program);
    gl.enableVertexAttribArray(program.vertexPositionAttribute);
    gl.enableVertexAttribArray(program.texturePositionAttribute);
}


var gridSize = 20;
function loadScene()
{

    scene.element = {};
    scene.buffer = {};
    scene.texture = {};
    scene.frame = 0;
    var identity = [1., 0., 0., 0., 1., 0., 0., 0., 1.];
    gl.uniformMatrix3fv(scene.shader['default'].transformUniform, false, identity);


    scene.texture['default'] = ImageTexture('../samples/helix_blancoHubble_1080.jpg');
//    scene.texture['default'] = ImageTexture('../samples/grid-checker-fabric-texture-13-512x512.jpg');



    makeMinimalScene();

    setViewportSize();
}


function makeMinimalScene() 
{

    var coordBuffer = gl.createBuffer();
    gl.bindBuffer(gl.ARRAY_BUFFER, coordBuffer);
    gl.bufferData(gl.ARRAY_BUFFER, new Float32Array([
	-0.8,  -0.8,
	0.8,  -0.8,
	-0.8,  0.8,
	-0.8,  0.8,
	0.8,  -0.8,
	0.8,  0.8]), gl.STATIC_DRAW);

    scene.buffer['vCoord0'] = coordBuffer;

    var texCoordBuffer = gl.createBuffer();
    gl.bindBuffer(gl.ARRAY_BUFFER, texCoordBuffer);
    gl.bufferData(gl.ARRAY_BUFFER, new Float32Array([
	0.0,  0.0,
	1.0,  0.0,
	0.0,  1.0,
	0.0,  1.0,
	1.0,  0.0,
	1.0,  1.0]), gl.STATIC_DRAW);
    
    scene.buffer['tCoord0'] = texCoordBuffer;

    gl.bindBuffer(gl.ARRAY_BUFFER, null);
}


function drawScene()
{
    gl.viewport(0, 0, gl.drawingBufferWidth, gl.drawingBufferHeight);
    gl.clear(gl.COLOR_BUFFER_BIT|gl.DEPTH_BUFFER_BIT);

    gl.activeTexture(gl.TEXTURE0);
    gl.bindTexture(gl.TEXTURE_2D, scene.texture['default']);
    gl.uniform1i(scene.shader['default'].samplerUniform, 0);

    var vCoordLocation = gl.getAttribLocation(scene.shader['default'], "aVertPosition");
        gl.bindBuffer(gl.ARRAY_BUFFER, scene.buffer['vCoord0']);
    gl.vertexAttribPointer(vCoordLocation, 2, gl.FLOAT, false, 0, 0); 
    
    var tCoordLocation = gl.getAttribLocation(scene.shader['default'], "aTexPosition");
    gl.bindBuffer(gl.ARRAY_BUFFER, scene.buffer['tCoord0']);
    gl.vertexAttribPointer(tCoordLocation, 2, gl.FLOAT, false, 0, 0);    

    gl.drawArrays(gl.TRIANGLES, 0, 6);

    gl.flush();
}



function doResize() {
    if (gl !== undefined) {
	setViewportSize();
	drawScene();
    }
}

function setViewportSize() {
    var canvas = document.getElementById("canvas1");
    console.log("Setting viewport");
    console.log("Resize canvas size: " + canvas.width + ", " + canvas.height + " clientsize: " + canvas.clientWidth + ", " + canvas.clientHeight);
    var w = canvas.clientWidth;
    var h = canvas.clientHeight;
    if (canvas.width != w)
	canvas.width = w;
    if (canvas.height != h)
	canvas.height = h;

    console.log("Resize buffer size: " + gl.drawingBufferWidth + ", " + gl.drawingBufferHeight);
}

function doKeyPress(event) {

    var chCode = ('charCode' in event) ? event.charCode : event.keyCode;
    console.log("Key pressed: " + chCode);
    var triggered = false;
    if (chCode =='q'.charCodeAt(0)) {
	stopAnimation();
    } else if (chCode =='x'.charCodeAt(0)) {
	triggered = true;
    }

    if (triggered) {
	console.log("Key triggered");
    }
    if (triggered && !scene.timer) {
	startAnimation();
    }
}


function updateScene() {
    scene.frame++;
    // return scene.update()
    return true; 
}


function animate() {
    if (! scene.texture['default'].ready) {
	console.log("Poll for texture...");
	if (scene.texture['default'].error !== undefined) {
	    stopAnimation();
	}
	return;
    }
    if (! (scene.frame % 30)) {
	console.log("Frame: " + scene.frame);
    }
    var cont = updateScene();
    drawScene();
    if (!cont) {
	stopAnimation();
    }
}

function stopAnimation() {
    clearInterval(scene.timer);
    scene.timer = null;
    console.log("Animation stopped");
}


function startAnimation() {
    scene.timer = setInterval(animate, 20);
    console.log("Animation started");
}
