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
            const showcaseSwiper = new Swiper(".showcase-3d-swiper", {
                effect: "fade",
                fadeEffect: {
                    crossFade: true
                },
                loop: true,
                speed: 600,
                autoplay: {
                    delay: 5500,
                    disableOnInteraction: false,
                    pauseOnMouseEnter: true,
                },
                pagination: {
                    el: ".swiper-pagination-3d",
                    clickable: true,
                },
                navigation: {
                    nextEl: ".swiper-button-next-3d",
                    prevEl: ".swiper-button-prev-3d",
                },
                on: {
                    slideChange: function () {
                        const realIndex = this.realIndex;
                        const tabs = document.querySelectorAll(".showcase-tab-btn");
                        tabs.forEach((tab, idx) => {
                            if (idx === realIndex) {
                                tab.classList.add("active");
                            } else {
                                tab.classList.remove("active");
                            }
                        });
                        const counter = document.getElementById("showcaseSlideCounter");
                        if (counter) {
                            counter.innerText = `0${realIndex + 1} / 07`;
                        }
                    }
                }
            });

            // Interactive domain tab click listeners
            document.querySelectorAll(".showcase-tab-btn").forEach((btn, idx) => {
                btn.addEventListener("click", function () {
                    showcaseSwiper.slideToLoop(idx);
                });
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
