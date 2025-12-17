// MENÚ RESPONSIVE
const menuBtn = document.getElementById('menuBtn');
const navLinks = document.getElementById('navLinks');


menuBtn.addEventListener('click', () => {
navLinks.classList.toggle('active');
});


// PROYECTOS DESDE ARRAY
const projects = [
{ title: 'Landing Page', description: 'HTML y CSS puro' },
{ title: 'Formulario', description: 'Validación con JavaScript' },
{ title: 'Modal', description: 'Interacción dinámica' }
];


const container = document.getElementById('projectContainer');


projects.forEach(project => {
const card = document.createElement('div');
card.className = 'card';
card.innerHTML = `<h3>${project.title}</h3><p>${project.description}</p>`;
container.appendChild(card);
});


// MODAL
const modal = document.getElementById('modal');
const openModal = document.getElementById('openModal');
const closeModal = document.getElementById('closeModal');


openModal.onclick = () => modal.style.display = 'flex';
closeModal.onclick = () => modal.style.display = 'none';


// FORMULARIO
const form = document.getElementById('contactForm');
const status = document.getElementById('formStatus');


form.addEventListener('submit', e => {
e.preventDefault();
status.textContent = 'Formulario enviado correctamente';
form.reset();
});