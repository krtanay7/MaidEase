// JavaScript to toggle the content display
document.querySelector('.read-more-btn').addEventListener('click', function () {
    var content = document.querySelector('.content');
    if (content.style.display === 'none') {
        content.style.display = 'block';
        this.textContent = 'Read Less'; // Change button text to "Read Less"
    } else {
        content.style.display = 'none';
        this.textContent = 'Read More'; // Change button text back to "Read More"
    }
});

window.onscroll = function() {
if (document.body.scrollTop > 100 || document.documentElement.scrollTop > 100) {
    scrollToTopBtn.style.display = "block"; // Show button
} else {
    scrollToTopBtn.style.display = "none"; // Hide button
}
};

// Scroll to top when button is clicked
scrollToTopBtn.addEventListener("click", function() {
window.scrollTo({
    top: 0,
    behavior: "smooth" // Smooth scroll
});
})

// reveiws


var swiper = new Swiper(".review-slider", {
spaceBetween: 20,
loop:true,
autoplay: {
delay: 2500,
disableOnInteraction: false,
},
breakpoints: {
640: {
  slidesPerView: 1,
},
768: {
  slidesPerView: 2,
},
1024: {
  slidesPerView: 3,
},
},
});