String.prototype.getKeyCode = function () {
    return this.toUpperCase().charCodeAt(0);
};

var vs = function () {};

function createTrackballControl(camera) {
    
    controls = new THREE.TrackballControls(camera);
    controls.rotateSpeed = 1.0;
    controls.zoomSpeed = 1.2;
    controls.panSpeed = 1.1;
    
    controls.noZoom = false;
    controls.noPan = false;
    controls.staticMoving = true;
    controls.dynamicDampingFactor = 0.15;

    vs.controls = controls;
}



// similar for camera and resize. register cameras
function getKeyMapper () {
    function onKeyDown(evt) {
	if (vs.keymap === undefined) 
	    return;
	for (var key in vs.keymap) {
	    if (vs.keymap.hasOwnProperty(key)) {
		if (key.getKeyCode() == evt.keyCode)
		    vs.keymap[key].func(evt.keyCode);
	    }
	}
    }

    if (vs.keymap === undefined) {
	vs.keymap = {};
	window.addEventListener('keydown', onKeyDown, false);
    }
    vs.keymap.addKeyMapping = function (key, func, description) {
	var map = {};
	map.func = func;
	map.description = description;
	vs.keymap[key] = map;
	
    };
   vs.keymap.addElement = function () {
       // create elem fill with descs, add it to doc
   }
}


function registerKeyMapping (keycode, func, description)
{
}

