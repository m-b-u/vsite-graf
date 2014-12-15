var scene = function () {};
var state = function () {};

state.G = {
    start: 0.2,
    end: 0.6,
    current: 0.2,
    blow: -10.0,
    blown: 0,
    state: 'none',
    charged: function() {
	return this.current > 0.85 * this.end;
    },
    update: function() {
	if (this.state == 'none') {
	    this.current += (this.start - this.current) * 0.02;
	} else if (this.state == 'charge') {
	    if (this.current < this.end) {
		this.current += (this.end - this.current) * 0.1;
	    }
	} else if (this.state == 'blow') {
	    this.current = this.blow;
	    this.state = 'none';
	}
	return this.current;
    }
};


// General workflow with attributes.
// 1. Enable attribute arrays after the program is linked
// 2. Create buffers, bind them to fill data
// 3. Bind buffers, set vertexAttribPointers before the draw.
// Seems that buffer bound at the draw time is irrelevant, it should be picked up (by implicit VAO?) at the time of setting the pointer

function initShaders() {

    var fragmentShader = getShader("shader-frag", gl.FRAGMENT_SHADER);
    var vertexShader =   getShader("shader-vert", gl.VERTEX_SHADER);
    var vertex3DShader = getShader("shader-vert-3d", gl.VERTEX_SHADER);

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
    program.cursorUniform = gl.getUniformLocation(program, "cursorCoord");

    // Second shader, with xyz coords
    var program3d = gl.createProgram();
    scene.shader['3d'] = program3d;
    gl.attachShader(program3d, vertex3DShader);
    gl.attachShader(program3d, fragmentShader);
    gl.linkProgram(program3d);

    program3d.vertexPositionAttribute = gl.getAttribLocation(program3d, "aVertPosition");
    program3d.texturePositionAttribute = gl.getAttribLocation(program3d, "aTexPosition");

    program3d.transformUniform = gl.getUniformLocation(program3d, "uTransform");
    program3d.samplerUniform = gl.getUniformLocation(program3d, "sampler");
    program3d.cursorUniform = gl.getUniformLocation(program3d, "cursorCoord");

    // use first program for now

    gl.useProgram(program);
    gl.enableVertexAttribArray(program.vertexPositionAttribute);
    gl.enableVertexAttribArray(program.texturePositionAttribute);
}

function makeGravMutator(x0,y0,G)
{
    return function (x,y) {
	var dir = vec2.normalize(vec2.create(), vec2.fromValues(x-x0,y-y0));
	var pow = G/vec2.squaredLength(dir);
	//console.log("Created mutator: Pow: " + pow + " G: " + G + " direction: " + dir);
	return {x: x - dir[0]*pow, y:y - dir[1]*pow};
    };
}

function makeGrid(vertices, startPos, gridSize, left, width, mutator)
{
    var numPoints = 0;
    var pos = startPos;
    for (i=0; i<gridSize; ++i) {
	for (j=0; j<gridSize; ++j) {
	    var x = left + width*(j/(gridSize-1.0));   // x coord
	    var y = left + width*(i/(gridSize-1.0)); // y coord
	    if (mutator!== undefined) {
		var pt = mutator(x,y);
		//console.log("Mutated amount: " + (x-pt.x) + ", " + (y-pt.y));
		x = pt.x;
		y = pt.y;
	    }
	    vertices[pos++] = x;
	    vertices[pos++] = y;

	    numPoints++;

	}
    }
    return numPoints; // or (pos - startPos)/2 now
}

function makeSceneElement(name) {
    var element = function() {};
    if (scene.element === undefined) {
	scene.element = {};
    }
    element.name = name;
    scene.element[name] = element;
    return element;
}

function makeGridElements(elements, start, gridSize, elemMaker)
{
    var i,j;
    var posElem = start;
    var numElems = 0;
    for (i=0; i<=gridSize; ++i) {
	for (j=0; j<=gridSize; ++j) {
	    // set up vertex index array for elements
	    if (j<gridSize-1 && i<gridSize-1) {                             
		// triangle 1 [0, 1, 2]
		//if (vertexIdx + gridSize > gridSize*gridSize-1) {
		//    console.log("Overrun: " + i + ", " + j + " idx: " + vertexIdx);
		//}
		function addElem(x,y) {
		    var elem = elemMaker(x,y);
		    for (var p=0;p<elem.length;++p) 
			elements[posElem++] = elem[p];
		    return elem;
		}
		addElem(i  , j); numElems++;
		addElem(i  , j+1); numElems++;
		addElem(i+1, j+1); numElems++;
		// triangle 2 [2, 3, 0]
		addElem(i+1, j+1); numElems++;
		addElem(i+1, j); numElems++;
		addElem(i  , j); numElems++;
	    }
	}
    }
    return numElems;
}

function makeGridSplit(elements, start, gridSize, left, width, zcoord)
{
    if (zcoord === undefined) {
	return makeGridElements(elements, start, gridSize, function(i,j) {
	    return [left + width*(j/(gridSize-1.0)), left + width*(i/(gridSize-1.0))];
	});
    } else {
	return makeGridElements(elements, start, gridSize, function(i,j) {
	    return [left + width*(j/(gridSize-1.0)), left + width*(i/(gridSize-1.0)), zcoord];
	});
    }
}


var gridSize = 20;
function loadScene()
{

    scene.texture = {};
    scene.frame = 0;

    var element = makeSceneElement('triangles');

    var vertices = new Float32Array(gridSize*gridSize*2);
    element.vertices = vertices;
    element.vectComponents = 2;
    
    var texCoords = new Float32Array(gridSize*gridSize*2);
    var elements = new Uint16Array(gridSize*gridSize*6); // two triangles per subdivided quad



    var numVertices = makeGrid(vertices, 0, gridSize, -2.0, 4.0);
    makeGrid(texCoords, 0, gridSize, 0.0, 1.0);

    var posElem = makeGridElements(elements, 0, gridSize, function(i,j) { return [i*gridSize + j]; });

    //scene.element['triangles'].numElements = gridSize * gridSize * 6;
    element.numElements = posElem;
    element.numVertices = numVertices;
    element.offsetElements = 0;

    // Now create buffers for those arrays

    var vertexBuffer = gl.createBuffer();
    gl.bindBuffer(gl.ARRAY_BUFFER, vertexBuffer);
    gl.bufferData(gl.ARRAY_BUFFER, vertices, gl.DYNAMIC_DRAW);   // We expect to change vertex coordinates per draw
    element.vertexBuffer = vertexBuffer;
    
    var elemBuffer = gl.createBuffer();
    gl.bindBuffer(gl.ELEMENT_ARRAY_BUFFER, elemBuffer); 
    gl.bufferData(gl.ELEMENT_ARRAY_BUFFER, elements, gl.STATIC_DRAW);
    element.elemBuffer = elemBuffer;

    var texCoordBuffer = gl.createBuffer();
    gl.bindBuffer(gl.ARRAY_BUFFER, texCoordBuffer);
    gl.bufferData(gl.ARRAY_BUFFER, texCoords, gl.STATIC_DRAW);
    element.texCoordBuffer = texCoordBuffer;

    scene.transform = mat3.identity(mat3.create());
    scene.transform3d = mat4.identity(mat4.create());

    scene.texture['default'] = ImageTexture('../samples/helix_blancoHubble_1080.jpg');
//    scene.texture['default'] = ImageTexture('../samples/grid-checker-fabric-texture-13-512x512.jpg');

    gl.bindBuffer(gl.ARRAY_BUFFER, null);
    setViewportSize();
}


function createRandomTrans(array, startPos)
{
    return mat4.create();
}

function createSplitTriaBufs()
{
    var vertices = new Float32Array(gridSize*gridSize*6*3); // 
    var texCoords = new Float32Array(gridSize*gridSize*6*3); // 2 additonal pts per 4 grid pts
    var element = makeSceneElement('triangles2');

    element.vertices = vertices;
    var numVertices = makeGridSplit(vertices, 0, gridSize, -2.0, 4.0, -1.0); // -1.0);
    makeGridSplit(texCoords, 0, gridSize, 0.0, 1.0);
    element.numVertices = numVertices;
    element.offsetElements = 0;
    element.vectComponents = 3;

    var vertexBuffer = gl.createBuffer();
    gl.bindBuffer(gl.ARRAY_BUFFER, vertexBuffer);
    gl.bufferData(gl.ARRAY_BUFFER, vertices, gl.DYNAMIC_DRAW);
    element.vertexBuffer = vertexBuffer;
    
    var texCoordBuffer = gl.createBuffer();
    gl.bindBuffer(gl.ARRAY_BUFFER, texCoordBuffer);
    gl.bufferData(gl.ARRAY_BUFFER, texCoords, gl.STATIC_DRAW);
    element.texCoordBuffer = texCoordBuffer;

    gl.bindBuffer(gl.ARRAY_BUFFER, null);
}

function deviceToFrameCoord(device_pos)
{
    return vec2.fromValues( (device_pos[0] + 1.)/2. * gl.drawingBufferWidth, (device_pos[1] + 1.)/2. * gl.drawingBufferHeight);
}


function drawScene()
{
    gl.viewport(0, 0, gl.drawingBufferWidth, gl.drawingBufferHeight);
    gl.clear(gl.COLOR_BUFFER_BIT|gl.DEPTH_BUFFER_BIT);

    // always active gl.useProgram(scene.shader['default']);
    // gl.useProgram(scene.shader['default']);

    var shader = (scene.mode == 'split') ? '3d' : 'default';
    var transform = (scene.mode == 'split') ? scene.transform3d : scene.transform;
    var element = (scene.mode == 'split') ? scene.element['triangles2'] : scene.element['triangles'];

    if (scene.mode != 'split') {
	gl.uniformMatrix3fv(scene.shader['default'].transformUniform, gl.FALSE, scene.transform);
	if (scene.cursorPos !== undefined) {
	    var inverse_trans = mat3.invert(mat3.create(),scene.transform);
	    var touch_pos = vec2.transformMat3(vec2.create(), scene.cursorPos, inverse_trans);
	    var device_pos =  vec2.transformMat3(vec2.create(), scene.cursorPos, scene.transform);
	    var canvas = document.getElementById("canvas1");
	    var w = canvas.clientWidth;
	    var h = canvas.clientHeight;
	    var frame_pos = deviceToFrameCoord(scene.cursorPos); // retransform relative canvas pos back to framebuffer (almost the same)
	    //	gl.uniform2f(scene.shader['default'].cursorUniform, device_pos[0], device_pos[1]);
	    gl.uniform2f(scene.shader['default'].cursorUniform, frame_pos[0], frame_pos[1]);
	    //console.log("Cursor: " + scene.cursorPos.toString() + " -> " + device_pos.toString() + " -> " + frame_pos.toString());

	    var vertices = scene.element['triangles'].vertices;
	    gl.bindBuffer(gl.ARRAY_BUFFER, scene.element['triangles'].vertexBuffer);
	    var gravMutator = makeGravMutator(touch_pos[0], touch_pos[1], state.G.current);
	    var numVertices = makeGrid(vertices, 0, gridSize, -2.0, 4.0, gravMutator);
	    //var subArr = vertices.subarray(numVertices*2);  // how many items we want to replace
	    gl.bufferSubData(gl.ARRAY_BUFFER, 0, vertices); //subArr);   // here we replace basically all of them.
	    // we are generating more vertices than we should?


	}
    } else {
	gl.uniformMatrix4fv(scene.shader['3d'].transformUniform, gl.FALSE, scene.transform3d);
    }
    
    // maybe also activate it only once
    gl.activeTexture(gl.TEXTURE0);
    gl.bindTexture(gl.TEXTURE_2D, scene.texture['default']);
    gl.uniform1i(shader.samplerUniform, 0);
    
    drawSceneElement(element);

    gl.flush();
}


function drawSceneElement (element) // and shader as param later on
{

    gl.bindBuffer(gl.ARRAY_BUFFER, element.vertexBuffer);
    gl.vertexAttribPointer(scene.shader['default'].vertexPositionAttribute, element.vectComponents, gl.FLOAT, false, 0, 0); 

    if (element.elemBuffer) {
	gl.bindBuffer(gl.ELEMENT_ARRAY_BUFFER, element.elemBuffer);
    }
	
    gl.bindBuffer(gl.ARRAY_BUFFER, element.texCoordBuffer);
    gl.vertexAttribPointer(scene.shader['default'].texturePositionAttribute, 2, gl.FLOAT, false, 0, 0);     

    if (element.elemBuffer !==  undefined) {
	gl.drawElements(gl.TRIANGLES, element.numElements, gl.UNSIGNED_SHORT, element.offsetElements);
    } else {
	gl.drawArrays(gl.TRIANGLES, element.offsetElements, element.numVertices);
    }

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

    var w = canvas.clientWidth;
    var h = canvas.clientHeight;
    if (canvas.width != w)
	canvas.width = w;
    if (canvas.height != h)
	canvas.height = h;
    console.log("Resize canvas size: " + canvas.width + ", " + canvas.height + " clientsize: " + canvas.clientWidth + ", " + canvas.clientHeight);
    console.log("Resize buffer size: " + gl.drawingBufferWidth + ", " + gl.drawingBufferHeight);
}

function doKeyPress(event) {

    var chCode = ('charCode' in event) ? event.charCode : event.keyCode;
    console.log("Key pressed: " + chCode);
    var triggered = false;
    if (chCode == 'a'.charCodeAt(0) || chCode == 37) {
	triggered = true;
	velocity -= maxSpeed/10.;
	if (velocity < -maxSpeed)
	    velocity = -maxSpeed;
    } else if (chCode =='d'.charCodeAt(0) || chCode == 39) {
	triggered = true;
 	velocity += maxSpeed/10.;
	if (velocity > maxSpeed)
	    velocity = maxSpeed;
    } else if (chCode =='q'.charCodeAt(0)) {
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

function doMouseMove(evt) {
    var canvas = document.getElementById("canvas1");
    //console.log("Mouse move: " + evt.x + ", " + evt.y);
    scene.cursorPos = vec2.fromValues (evt.x/canvas.width*2.0 - 1.0, 1.0 - evt.y/canvas.height*2.0);
} 

function doMouseDown(evt) {
    state.mouseDown = true;
    state.G.state = 'charge';
}
function doMouseUp(evt) {
    if (state.G.charged()) {
	state.G.state = 'blow';
	state.G.blown += 1;
	if (state.G.blown > 2) {
	    scene.mode = 'split';
	    if (scene.element['triangles2'] === undefined) {
		createSplitTriaBufs();
		var program = scene.shader['3d'];
		console.log("Switching to 3d shader");
		gl.useProgram(program);
		gl.enableVertexAttribArray(program.vertexPositionAttribute);
		gl.enableVertexAttribArray(program.texturePositionAttribute);
	    }
	}
    } else {
	state.G.state = 'none';
    }
}

function updateScene() {
    scene.frame++;
    if (scene.nextVelFrame === undefined || scene.frame > scene.nextVelFrame) {
	scene.nextVelFrame = scene.frame + Math.random()*200 - 50;
	scene.velocity = vec2.fromValues(Math.random()*0.01 - 0.005, Math.random()*0.01 - 0.005);
    }
    if (scene.mode != 'split') {
	mat3.translate(scene.transform, scene.transform, scene.velocity);
    } else {
	mat4.translate(scene.transform3d, scene.transform3d, vec3.fromValues(scene.velocity[0], scene.velocity[1], 0.0));
    }
    state.G.update();
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
//	console.log("Frame, speed=" + velocity + " position: " + position);
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
