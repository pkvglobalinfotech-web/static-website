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
        if (document.querySelector(".showcase-3d-swiper")) {
            new Swiper(".showcase-3d-swiper", {
                effect: "coverflow",
                grabCursor: true,
                centeredSlides: true,
                slidesPerView: "auto",
                spaceBetween: 30,
                loop: true,
                speed: 750,
                autoplay: {
                    delay: 5000,
                    disableOnInteraction: false,
                    pauseOnMouseEnter: true,
                },
                coverflowEffect: {
                    rotate: 15,
                    stretch: 0,
                    depth: 220,
                    modifier: 1,
                    slideShadows: true,
                },
                pagination: {
                    el: ".swiper-pagination-3d",
                    clickable: true,
                    dynamicBullets: true,
                },
                navigation: {
                    nextEl: ".swiper-button-next-3d",
                    prevEl: ".swiper-button-prev-3d",
                },
                breakpoints: {
                    320: {
                        slidesPerView: 1,
                        coverflowEffect: { rotate: 0, depth: 80 },
                    },
                    768: {
                        slidesPerView: 1.15,
                        coverflowEffect: { rotate: 10, depth: 160 },
                    },
                    1200: {
                        slidesPerView: 1.25,
                        coverflowEffect: { rotate: 15, depth: 220 },
                    },
                },
            });
        }

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

    // Prevent multiple simultaneous form submissions
    const enquiryForm = document.getElementById("enquiryForm");
    const submitBtn = document.getElementById("submitEnquiryBtn");
    if (enquiryForm && submitBtn) {
        enquiryForm.addEventListener("submit", function (e) {
            if (submitBtn.classList.contains("submitting")) {
                e.preventDefault();
                return false;
            }
            submitBtn.classList.add("submitting");
            submitBtn.style.pointerEvents = "none";
            submitBtn.style.opacity = "0.7";
            submitBtn.innerHTML = '<span class="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>Submitting...';
            setTimeout(function () {
                submitBtn.disabled = true;
            }, 50);
        });
    }
});
