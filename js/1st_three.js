console.log("Started creating scene");
var scene = new THREE.Scene();
var camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
//var camera = new THREE.OrthographicCamera( width / - 2, width / 2, height / 2, height / - 2, 1, 1000 ); scene.add( camera );
camera.position.z = 5;

var renderer = new THREE.WebGLRenderer();
renderer.setSize( window.innerWidth, window.innerHeight);
document.body.appendChild( renderer.domElement);

var light = new THREE.PointLight(0xffffff, 1, 1400);
light.position.set(250, 40, 560);
light.castShadow = true;
scene.add(light);
var light_diffuse = new THREE.AmbientLight(0x404040);
scene.add(light_diffuse);


var spotLight = new THREE.SpotLight( 0xffffff );
spotLight.position.set(100, 300, 1000);

spotLight.castShadow = true;

spotLight.shadowMapWidth = 1024;
spotLight.shadowMapHeight = 1024;

spotLight.shadowCameraNear = 500;
spotLight.shadowCameraFar = 4000;
spotLight.shadowCameraFov = 30;
spotLight.target.position.set( 10, 10, 5);
scene.add(spotLight);

var geometry = new THREE.BoxGeometry(1, 1, 1);
//var material = new THREE.MeshBasicMaterial({ color: 0xf0f0ff });
var material = new THREE.MeshLambertMaterial({ color: 0xf0f0ff });
var cube = new THREE.Mesh(geometry, material);


var cube_wire = new THREE.BoxHelper(cube);
cube_wire.material.color.set(0x80ff80);
cube_wire.matrixAutoUpdate = true;
cube_wire.scale.set(5, 5, 5);

scene.add(cube_wire);


controls = new THREE.TrackballControls( camera );

controls.rotateSpeed = 1.0;
controls.zoomSpeed = 1.2;
controls.panSpeed = 0.8;

controls.noZoom = false;
controls.noPan = false;

controls.staticMoving = true;
controls.dynamicDampingFactor = 0.15;

var manager = new THREE.LoadingManager();
manager.onProgress = function ( item, loaded, total ) {
    console.log("Loading: ", item, loaded, total);
};


var model_material = new THREE.MeshPhongMaterial( { ambient: 0x030303, color: 0xdddddd, specular: 0x000099, shininess: 300, shading: THREE.SmoothShading });
// model
var obj = null;
//var loader = new THREE.OBJMTLLoader(manager);
//loader.load( '../samples/rendu_argos.obj', '../samples/rendu_argos.mtl', function ( object ) {
var loader = new THREE.OBJLoader(manager);
loader.load( '../samples/rendu_argos.obj', function ( object ) {

//var loader = new THREE.STLLoader(manager);
//loader.load( '../samples/slottedDisk.stl', function ( object ) {


    console.log("Loaded!");
    object.traverse( function ( child ) {
	console.log("Test type: ", child.type);
	if ( child instanceof THREE.Mesh ) {	    
	    console.log("Setting material for:" , child);
	    child.material = model_material;
	}	
    });
    
    /*    var geometry = object;
	  if (geometry.hasColors) {
	  material = new THREE.MeshPhongMaterial( {opacity: geometry.alpha, vertexColor: THREE.VertexColors });
	  obj = THREE.Mesh(geometry, material);
	  } else {
	  obj = THREE.Mesh(geometry);
	  }
    */
    object.receiveShadow = true;
    obj = object;
    var geometry = object.geometry || object.children[0].geometry;
    geometry.computeBoundingBox();
    var box = geometry.boundingBox.clone();
    cube_wire.scale.set (box.max - box.min);
    scene.add(obj);

    var size = box.size();
    var boxgeometry = new THREE.BoxGeometry(size.x * 1.03, size.y * 0.03, size.z * 1.03);

    var material = new THREE.MeshPhongMaterial({ color: 0x30ff30 });
    var cube = new THREE.Mesh(boxgeometry, material);
    cube.position.y = box.min.y - size.y * 0.015;
    scene.add(cube);
    console.log("Box: ", box);
//    camera.position.set (box.max * 1.8);
    var rad = Math.max(size.x,size.z) ;
    var geometry = new THREE.CylinderGeometry( rad, rad, size.y * 0.04, 32, 1 );
    var material = new THREE.MeshBasicMaterial({ color: 0xf0f0ff });
    var cyl = new THREE.Mesh(geometry,material);
    //cyl.rotation.x = Math.PI / 2;
    scene.add(cyl);
    camera.position.set (30, 30, 30);
    
}, function (object) {
    console.log("Progress.."); 
}, function (xhr) { 
    console.log ("Error loading object");
} );



function render() {
    controls.update();
    requestAnimationFrame(render);
    renderer.render(scene, camera);
    cube_wire.rotation.y += 0.001;
    if (obj && obj.rotation) {
	obj.rotation.y += 0.001;
    }
}


function onWindowResize() {
    
    windowHalfX = window.innerWidth / 2;
    windowHalfY = window.innerHeight / 2;
    
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();    
    renderer.setSize( window.innerWidth, window.innerHeight );
    
}

window.addEventListener( 'resize', onWindowResize, false );


console.log("Up to render!");
render();
