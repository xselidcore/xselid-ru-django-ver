function updateFooterClock() {
    const now = new Date();
    const day = String(now.getDate()).padStart(2, '0');
    const month = String(now.getMonth() + 1).padStart(2, '0');
    const year = String(now.getFullYear()).slice(-2);
    const hours = String(now.getHours()).padStart(2, '0');
    const minutes = String(now.getMinutes()).padStart(2, '0');
    const seconds = String(now.getSeconds()).padStart(2, '0');

    const formatted = `${day}.${month}.${year} - ${hours}:${minutes}:${seconds}`;
    document.getElementById("footer-clock").textContent = formatted;
}

updateFooterClock();
setInterval(updateFooterClock, 1000);






const text = "Мы активно разрабатываем сайт:";
let index = 0;
const typingElem = document.getElementById("typing");
const cursor = document.querySelector(".cursor");

function type() {
    if (index < text.length) {
        typingElem.textContent += text[index];
        index++;
        setTimeout(type, 50);
    } else {
        cursor.style.display = "none";
    }
}

type();


