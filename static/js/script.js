// List of background image URLs from the static folder
const backgrounds = [
    "url('/static/images/bg.jpg')", 
    "url('/static/images/bg1.jpg')", 
    "url('/static/images/bg2.jpg')",
    "url('/static/images/bg3.jpg')",
    "url('/static/images/bg4.jpeg')", 
    "url('/static/images/bg5.jpg')",
    "url('/static/images/bg6.png')",
    "url('/static/images/bg7.jpg')",
    "url('/static/images/bg8.jpg')"
];

let currentBackground = 0;

// Function to change the background
function changeBackground() {
    // Set the background image, size, and position to ensure it covers the entire screen
    document.body.style.backgroundImage = backgrounds[currentBackground];
    document.body.style.backgroundSize = 'cover';  // Ensures the background covers the entire viewport
    document.body.style.backgroundPosition = 'center center';  // Ensures the background is centered
    document.body.style.backgroundAttachment = 'fixed';  // Makes the background fixed while scrolling
    currentBackground = (currentBackground + 1) % backgrounds.length;
}

// Initial background change
changeBackground();

// Change the background every 25 seconds (25000 milliseconds)
setInterval(changeBackground, 8000);
