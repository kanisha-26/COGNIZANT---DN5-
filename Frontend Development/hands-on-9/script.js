const cards = document.querySelectorAll(".course-card");

cards.forEach(function(card){

card.addEventListener("click",function(){

alert("Course Selected");

});

card.addEventListener("keydown",function(event){

if(event.key==="Enter"){

event.preventDefault();

alert("Course Selected");

}

});

});