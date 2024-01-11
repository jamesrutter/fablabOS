document.addEventListener('DOMContentLoaded', (event) => {
  let slideIndex = 0;
  const slides = [
    'assets/images/image1.jpg',
    'assets/images/image2.jpg',
    'assets/images/image3.jpg',
    // ...add paths to all images you have
  ];

  const showSlides = () => {
    let i;
    const slideshowDiv = document.getElementById('slideshow');
    for (i = 0; i < slides.length; i++) {
      slides[i].style.display = 'none';
    }
    slideIndex++;
    if (slideIndex > slides.length) {
      slideIndex = 1;
    }
    const img = document.createElement('img');
    img.src = slides[slideIndex - 1];
    img.style.display = 'block';
    img.className = 'fade';
    slideshowDiv.innerHTML = '';
    slideshowDiv.appendChild(img);
    setTimeout(showSlides, 4000); // Change image every 4 seconds
  };

  showSlides();
});
