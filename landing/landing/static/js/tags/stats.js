const statsBoard = document.querySelector('.stats__board');
const timeHideElem = document.querySelector('.time__hide');
const gradeHideElem = document.querySelector('.grade__hide');

function activeBoard() {
  statsBoard.classList.add('marked');
}

function deactivateBoard() {
  statsBoard.classList.remove('marked');
  clearListData();
}

function clearLists() {
  const lists = document.querySelectorAll('li.list');
  lists.forEach(list => list.classList.remove('selected'));
}

function clearListData() {
  timeHideElem.innerHTML = '';
  gradeHideElem.innerHTML = '';
}

function setListData(time, corrects) {
  clearListData();
  timeHideElem.innerHTML = time;
  gradeHideElem.innerHTML = corrects;
}

function getListData(listID) { 
  $.ajax({
    type: 'GET',
    url: `listas/submission/${listID}/`,
    success: function(data) {
      const { time, corrects } = data;
      setListData(time, corrects);
    },
    error: function(error) {
      console.log(error);
    }
  });
}

function markList(listID) {
  const list = document.getElementById(`list-item-${listID}`);

  if (list.classList.contains('selected')) {
    list.classList.remove('selected');
    deactivateBoard();
    return;
  }

  clearLists();
  getListData(listID);
  activeBoard();
  list.classList.add('selected');
}
