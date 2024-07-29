const counterElement = document.querySelector('.counter');
const counterDisplay = counterElement.querySelector('.counter__display');

function startCounter() {
  const duration = counterElement.getAttribute('data-duration');
  const start = counterElement.getAttribute('data-start');
  const nowTime = new Date().getTime();

  const interval = setInterval(() => {
    const currentTime = new Date().getTime();
    const elapsedTime = currentTime - nowTime;
    const progress = elapsedTime / duration;
    const currentCount = Math.floor(progress * start);

    counterDisplay.textContent = currentCount;

    if (currentCount >= start) {
      clearInterval(interval);
      counterDisplay.textContent = start;
    }
  }, 1000);

  return interval;
};


console.log