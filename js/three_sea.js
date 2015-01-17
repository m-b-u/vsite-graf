/*
  Boat - rough torus
  See sin(x+y)
  Boat rocking
  Physics?
  Man, hand, flare
*/


var scene = new THREE.Scene();
var camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
camera.position.set (0, 3, 6);
camera.lookAt (0, 0.3, 0);
var camera2;
var activeCamera = camera;
var controls;
var renderer = new THREE.WebGLRenderer({ maxLights: 6});
renderer.setSize( window.innerWidth, window.innerHeight);
document.body.appendChild( renderer.domElement);

var clock = new THREE.Clock(true);
var g = new THREE.Vector3(0, -9.81, 0);
var flare_lights = [];

var flares = [];
flares.current_light = 0;

function switchCamera()
{
    if (activeCamera == camera) {
	activeCamera = camera2 || camera;
    } else {
	activeCamera = camera;
    }
    console.log("Switching camera to " + (activeCamera == camera ? " standard" : " person"));
}

function createLights() {

    var light = new THREE.PointLight(0xffffd0, 1, 1400);
    light.position.set(150, 500, 100);
    light.castShadow = true;
    scene.add(light);
    var light_ambient = new THREE.AmbientLight(0x404040);
    scene.add(light_ambient);

    for (var i=0; i<4; ++i) {
	flare_lights[i] = new THREE.PointLight(0x000000, 0, 1);
	scene.add(flare_lights[i]);
    }
    
}

function createControls() {
    controls = new THREE.TrackballControls( camera );
    controls.rotateSpeed = 1.0;
    controls.zoomSpeed = 1.2;
    controls.panSpeed = 1.1;
    
    controls.noZoom = false;
    controls.noPan = false;
    controls.staticMoving = true;
    controls.dynamicDampingFactor = 0.15;
}


function createSea()
{
    var mat = new THREE.MeshPhongMaterial( { ambient: 0x3030ff, color: 0x2020ff, specular: 0xe0e040, shininess: 1500, shading: THREE.SmoothShading });
    var geometry = new THREE.PlaneGeometry(300, 300, 200, 200);
    var mat_under = new THREE.MeshLambertMaterial( { ambient: 0x3030ff, color: 0x2020ff, shading: THREE.FlatShading });

    //var norm = THREE.ImageUtils.generateDataTexture(1024, 1024, 0x808080); //THREE.ImageUtils.loadTexture( "textures/normal/ninja/normal.jpg" );
    //mat.normalMap = norm; // uniforms['tNormal'].value;
    

    var sea = new THREE.Mesh(geometry, mat);
    var sea_under = new THREE.Mesh(geometry, mat_under);
    sea.rotation.x = -Math.PI/2;
    scene.add(sea);
    sea.updateMatrix();

    sea_under.rotation.x = Math.PI/2;
    sea_under.updateMatrix();
    mat_under.transparent = true;
    mat_under.opacity = 0.6;
    scene.add(sea_under);

    return sea;
}

function createBoat()
{
    var boat = new THREE.Object3D();
    var mat = new THREE.MeshLambertMaterial( { color: 0xff0000, ambient: 0xff4040 } );
    var tube_radius = 0.2;
    var geometry = new THREE.TorusGeometry(1, tube_radius, 40, 8);
    var boat_mesh = new THREE.Mesh (geometry, mat);
    boat_mesh.scale.set(1, 1.5, 1);
    boat_mesh.position.y = tube_radius/2;
    boat_mesh.rotation.x = Math.PI/2;
    boat_mesh.updateMatrix();
    boat.add(boat_mesh);
    var floor_geometry = new THREE.BoxGeometry(1.75, 0.01, 2.45);
    var mat_floor = new THREE.MeshLambertMaterial( { color: 'brown', ambient: 'brown', specular: 0xe0e040, shininess: 500, shading: THREE.SmoothShading } );
    var floor_mesh = new THREE.Mesh(floor_geometry, mat_floor);
    // this lets "sea" in boat: floor_mesh.position.y = - tube_radius/2;
    floor_mesh.position.y =  tube_radius/20;
    floor_mesh.updateMatrix();
    
    boat.add(floor_mesh);
    return boat;
}

function createMan(parent)
{
    var man = new THREE.Object3D();
    if (parent) {
	parent.add(man);
    } else {
	scene.add(man);
    }
    var skin_material = new THREE.MeshLambertMaterial( { color: 0xe0b080 } );

    var torso = new THREE.Mesh(new THREE.BoxGeometry(0.2, 0.5, 0.07), skin_material);
    torso.position.set(0, 1.2, 0);
    torso.updateMatrix();

    var head = new THREE.Mesh(new THREE.SphereGeometry(0.1, 20, 20), skin_material);
    head.position.set(0, 0.4, 0);
    head.updateMatrix();
    torso.add(head);
    
    
    var trouser_material = new THREE.MeshLambertMaterial( { color: 0x3030a0, ambient: 0x3030a0 } );
    var leg_geometry = new THREE.BoxGeometry(0.1, 0.8, 0.12);
    
    var leg = new THREE.Mesh(leg_geometry,trouser_material);
    leg.position.set(-0.08, -0.6, 0);
    var leg2 = leg.clone();
    leg2.position.x = 0.08;
    leg.updateMatrix(); leg2.updateMatrix();
    torso.add(leg); torso.add(leg2);

    var hand_geometry = new THREE.BoxGeometry(0.07, 0.45, 0.07);
    var hand = new THREE.Mesh(hand_geometry, skin_material);
    var hand2 = hand.clone();
    hand.position.set(-0.15, 0, 0);
    hand2.position.set(0.15, 0, 0);
    hand.rotation.useQuaternion = true;
    //	  hand.rotation.quaternion.setFromUnitVectors(new THREE.Vector3( 0, -1, 0 ), //
    //						new THREE.Vector3( 
    var hand_quat = new THREE.Quaternion();
    hand_quat.setFromAxisAngle(new THREE.Vector3( 0, 0, -1 ), Math.PI * 3 / 4.0); 
    hand.rotation.quaternion = hand_quat;

    hand.updateMatrix(); hand2.updateMatrix();
    torso.add(hand); torso.add(hand2);
    var head_camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
    head.add(head_camera);
    man.add(torso);
    man.head_camera = head_camera;
    camera2 = head_camera;

    man.hand_pos = function(o) {
	//scene.updateMatrixWorld();
	return { end: hand.localToWorld (new THREE.Vector3( 0, -0.45, 0)),
		 start: hand.localToWorld (new THREE.Vector3( 0, 0, 0)) };
    }
    return man;

}

console.log("Started creating scene");


createLights();
createControls();
createSea();
var boat = createBoat();
scene.add(boat);
var man = createMan(boat);

var texture=new THREE.Texture();

var manager = new THREE.LoadingManager();
manager.onProgress = function ( item, loaded, total ) {
    console.log("Loading: ", item, loaded, total);
};





var imageLoader = new THREE.ImageLoader(manager);
imageLoader.load( '../samples/UV_Grid_Sm.jpg', function ( image ) {
    texture.image = image;
    texture.needsUpdate = true;
//    plane.material.map = texture;
});


function flares_prerender(dt)
{
    var i;
    for (i = flares.length-1; i>=0; --i) {
        if (i >= flares.length)
            break; // if we deleted last flare
	var flare = flares[i];
	if (clock.getElapsedTime() - flare.time > 40) {
	    if (flare.light) {
		flare.light.intensity = 0;
		flare.light.distance = 1;
	    }
	    scene.remove(flare);
	    flares.splice(i,1);
            console.log("Flare deleted: #" + i + " remaining: " + flares.length);
	    continue;
	}
	
	flare.prev_velocity = flare.velocity.clone();
	var gdt = g.clone();
	gdt.multiplyScalar(dt);
	if (!flare.active)
	    flare.velocity.add(gdt);
	else
	    flare.velocity.add(gdt.multiplyScalar(0.1));
	flare.position.add(flare.velocity.clone().multiplyScalar(dt));
	if (flare.light)
	    flare.light.position.copy(flare.position);
	if (!flare.active && flare.velocity.length() > flare.prev_velocity.length()) {
	    flare.active = true;
	    console.log("Flare activated: #" + i);
	    //flare.emissive = new THREE.Color (0xffffff);
	    if (flare.light) {
		flare.light.intensity *= 3;
		flare.light.distance *= 5;
	    }

	}
	flare.updateMatrix();
    }
}

function render() {
    var dt = clock.getDelta();
    flares_prerender(dt);
    controls.update();
    requestAnimationFrame(render);
    renderer.render(scene, activeCamera);

    //if (obj && obj.rotation) {
    //obj.rotation.y += 0.001;
    //}
}
var flare_material = new THREE.MeshLambertMaterial( { emissive: 0xffffff });
var flare_num = 0;
var flare_colors = [ 0xffff80, 0xff80ff, 0x80ffff, 0xffc0c0, 0xc0ffc0, 0xc0c0ff ];
function fireFlare()
{
    console.log("Fire flare: " + flare_num);
    var hand_pos = man.hand_pos();
    var dir = new THREE.Vector3().subVectors(hand_pos.end, hand_pos.start).normalize();
    var mat = flare_material.clone();
    mat.emissive = new THREE.Color(flare_colors[flare_num % flare_colors.length]);
    var flare = new THREE.Mesh(new THREE.SphereGeometry(0.05), mat);
    flare.time = clock.getElapsedTime();
    flare_num++;
    flare.position.copy(hand_pos.end);
    flare.velocity = dir.clone();
    flare.velocity.multiplyScalar(-20);  // this should be positive once the hand is ok oriented, for testing 
    
    var light = flare_lights[flares.current_light++];
    flares.current_light %= flare_lights.length;
    flare.light = light;
    light.color = mat.emissive.clone();
    light.intensity = 1;
    light.distance = 1500;
    light.position.copy(flare.position);
    //flare.add(light); it's now outside
    // also not needed, light is now separate // flare.frustumCulled = false;
    flares.push(flare);
    scene.add(flare);
}

function onKeyDown(event)
{
    var result;
    switch (event.keyCode) {
      case '1': // '1'
	// Day/night
        break;
      case 50:
	// Sea lod
        break;
      case ' ':
      case 'e':
	fireFlare();
	break;
      case 'c': // 'C'
	switchCamera();
	break;
    }
}

function onWindowResize() {
    
    windowHalfX = window.innerWidth / 2;
    windowHalfY = window.innerHeight / 2;
    
    function fixCamera(camera) {
	camera.aspect = window.innerWidth / window.innerHeight;
	camera.updateProjectionMatrix();    
    }
    fixCamera(camera);
    if (camera2) 
	fixCamera(camera2);
    renderer.setSize( window.innerWidth, window.innerHeight );
    
}

window.addEventListener( 'resize', onWindowResize, false );
window.addEventListener( 'keydown', onKeyDown, false );


console.log("Up to render!");
render();
