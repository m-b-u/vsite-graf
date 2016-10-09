
function createFramebuffer(M,N) {
    var A = new Uint8Array(N*M);
    A.rows=N;
    A.columns=M;
    return A;
}

function clearFramebuffer(A) {
    for (var i=0; i<A.length; ++i) {
	A[i]=".".charCodeAt(0);
    }
}

function clearFramebuffer_1D(A) {
    for (var i=0; i<A.rows; ++i) {
	for (var j=0; j<A.columns; ++j) {
	    A[i*A.columns+j]=0;
	}
    }
}

function putPixel(A, x, y, value) {
    A[y*A.columns+x] = value;
}

function getPixel(A, x, y) {
    return A[y*A.columns+x];
}

function printFramebuffer(elem,A) {
    var list=document.createElement("ul");
    for (var i=0; i<A.rows; ++i) {
	var rowElem = document.createElement("li");
	var text = document.createTextNode(new TextDecoder("utf-8").decode(A.subarray(i*A.columns, (i+1)*A.columns)));
	rowElem.appendChild(text);
	list.appendChild(rowElem);
    }
    elem.appendChild(list);
    elem.appendChild(document.createElement("hr"));
}


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

