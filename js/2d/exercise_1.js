

function startExercise1() {
    console.log("Start exercise 1");
    var div = document.getElementById("main");
    
    var fb = createFramebuffer(60,15);
    clearFramebuffer(fb);
    putPixel(fb, 3, 5, "*".charCodeAt(0));

    consoleprintFramebuffer(fb);
    printFramebuffer(div, fb);
    putPixel(fb, 20, 12, "#".charCodeAt(0));
    
    consoleprintFramebuffer(fb);
    printFramebuffer(div, fb);
}
