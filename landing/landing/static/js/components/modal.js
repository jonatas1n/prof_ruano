const closeModal = modalSelector => {
    const modal = document.querySelector(modalSelector);
    modal.classList.remove('active');
    document.body.classList.remove('modal-active');
}

const openModal = modalSelector => {
    const modal = document.querySelector(modalSelector);
    modal.classList.add('active');
    document.body.classList.add('modal-active');
}

const toggleModal = modalSelector => {
    const modal = document.querySelector(modalSelector);
    modal.classList.toggle('active');
    document.body.classList.toggle('modal-active');
}
