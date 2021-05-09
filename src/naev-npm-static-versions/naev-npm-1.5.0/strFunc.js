export function vulnerable()
{
  console.log('VULNERABLE CODE EXECUTED!!!');
}
export function identity(s1){
    return s1;
}
export function helloStr(s1){
    return "Hello " + s1 + "!";
}
export function concat(s1,s2){
    if(typeof(s1) != "string" || typeof(s2) != "string"){
        return null
    }
    else
    {
        return s1 + s2;
    }
}