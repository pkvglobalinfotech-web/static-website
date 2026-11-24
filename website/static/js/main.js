// Counter Animation (null-safe)
document.addEventListener("DOMContentLoaded", function () {
    const counters = document.querySelectorAll(".counter");
    if (counters.length > 0) {
        counters.forEach(counter => {
            let target = parseInt(counter.innerText) || 0;
            let value = 0;
            if (target > 0) {
                let interval = setInterval(() => {
                    value++;
                    counter.innerText = value;
                    if (value >= target) {
                        clearInterval(interval);
                    }
                }, 30);
            }
        });
    }

    // Scroll-to-Top Button (null-safe)
    const topBtn = document.getElementById("topBtn");
    if (topBtn) {
        window.addEventListener("scroll", function () {
            if (window.scrollY > 300) {
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
    }

    // AOS Animation Guard
    if (typeof AOS !== "undefined") {
        AOS.init({
            duration: 800,
            once: true
        });
    }

    // Swiper Guard
    if (typeof Swiper !== "undefined") {
        if (document.querySelector(".swiper")) {
            new Swiper(".swiper", {
                slidesPerView: 3,
                spaceBetween: 20,
                autoplay: {
                    delay: 2000
                }
            });
        }

        if (document.querySelector(".testimonialSwiper")) {
            new Swiper(".testimonialSwiper", {
                slidesPerView: 3,
                spaceBetween: 30,
                loop: true,
                autoplay: {
                    delay: 3000,
                    disableOnInteraction: false
                },
                pagination: {
                    el: ".swiper-pagination",
                    clickable: true
                },
                breakpoints: {
                    0: { slidesPerView: 1 },
                    768: { slidesPerView: 2 },
                    992: { slidesPerView: 3 }
                }
            });
        }
    }
});
