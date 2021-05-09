/* 
  I am not kidding, this is the stupidest code I've ever written
  but if I didn't do it like this, jest literally wouldn't run.
  I don't know whats going on. I dont WANT to know whats going on.
 
  Please help me.
*/
export function vulnerable()
{
  console.log('VULNERABLE CODE EXECUTED!!!');
}
export function funcOne(i1) {
  //vulnerable()
  return i1 + 2;
}

export function funcTwo(i1) {
  return i1 * 3;
}

export function funcThree(i1, i2){
  return i1 + i2 - 4;
}

export function funcFour(i1){
  if(i1 == 1337)
    return 1337;
  return 7331;
}

export function funcFive(i1,i2,i3){
  if (i1 == i2 && i2 != i3)
    return i1 + i3;
  return i1 + i2;
}

export function funcSix(i1){
  return i1 * i1 * i1;
}

export function funcSeven(i1,i2){
  vulnerable();
  return 0;
}

export function funcEight(i1,i2,i3,i4){
  return i1 * i2 * i3 * i4;
}

export function funcNine(i1, i2, i3){
  vulnerable();
  return i2 * (i3 - i1);
}

export function funcTen(i1){
  return i1;
}