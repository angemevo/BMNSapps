const carouselImages = document.querySelector('.carousel-images');
const images = document.querySelectorAll('.carousel-images img');

let currentIndex = 0;
const totalImages = images.length;
const intervalTime = 3000; // Temps entre chaque changement d'image (en millisecondes)

function nextImage() {
  currentIndex = (currentIndex + 1) % totalImages;
  updateCarousel();
}

function updateCarousel() {
  carouselImages.style.transform = `translateX(-${currentIndex * 100}%)`;
}

// Démarre le carousel automatique
function startCarousel() {
  setInterval(nextImage, intervalTime);
}

// Affiche la première image au démarrage
updateCarousel();

// Démarre le carousel automatique
startCarousel();
