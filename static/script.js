// script.js

// Cursor Effect
const cursor = document.createElement('div');
cursor.classList.add('cursor-effect');
document.body.appendChild(cursor);

document.addEventListener('mousemove', (e) => {
    cursor.style.left = `${e.pageX}px`;
    cursor.style.top = `${e.pageY}px`;
    cursor.classList.remove('burst');
});

document.addEventListener('click', () => {
    cursor.classList.add('burst');
    setTimeout(() => cursor.classList.remove('burst'), 500);
});

// Firefly Animation
const fireflies = [];
const numFireflies = 50;

for (let i = 0; i < numFireflies; i++) {
    const firefly = document.createElement('div');
    firefly.classList.add('firefly');
    firefly.style.left = `${Math.random() * 100}vw`;
    firefly.style.top = `${Math.random() * 100}vh`;
    firefly.style.animationDuration = `${5 + Math.random() * 10}s`;
    firefly.style.animationDelay = `${Math.random() * 5}s`;
    firefly.style.animationName = 'firefly-move';
    fireflies.push(firefly);
    document.body.appendChild(firefly);
}

const styleTag = document.createElement('style');
styleTag.innerHTML = `
    @keyframes firefly-move {
        0% { transform: translateY(0); }
        50% { transform: translateY(-50px); }
        100% { transform: translateY(0); }
    }
    .firefly {
        position: fixed;
        width: 10px;
        height: 10px;
        border-radius: 50%;
        background: rgba(255, 255, 153, 0.8);
        box-shadow: 0 0 10px rgba(255, 255, 153, 0.8);
        z-index: 1;
    }
`;
document.head.appendChild(styleTag);


// script.js

// Generate Fireflies
const createFireflies = (num) => {
    for (let i = 0; i < num; i++) {
        const firefly = document.createElement('div');
        firefly.classList.add('firefly');
        firefly.style.left = `${Math.random() * 100}vw`;
        firefly.style.top = `${Math.random() * 100}vh`;
        firefly.style.animationDuration = `${5 + Math.random() * 10}s`;
        document.body.appendChild(firefly);
    }
};

// Add Fireflies
createFireflies(50);

// Cursor Effect
const cursor = document.createElement('div');
cursor.classList.add('cursor-effect');
document.body.appendChild(cursor);

document.addEventListener('mousemove', (e) => {
    cursor.style.left = `${e.pageX}px`;
    cursor.style.top = `${e.pageY}px`;
    cursor.classList.remove('burst');
});

document.addEventListener('click', () => {
    cursor.classList.add('burst');
    setTimeout(() => cursor.classList.remove('burst'), 500);
});
