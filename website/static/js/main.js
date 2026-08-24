    const counters=document.querySelectorAll(".counter");


counters.forEach(counter=>{


let value=0;


let target=parseInt(counter.innerText);



let interval=setInterval(()=>{


value++;


counter.innerText=value;



if(value==target)

{

clearInterval(interval);

}



},30);



});

AOS.init({
    duration:1000,
    once:true
});

new Swiper(".swiper",
{

slidesPerView:3,

spaceBetween:20,


autoplay:
{

delay:2000

}


});

window.onscroll = function () {
    document.getElementById("topBtn").style.display =
        window.scrollY > 300 ? "block" : "none";
};

document.getElementById("topBtn").onclick = function () {
    window.scrollTo({
        top: 0,
        behavior: "smooth"
    });
};

const topBtn = document.getElementById("topBtn");

window.addEventListener("scroll", function () {
    if (window.pageYOffset > 300) {
        topBtn.style.display = "block";
    } else {
        topBtn.style.display = "none";
    }
});

topBtn.addEventListener("click", function () {
    window.scrollTo({
        top: 0,
        behavior: "smooth"
    });
});

new Swiper(".testimonialSwiper", {
    slidesPerView: 3,
    spaceBetween: 30,
    loop: true,

    autoplay: {
        delay: 3000,
        disableOnInteraction: false,
    },

    pagination: {
        el: ".swiper-pagination",
        clickable: true,
    },

    breakpoints: {
        0: {
            slidesPerView: 1,
        },
        768: {
            slidesPerView: 2,
        },
        992: {
            slidesPerView: 3,
        }
    }
});