const statsBoard = document.querySelector('.stats__board');
const timeHideElem = document.querySelector('.time__hide');
const gradeHideElem = document.querySelector('.grade__hide');
const subjectsHideElem = document.querySelector('.subjects__hide');

const timeTitle = document.querySelector('.time .stats__item__title');
const gradeTitle = document.querySelector('.grade .stats__item__title');
const subjectsTitle = document.querySelector('.subjects .stats__item__title');

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
  changeTitles(false);
  timeHideElem.innerHTML = '';
  gradeHideElem.innerHTML = '';
  subjectsHideElem.innerHTML = '';
}

function changeTitles(selected=true) {
  if (selected) {
    timeTitle.innerHTML = 'Tempo de prova';
    gradeTitle.innerHTML = 'Porcentagem de acertos';
    subjectsTitle.innerHTML = 'Assuntos da prova';
    return;
  }
  timeTitle.innerHTML = 'Tempo médio';
  gradeTitle.innerHTML = '% de acertos';
  subjectsTitle.innerHTML = 'Assuntos mais errados';
}

function setListData(time, corrects, subjects) {
  clearListData();
  changeTitles();
  timeHideElem.innerHTML = time;
  gradeHideElem.innerHTML = corrects;
  subjectsHideElem.innerHTML = subjects;
}

function getListData(listID) { 
  $.ajax({
    type: 'GET',
    url: `listas/submission/${listID}/`,
    success: function(data) {
      const { time, corrects, subjects } = data;
      setListData(time, corrects, subjects);
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
