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

function KeyMapper() {
    this.keymap = {};
    this.addKeyMapping('?', function(keyCode) {
	console.log("Help!");
	var help = document.getElementById('helpdiv');
	help.style.visibility = 'visible';

    }, "Shows help window");
    window.addEventListener('keydown', this.onKeyDown, false);
}

KeyMapper.prototype = {
    onKeyDown: function (evt) {
	if (this.keymap === undefined) 
	    return;
	for (var key in this.keymap) {
	    if (this.keymap.hasOwnProperty(key)) {
		if (key.getKeyCode() == evt.keyCode)
		    this.keymap[key].func(evt.keyCode);
	    }
	}
    }, 
    addKeyMapping: function (key, func, description) {
	var map = {};
	map.func = func;
	map.description = description;
	this.keymap[key] = map;
    },
    addElement: function () {
	var element = document.createElement("DIV");
	for (var key in this.keymap) {
	    if (this.keymap.hasOwnProperty(key)) {
		var item = document.createTextNode("'" + key + "'" + this.keymap[key].description);
		element.appendChild(item);
	    }
	}
	element.id = 'helpdiv';
	element.style.visibility = 'hidden';

	var help_element = document.createElement("DIV");
	help_element.appendChild(document.createTextNode("Press ?"));
	document.body.appendChild(help_element);
    }
};
    

// similar for camera and resize. register cameras
function getKeyMapper () {
    if (vs.keymap === undefined) {
	vs.keymap = new KeyMapper();
    }
    return vs.keymap;
}


