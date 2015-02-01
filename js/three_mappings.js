var scene = new THREE.Scene();
var camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 10000);
camera.position.set (10, 20, 20);
camera.lookAt (0, 10, 0);


var clock = new THREE.Clock(true);

var renderer = new THREE.WebGLRenderer({ antialias: true });
renderer.setSize( window.innerWidth, window.innerHeight);
renderer.shadowMapEnabled = true;
renderer.shadowMapType = THREE.PCFSoftShadowMap;
document.body.appendChild(renderer.domElement);


var rec_texture = new THREE.WebGLRenderTarget( window.innerWidth, window.innerHeight, { minFilter: THREE.LinearFilter, magFilter: THREE.NearestFilter, format: THREE.RGBFormat, antialias: true } );


createControls();
createLights();

createSkymap();

var mat_floor = new THREE.MeshLambertMaterial( { ambient: 0x303010, color: 0x80A030 });
var floor = new THREE.Mesh(new THREE.PlaneGeometry(300, 300, 5, 5), mat_floor);
floor.receiveShadow = true;
floor.rotation.x = -Math.PI/2;

scene.add(floor);

createSign();
var billboard = createBillboard();

function createSign()
{
    var pole = new THREE.Mesh(new THREE.BoxGeometry(0.05,3.4,0.05), new THREE.MeshLambertMaterial( { color: 0xbbbbbb, ambient: 0xbbbbbb} ));
    pole.position.set(0,1.7,0);

    var canvas = document.createElement('canvas');
    var context = canvas.getContext('2d');
    context.canvas.width = 600;
    context.canvas.height = 75;
    context.beginPath();
    context.fillStyle = "rgba(255,255,00,1)";
    context.rect(0, 0, 600, 75);
    context.fill();
    context.lineWidth = 12;
    context.strokeStyle = 'black';
    context.stroke();
    context.font = "Bold 72px Arial";
    context.fillStyle = 'black';
    context.fillText('Rekurzija d.o.o.', 30, 60);
    
    // canvas contents will be used for a texture
    var texture = new THREE.Texture(canvas); 
    texture.needsUpdate = true;
    
    var material = new THREE.MeshBasicMaterial( {map: texture, side:THREE.DoubleSide } );

    var sign = new THREE.Mesh( new THREE.PlaneGeometry(canvas.width, canvas.height), material );
    sign.position.set(0,2.04,0);
    sign.scale.set(0.01,0.01,0.01);
    pole.add(sign);


    pole.castShadow = true;
    sign.castShadow = true;
    scene.add(pole);

}

function createBillboard()
{
    var pole = new THREE.Mesh(new THREE.BoxGeometry(0.1,7,0.1), new THREE.MeshLambertMaterial( { color: 0xbbbbbb, ambient: 0xbbbbbb} ));
    pole.position.set(-2, 3.5, -15);
    
    var texture = new THREE.Texture();
    var material = new THREE.MeshBasicMaterial( {map: rec_texture, side:THREE.DoubleSide } );

    var sign = new THREE.Mesh(new THREE.PlaneGeometry(12,9), material);
    sign.position.set(0, 8, 0);
    pole.castShadow = true;
    sign.castShadow = true;
    pole.add(sign);
    scene.add(pole);
    
    pole.getTexture = function (o) { return o.sign.material.map; };
    return pole;
}

function createLights()
{
    scene.add(new THREE.AmbientLight(0x666666));

    var light = new THREE.DirectionalLight(0xfdbe8f, 1.75);
    light.position.set(300, 400, 50);
    light.position.multiplyScalar(1.3);

    light.castShadow = true;
    light.shadowCameraVisible = true;

    light.shadowMapWidth = 512;
    light.shadowMapHeight = 512;
    
    scene.add(light);
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

function createSkymap()
{
    var sky_vertex = ' \
       varying vec2 vUV; \
       void main() { \
           vUV = uv; \
           vec4 pos = vec4(position, 1.0); \
           gl_Position = projectionMatrix * modelViewMatrix * pos; \
       }';
    var sky_fragment = ' \
       uniform sampler2D texture; \
       varying vec2 vUV; \
       void main() { \
           vec4 sample = texture2D(texture, vUV); \
           gl_FragColor = vec4(sample.xyz, sample.w); \
       }';

    var geometry = new THREE.SphereGeometry(3000, 60, 40);
    var uniforms = {
	texture: { type: 't', value: THREE.ImageUtils.loadTexture( '../images/skymap_photo8.jpg') }
    };

    var material = new THREE.ShaderMaterial( {
	uniforms:       uniforms,
	vertexShader:   sky_vertex,
	fragmentShader: sky_fragment
    });
    skyBox = new THREE.Mesh(geometry, material);
    skyBox.scale.set(-1, 1, 1);
    skyBox.eulerOrder = 'XZY';

    scene.add(skyBox);

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



function render() {
    var dt = clock.getDelta();
    controls.update();
    requestAnimationFrame(render);
    renderer.render(scene, camera, rec_texture, true);
    //rec_texture.needsUpdate = true;

    renderer.render(scene, camera);

}

function onKeyDown(event)
{
    var result;
    switch (event.keyCode) {
      case 'e':
	// NOP
	break;
    }
}


console.log("Up to render!");
render();
