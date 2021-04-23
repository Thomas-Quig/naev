// Change heading:
document.getElementById("myH").innerHTML = "My First Page";

// Change paragraph:
document.getElementById('myP').innerHTML = 'My first paragraph.';
var x = 5;      // Declare x, give it the value of 5
var y = x + 2;  // Declare y, give it the value of x + 2

export let a1, a2, a3;
export let b1="asdf", b2=4,b3=26.0;
export var c1, c2, c3;
export var d1="asdfadsf", d2="fjasg", d3;

export class class1 {
    outerparam1;
    outerparam2 = "asdf";
    static staticparam1 = "asdfasd";
    static staticparam2 = "asdfsdfsfssf";
    outerparam3 = 5626;
    _ignoredparam1=25;
    #ignoredparam2;

    constructor(p1, p2=5) {
        this.innerparam1 = 1435;
        this.innerparam2 = this.innerparam1;
        thisisastatement;
    }

    // comment is here
    static staticparam3;
    static staticmethod1(p1,p2,p3,p4) {
        var asdf = 1523;
        let sdfasdf = 2626;
        return 5;
    }
    /*
    ingoredmethod() {
        return null;
    }
    */
    method1() {
        this.innerparam3;
        return staticmethod1(1,2,3,4);
        //comment
    }
    static staticmethod2() {
        return 2;
    }
    
    method2(p1=3,p2=5) {
        this.innerparam4 = p1 * p2;
    }
}

export class class2 {
    onlyval=1;
}

export class class3{
    outerparam1;
    constructor(p1) {
        this.innerparam1 = p1;
    }
    get outerparam1() {
        return this.outerparam1;
    }

    //comment
    set outerparam1(p1) {
        this.outerparam1=p1;
    }
}

/*
The code below will change
the heading with id = "myH"
and the paragraph with id = "myP"
in my web page:
*/
document.getElementById("myH").innerHTML = 'My First Page';
document.getElementById("myP").innerHTML = "My first paragraph.";

export function asdf(p1,p2,p3,p4=5, p5="asdf") {
    var x = 5;
    // This is a comment
}