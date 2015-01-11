var scene = new THREE.Scene();
var camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
camera.position.set (30, 30, 30);
var controls;
var renderer = new THREE.WebGLRenderer();
renderer.setSize( window.innerWidth, window.innerHeight);
document.body.appendChild( renderer.domElement);


function createLights() {

    var light = new THREE.PointLight(0xffffff, 1, 1400);
    light.position.set(250, 40, 560);
    light.castShadow = true;
    scene.add(light);
    var light_ambient = new THREE.AmbientLight(0x404040);
    scene.add(light_ambient);
    
    var spotLight = new THREE.SpotLight( 0x3030ff );
    spotLight.position.set(100, 300, 1000);
    spotLight.castShadow = true;
    spotLight.shadowMapWidth = 1024;
    spotLight.shadowMapHeight = 1024;
    spotLight.shadowCameraNear = 500;
    spotLight.shadowCameraFar = 4000;
    spotLight.shadowCameraFov = 30;
    spotLight.target.position.set( 10, 0, 0);
    scene.add(spotLight);
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

console.log("Started creating scene");


createLights();
createControls();
var geometry = new THREE.BoxGeometry(20, 0.2, 20);

var texture = new THREE.Texture();
var material = new THREE.MeshBasicMaterial({ color: 0xf0f0ff });
//var material = new THREE.MeshFaceMaterial({ color: 0xffffff, map:texture });
var plane = new THREE.Mesh(geometry, material);
plane.matrixAutoUpdate = true;
plane.position.set (0, -1.2, 0);
plane.receiveShadow = true;
scene.add(plane);


function createObjects(x, y, z, material)
{
    var obj = new THREE.Object3D();
    obj.matrixAutoUpdate = true;
    var cube = new THREE.Mesh(new THREE.BoxGeometry(2,2,2), material.clone());
    cube.matrixAutoUpdate = true;
    cube.position.z = -2;
    obj.add(cube);
    var cyl = new THREE.Mesh(new THREE.CylinderGeometry(0.1,1,2,32), material.clone());
    cyl.matrixAutoUpdate = true;
    cyl.position.z = 0;
    obj.add(cyl);
    var sph = new THREE.Mesh(new THREE.SphereGeometry(1,32,32), material.clone());
    sph.matrixAutoUpdate = true;
    sph.position.z = 2;
    obj.add(sph);
    obj.position.set(x, y, z);
    scene.add(obj);
}

var mat = null;
mat = new THREE.MeshPhongMaterial( { ambient: 0x202020, color: 0x70ff70, specular: 0x9999ff, shininess: 30, shading: THREE.SmoothShading });
createObjects(-5, 0, 0, mat);
mat = new THREE.MeshPhongMaterial( { ambient: 0x202020, color: 0xff7070, specular: 0xa0a0ff, shininess: 100, shading: THREE.SmoothShading });
createObjects(0, 0, 0, mat);
mat = new THREE.MeshPhongMaterial( { ambient: 0x202020, color: 0x7070ff, specular: 0xffa0a0, shininess: 200, shading: THREE.SmoothShading });
createObjects(5, 0, 0, mat);



var manager = new THREE.LoadingManager();
manager.onProgress = function ( item, loaded, total ) {
    console.log("Loading: ", item, loaded, total);
};





var imageLoader = new THREE.ImageLoader(manager);
imageLoader.load( '../samples/UV_Grid_Sm.jpg', function ( image ) {
    texture.image = image;
    texture.needsUpdate = true;
    plane.material.map = texture;
});


function render() {
    controls.update();
    requestAnimationFrame(render);
    renderer.render(scene, camera);

    //if (obj && obj.rotation) {
    //obj.rotation.y += 0.001;
    //}
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
