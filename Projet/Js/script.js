// variable global
let compteur=0//pour trour l'image

let timer,elements,slides,slideswidth,speed;
window.onload=()=>{
    // on recupere le diapo
    const diapo=document.querySelector(".diapo");
    elements=document.querySelector(".elements");

    // on recupere le data speed
    speed=diapo.dataset.speed;
    //on clone la premiere image
    let firstImage=elements.firstElementChild.cloneNode(true);

    // on injecte le clone a la fin du diapo

    elements.appendChild(firstImage);

    slides=Array.from(elements.children);

    // on recupere la largeur d'une slides
    slideswidth=diapo.getBoundingClientRect().width;
 
 // les fleche

 let next=document.querySelector(".plus");
let prev =document.querySelector(".moins");
 // on gere le clic
 next.addEventListener("click",slideNext);
 prev.addEventListener("click",slidePrev);

 // automatiser un peu le defilement
//  timer=setInterval(slideNext,2000);
}
/**
 * Cette fonction faire defiler vers la droite */ 
function slideNext(){
    // incrementer le compteur
    compteur++;
    //pour la transition
    elements.style.transition="1s linear";

    let decal= -slideswidth*compteur;
elements.style.transform=`translateX(${decal}px)`;

// on attend la fin de la transition et on rembobine de facon caher
setTimeout(function()
{
    if(compteur >= slides.length -1){
        compteur=0;
        elements.style.transition= "unset";
        elements.style.transform="translateX(0)";
    }
},1000);
} 
//cette fonctionfaire defiler le diapo vers la gauchw
function slidePrev(){
// on decremente le compteur
compteur--;
elements.style.transition="1s linear";
  if(compteur<0){
    compteur=slides.length-1;
    let decal=-slideswidth*compteur;
    elements.style.transition= "unset";
  elements.style.transform="translateX(0)";
  elements.style.transform=`translateX(${decal}px)`;
 setTimeout(slidePrev(),1);
  } 
  let decal=-slideswidth*compteur;
  elements.style.transform=`translateX(${decal}px)`;

 }

