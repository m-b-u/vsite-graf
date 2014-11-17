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

    var shader = gl.createShader(typeStr)
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
	gl.viewportWidth = canvas.width;
	gl.viewportHeight = canvas.height;
    } catch (e) {
    }
    if (!gl) {
	alert("Error initializing WebGL!");
    }

}



