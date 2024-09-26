const counterElement = document.querySelector('.counter');
const counterDisplay = counterElement.querySelector('.counter__display');

function startCounter(remainingTimeSeconds) {
  const duration = counterElement.getAttribute('data-duration');
  const start = counterElement.getAttribute('data-start');
  const nowTime = new Date().getTime();

  const interval = setInterval(() => {
    // Calculate the time remaining
    const formattedTime = new Date().getTime() - nowTime;
    const currentCount = start + Math.floor((formattedTime / 1000));
    counterDisplay.textContent = currentCount;

    if (currentCount >= start) {
      clearInterval(interval);
      counterDisplay.textContent = start;
    }
  }, 1000);

  return interval;
};


console.log