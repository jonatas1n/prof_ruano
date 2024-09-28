const counterElement = document.querySelector('.counter');
const counterDisplay = counterElement.querySelector('.counter__display');


function formatSeconds(seconds) {
  const hours = Math.floor(seconds / 3600);
  const minutes = Math.floor((seconds % 3600) / 60);
  const remainingSeconds = seconds % 60;
  return `${hours}h${minutes}m${remainingSeconds}`;
}

function startCounter(remainingTimeSeconds) {
  let remainingTime = remainingTimeSeconds;
  const intervalId = setInterval(() => {
    if (remainingTime <= 0) {
      clearInterval(intervalId);
      return;
    }
    remainingTime -= 1;
    counterDisplay.textContent = formatSeconds(remainingTime);
  }, 1000);
};
