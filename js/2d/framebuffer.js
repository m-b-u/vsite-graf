
/* Creates the Uint8Array, of dimension M*N, to 
   represent our 8-bit deep frame-buffer. Mostly in browser contexts
   we will get it from other sources, often 32-bit deep 
*/
function createFramebuffer(M, N) {
    var A = new Uint8Array(N*M);
    A.rows=N;
    A.columns=M;
    return A;
}

/* Clears the 8-bit frame-buffer, default fill is <SPACE> if not otherwise 
   specified */
function clearFramebuffer(A, fill) {
    if (typeof fill == 'undefined') {
	fill = " ".charCodeAt(0);
    }
    for (var i=0; i<A.length; ++i) {
	A[i] = fill;
    }
}

/* Put the 8-bit value to pixel at coordinate (x, y) */
function putPixel(A, x, y, value) {
    A[y*A.columns+x] = value;
}

/* Returns the current pixel value at coordinates (x, y) */
function getPixel(A, x, y) {
    return A[y*A.columns+x];
}

/* This function will add ASCII representation of frame-buffer to 
   specified element, added as <ul> list
*/
function printFramebuffer(elem ,A) {
    var list = document.createElement("ul");
    for (var i=0; i<A.rows; ++i) {
	var rowElem = document.createElement("li");
	var text = new TextDecoder("utf-8").decode(A.subarray(i*A.columns, (i+1)*A.columns));
	var tt = document.createElement("pre");
	tt.innerHTML = text;
	rowElem.appendChild(tt);
	list.appendChild(rowElem);
    }
    elem.appendChild(list);
    elem.appendChild(document.createElement("hr"));
}


/* This function will output the framebuffer to the browser console.
   Note that most browsers nowadays collapse same output lines, 
   so framebuffer look as if some lines are missing
*/
function consoleprintFramebuffer(A) {
    var hline = ['+'];
    for (var i=0; i<A.columns; ++i) {
	hline.push('-');
    }
    hline.push('+');
    hline = hline.join("");
    console.log(hline);
    for (var i=0; i<A.rows; ++i) {
	var row = "|" + new TextDecoder("utf-8").decode(A.subarray(i*A.columns, (i+1)*A.columns)) + "|";
	console.log(row);
    }
    console.log(hline); console.log(""); console.log("");
}

