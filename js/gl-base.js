var gl = null;

function getShaderSource(shaderNode) {
    var shaderSource = "";
    var node = shaderNode.firstChild;
    while (node) {
        if (node.nodeType == 3) // Node.TEXT_NODE
            shaderSource += node.textContent;
        node = node.nextSibling;
    }
    return shaderSource;
}

function getShader(nodeId, typeStr) {
    var shaderNode = document.getElementById(nodeId);
    var shaderSource = getShaderSource(shaderNode);

    var shader = gl.createShader(typeStr);
    gl.shaderSource(shader, shaderSource);
    gl.compileShader(shader);

    if (!gl.getShaderParameter(shader, gl.COMPILE_STATUS)) {
      alert("Shader compilation (" + typeStr + ") GL : " + gl.getShaderInfoLog(shader) + "\nSource: " + shaderSource);
      return false;
    }
    return shader;
}


function initGL() {
    var canvas = document.getElementById("canvas1");
    try {
	gl = canvas.getContext("experimental-webgl");
	gl = WebGLDebugUtils.makeDebugContext(gl);
	gl.viewportWidth = canvas.clientWidth;
	gl.viewportHeight = canvas.clientHeight;
    } catch (e) {
    }
    if (!gl) {
	alert("Error initializing WebGL!");
    }

}

function isPOT(num) 
{
    return (num & (num - 1)) == 0;
}

function initTexture(texture)
{
    console.log("Texture: " + texture.image.src + " loaded, width: " + texture.image.width + ", height: " + texture.image.height);
    gl.bindTexture(gl.TEXTURE_2D, texture);
    gl.pixelStorei(gl.UNPACK_FLIP_Y_WEBGL, true);
    gl.texImage2D(gl.TEXTURE_2D, 0, gl.RGBA, gl.RGBA, gl.UNSIGNED_BYTE, texture.image);


   if (false && isPOT(texture.image.width) && isPOT(texture.image.height)) {
	console.log("POT texture - OK");
	gl.generateMipmap(gl.TEXTURE_2D);
    } else {
	console.log("NOPOT texture - reduce quality");
	gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MAG_FILTER, gl.NEAREST);
	gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MIN_FILTER, gl.NEAREST);
	gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_S, gl.CLAMP_TO_EDGE);
	gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_T, gl.CLAMP_TO_EDGE);
    }
    gl.bindTexture(gl.TEXTURE_2D, null);
    texture.ready = true;
    console.log("Texture inited!");
}


function ImageTexture(src) {
    var texture;
    texture = gl.createTexture();
    texture.image = new Image();
    texture.image.crossOrigin = "anonymous";
    // on Chrome - kill all instances and rerun with –allow-file-access-from-files
    texture.image.onload = function() {
	initTexture(texture);
    };
    texture.image.onerror = function(error) {
	console.log("Error: " + error + " loading texture: " + texture.image.src);
	texture.error = true;
    };
    texture.image.src = src;
    return texture;
}


