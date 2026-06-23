const techChat = document.querySelector('.tech-chat');
const techToggle = document.querySelector('.tech-chat-toggle');
const techClose = document.querySelector('.tech-close');
const techForm = document.getElementById('techChatForm');
const techInput = document.getElementById('techInput');
const catalogForm = document.getElementById('catalogSearchForm');
const clearSearch = document.getElementById('clearSearch');
const resultsGrid = document.getElementById('resultsGrid');
const resultsCount = document.getElementById('resultsCount');
const recommendedPrev = document.getElementById('recommendedPrev');
const recommendedNext = document.getElementById('recommendedNext');
const recommendedDots = document.getElementById('recommendedDots');
let recommendedPage = 0;
let carouselPage = 0;
let carouselTimer;
const categorySelect = catalogForm?.elements.categoria;
const categoryNames = [];
const techState = {
    lastBooks: [],
    lastQuery: {}
};
const carousel = document.querySelector('.categories-grid');
const carouselCards = Array.from(document.querySelectorAll('.cat-card'));
const prevCarousel = document.querySelector('.books-arrow-left');
const nextCarousel = document.querySelector('.books-arrow-right');
const carouselDots = document.querySelector('.books-dots');

const techReplyTemplates = {
    horario: [
        '¡Genial! Nuestro horario es lunes a viernes de 8:00 a.m. a 6:00 p.m., y sábados de 9:00 a.m. a 1:00 p.m.',
        'Abrimos de lunes a viernes de 8:00 a.m. a 6:00 p.m. y también los sábados de 9:00 a.m. a 1:00 p.m.',
        'Estoy disponible para ayudarte con horarios: de lunes a viernes 8:00–18:00 y sábados 9:00–13:00.'
    ],
    catalogo: [
        'Puedes buscar libros, autores y temas desde el buscador principal. Si quieres, te recomiendo alguno según categoría o autor.',
        'El catálogo está listo para ti. Pide un autor, una categoría o una idea de lectura y te sugiero libros.'
    ],
    ubicacion: [
        'Bibliotech es un espacio físico y digital. Si necesitas ubicación exacta, revisa la página de contacto o escribe a contacto@bibliotech.edu.co.',
        'Estamos en la biblioteca principal de la institución. Para más detalles, consulta contacto@bibliotech.edu.co.'
    ],
    registro: [
        'Puedes registrarte desde el botón de inicio de sesión. Si ya tienes cuenta, ingresa con tu usuario y contraseña.',
        'Si no estás registrado, ve a la sección de usuario y completa el formulario para crear tu cuenta.'
    ],
    tarjeta: [
        'Para usar la biblioteca en persona necesitas la tarjeta de usuario. Pregunta en atención si aún no la tienes.',
        'La tarjeta de biblioteca te permite pedir préstamos y acceder a servicios especiales. Solicítala en el punto de atención.'
    ],
    renovacion: [
        'Si necesitas renovar un préstamo, pregunta en la biblioteca o revisa el estado en tu cuenta de usuario.',
        'La renovación depende de la disponibilidad del libro, así que consulta en la biblioteca para extender tu préstamo.'
    ],
    devolucion: [
        'Devuelve los libros en el punto de atención antes de la fecha de entrega para evitar multas.',
        'Puedes devolver tu libro en recepción o en el buzón de devoluciones según el horario de la biblioteca.'
    ],
    sancion: [
        'Las multas se aplican cuando un libro se entrega tarde. Consulta el monto exacto en recepción.',
        'Si tienes sanción, habla con el personal de la biblioteca para conocer el plazo y el valor de la multa.'
    ],
    servicios: [
        'Ofrecemos préstamo de libros, salas de estudio, consultoría de investigación y acceso a recursos digitales.',
        'La biblioteca cuenta con servicios de préstamo, apoyo académico, internet y acceso a material digital.'
    ],
    digital: [
        'También puedes acceder a contenido digital desde nuestra plataforma si eres usuario registrado.',
        'Hay recursos digitales disponibles para miembros registrados: libros, artículos y guías en línea.'
    ],
    eventos: [
        'Regularmente hacemos talleres y actividades culturales. Pregunta en atención para conocer la agenda.',
        'La biblioteca organiza eventos y charlas. Mantente atento a las noticias o consulta en el punto de atención.'
    ],
    ayuda: [
        'Claro, dime qué tipo de libro te gustaría leer y te hago unas recomendaciones.',
        'Puedo sugerirte libros por categoría, autor o tema. ¿Qué te apetece leer hoy?'
    ],
    contacto: [
        'Puedes escribirnos a contacto@bibliotech.edu.co. Estoy aquí para ayudarte con cualquier duda.',
        'Nuestro correo es contacto@bibliotech.edu.co. Escríbenos si necesitas soporte o información adicional.'
    ],
    saludo: [
        '¡Hola! Soy Tech, tu asistente de Bibliotech. ¿En qué te puedo ayudar hoy?',
        '¡Hola! ¿Quieres recomendaciones de lectura o información sobre la biblioteca?'    ],
    gracias: [
        '¡Con gusto! Si necesitas algo más, estoy aquí para ayudarte.',
        'Gracias a ti. Dime si quieres otra recomendación o información de la biblioteca.'
    ],
    despedida: [
        'Hasta luego, que tengas un buen día. Vuelve cuando quieras para más recomendaciones.',
        'Nos vemos pronto. Cuando quieras, te ayudo con más libros o información de la biblioteca.'
    ],
    default: [
        'Hola, soy Tech. Puedo ayudarte con horarios, catálogo, préstamos, contacto y recomendaciones de libros.',
        '¡Hola! Pregúntame por libros recomendados, categorías disponibles, horarios o contacto.'
    ],
    noResults: [
        'No encontré nada con esos datos, ¿quieres que pruebe con otra categoría, autor o palabra clave?',
        'Lo siento, no pude encontrar libros con esa búsqueda. Dime otra idea y lo intento de nuevo.'
    ]
};

function randomChoice(items) {
    return items[Math.floor(Math.random() * items.length)];
}

function normalize(text) {
    // Preserve 'ñ' by only stripping specific accent marks (excluding the tilde for ñ)
    return (text || '')
        .toLowerCase()
        .normalize('NFD')
        .replace(/[\u0300-\u0302\u0304-\u036f]/g, "") // Mantener \u0303 (tilde de la ñ)
        .normalize('NFC');
}

function getBookCategoryFromMessage(message) {
    const normalized = normalize(message);
    return categoryNames.find((name) => normalized.includes(normalize(name)));
}

function getBookAuthorFromMessage(message) {
    const normalized = normalize(message);
    // Mejora: Solo capturar si viene precedido de 'por' o si el mensaje es explícitamente 'buscar por autor <autor>'
    // Evitamos capturar 'de <Libro>' que suele ser el título
    const authorMatch = normalized.match(/(?:escrito por|de la autoría de|del autor|por) ([a-z\sáéíóúñü]{3,})/) 
                      || normalized.match(/^buscar por autor ([a-z\sáéíóúñü]{3,})$/);
    
    if (authorMatch) {
        const potential = authorMatch[1].trim();
        // Evitar capturar palabras comunes que suelen no ser autores solos
        if (['soledad', 'la', 'el', 'los', 'un', 'una'].includes(potential)) return '';
        return potential;
    }
    return '';
}

function getBookTopicFromMessage(message) {
    const normalized = normalize(message);
    // Intentar capturar el tema después de palabras clave comunes
    const topicMatch = normalized.match(/(?:de la categoria|de la categor[ií]a|de categoria|de categor[ií]a|sobre|acerca de) ([a-z\sáéíóúñü\d\s]{3,})/);
    if (topicMatch) {
        let topic = topicMatch[1].trim();
        return topic.replace(/^(un|una|el|la)\s+/, '').trim();
    }
    // Si no hay frases de 'categoria/sobre', pero es una recomendacion, 
    // podria ser directamente el nombre del libro despues de 'recomiendame'
    const recMatch = normalized.match(/(?:recomiendame|sugiereme|busca|quiero leer) ([a-z\sáéíóúñü\d\s]{3,})/);
    if (recMatch) {
        return recMatch[1].trim();
    }
    return '';
}

function mapTopicToCategory(topic) {
    if (!topic) return '';
    const normalizedTopic = normalize(topic);
    return categoryNames.find((name) => {
        const normalizedName = normalize(name);
        return normalizedName.includes(normalizedTopic) || normalizedTopic.includes(normalizedName);
    }) || '';
}

function isRecommendationRequest(message) {
    return /recomiend|sugier|propone|quiero.*libro|busca.*libro|dame.*libro|necesito.*libro|tengo ganas de leer/i.test(message);
}

function isCategoryRequest(message) {
    return /categor[ií]as?|g[eé]neros?|temas?|tipos?/i.test(message);
}

function isNewBookRequest(message) {
    return /novedad|nuevo|nuevos libros|estreno|ultim[oa]s adquisiciones/i.test(message);
}

function isWhyRequest(message) {
    return /por ?que|porque|por qué|por que/i.test(message) && /recomend|suger|buscar|libro|ese|esta|esto/i.test(message);
}

function getRecommendationReason(libro) {
    if (!libro) return 'Te recomiendo este libro porque coincide con lo que me pediste y está disponible en nuestro catálogo.';

    const reasons = [];
    if (techState.lastQuery.categoria) {
        reasons.push(`pertenece a la categoría "${techState.lastQuery.categoria}" que solicitaste`);
    }
    if (techState.lastQuery.autor) {
        reasons.push(`coincide con el autor ${techState.lastQuery.autor}`);
    }
    if (techState.lastQuery.q && !techState.lastQuery.categoria && !techState.lastQuery.autor) {
        reasons.push(`coincide con tu búsqueda de "${techState.lastQuery.q}"`);
    }

    if (reasons.length === 0) {
        reasons.push('es una opción disponible en nuestro catálogo y tiene buena recepción entre los lectores');
    }

    const availability = Number(libro.ejemplares_disponibles || 0) > 0
        ? 'Además, tiene ejemplares disponibles para préstamo.'
        : 'Lo recomiendo porque está presente en nuestra colección y suele interesar a muchos lectores.';

    let reason = `Lo elegí porque ${reasons.join(' y ')}.`;
    if (libro.materia && !techState.lastQuery.categoria) {
        reason += ` Pertenece a la categoría "${libro.materia}", que es relevante para ese interés.`;
    }
    if (libro.autor && !techState.lastQuery.autor) {
        reason += ` ${libro.autor} es un autor muy valorado en esta área.`;
    }
    reason += ` ${availability}`;
    return reason;
}

function buildTechBookList(libros) {
    return libros.slice(0, 3).map((libro, index) => {
        const title = libro.titulo || 'Título desconocido';
        const author = libro.autor || 'Autor desconocido';
        const category = libro.materia || 'General';
        return `${index + 1}. ${title} — ${author} (${category})`;
    }).join('\n');
}

function buildTechBookRecommendation(libro) {
    if (!libro) return 'Lo siento, no tengo una recomendación específica ahora mismo.';
    const title = libro.titulo || 'un libro interesante';
    const author = libro.autor ? ` de ${libro.autor}` : '';
    const category = libro.materia ? ` en la categoría ${libro.materia}` : '';
    return `Te sugiero especialmente "${title}"${author}${category}.`;
}

function setSearchValues(values = {}) {
    if (!catalogForm) return;
    catalogForm.reset();
    if (values.q) catalogForm.elements.q.value = values.q;
    if (values.titulo) catalogForm.elements.titulo.value = values.titulo;
    if (values.autor) catalogForm.elements.autor.value = values.autor;
    if (values.categoria) catalogForm.elements.categoria.value = values.categoria;
    if (values.editorial) catalogForm.elements.editorial.value = values.editorial;
    if (values.anio) catalogForm.elements.anio.value = values.anio;
}

function parseTechIntent(message) {
    const normalized = normalize(message);
    if (isWhyRequest(normalized)) {
        return { type: 'why' };
    }
    if (isCategoryRequest(normalized)) {
        return { type: 'categories' };
    }

    const category = getBookCategoryFromMessage(normalized);
    const author = getBookAuthorFromMessage(normalized);
    const topic = getBookTopicFromMessage(message);
    if (isRecommendationRequest(normalized) || isNewBookRequest(normalized)) {
        return { type: 'recommendation', category, author, topic };
    }

    if (/buscar|encuentra|mostrar|ver|busca|quiero.*leer|leer/i.test(normalized)) {
        return { type: 'search', category, author, topic, query: normalized };
    }

    return { type: 'general' };
}

async function getBooksForTech(params = {}) {
    const query = new URLSearchParams();
    if (params.categoria) query.append('categoria', params.categoria);
    if (params.autor) query.append('autor', params.autor);
    if (params.q) query.append('q', params.q);

    const response = await fetch(`/api/books/?${query.toString()}`);
    const data = await response.json();
    return data.libros || [];
}

function getTechFallbackReply(message) {
    const text = normalize(message);
    const keys = Object.keys(techReplyTemplates).filter((item) => item !== 'default' && item !== 'noResults');
    const matchedKey = keys.find((item) => text.includes(item));

    if (matchedKey) {
        return randomChoice(techReplyTemplates[matchedKey]);
    }

    if (/hola|buenos|buenas|saludos/i.test(message)) {
        return randomChoice(techReplyTemplates.saludo);
    }
    if (/gracias|muchas gracias|thank/i.test(message)) {
        return randomChoice(techReplyTemplates.gracias);
    }
    if (/adios|nos vemos|hasta luego|chao|bye/i.test(message)) {
        return randomChoice(techReplyTemplates.despedida);
    }

    return randomChoice(techReplyTemplates.default);
}

function getTechNoResultReply() {
    return randomChoice(techReplyTemplates.noResults);
}

// Elementos del chat de soporte (Tech Chat)
const techMessages = document.getElementById('techMessages');
const techSuggestions = document.getElementById('techSuggestions');

function getRecommendedVisible() {
    if (window.matchMedia('(max-width: 768px)').matches) return 1;
    if (window.matchMedia('(max-width: 1024px)').matches) return 2;
    if (window.matchMedia('(max-width: 1400px)').matches) return 3;
    return 4; 
}

function renderRecommendedCarousel() {
    if (!resultsGrid) return;

    // Hacemos el contenedor más ancho para que la sección sea más imponente
    if (resultsGrid.parentElement) {
        resultsGrid.parentElement.style.maxWidth = '1600px';
        resultsGrid.parentElement.style.width = '98%';
        resultsGrid.parentElement.style.margin = '0 auto';
    }

    // Configuramos el contenedor para permitir el desplazamiento horizontal suave
    resultsGrid.style.display = 'flex';
    resultsGrid.style.flexWrap = 'nowrap';
    const gap = 24;
    resultsGrid.style.gap = `${gap}px`;
    resultsGrid.style.padding = '30px 10px';
    resultsGrid.style.transition = 'transform 0.8s cubic-bezier(0.165, 0.84, 0.44, 1)';
    resultsGrid.style.width = 'fit-content';

    const cards = Array.from(resultsGrid.querySelectorAll('.result-card'));
    if (cards.length === 0) {
        resultsGrid.style.transform = 'translateX(0)';
        return;
    }

    const visibleCards = getRecommendedVisible();
    const pages = Math.max(Math.ceil(cards.length / visibleCards), 1);
    recommendedPage = (recommendedPage + pages) % pages;

    const containerWidth = resultsGrid.parentElement?.offsetWidth || resultsGrid.offsetWidth;
    const cardWidth = (containerWidth - (gap * (visibleCards - 1))) / visibleCards;

    cards.forEach((card, index) => {
        card.classList.remove('is-hidden'); 
        card.style.flex = `0 0 ${cardWidth}px`;
        card.style.maxWidth = `${cardWidth}px`;
        card.style.height = 'auto';
    });

    const scrollOffset = recommendedPage * (containerWidth + gap);
    resultsGrid.style.transform = `translateX(-${scrollOffset}px)`;
    resultsGrid.style.justifyContent = cards.length < visibleCards ? 'center' : 'flex-start';

    const showControls = cards.length > visibleCards;
    
    if (recommendedPrev) recommendedPrev.classList.toggle('is-hidden', !showControls);
    if (recommendedNext) recommendedNext.classList.toggle('is-hidden', !showControls);

    if (recommendedDots) {
        recommendedDots.innerHTML = '';
        if (showControls) {
            for (let index = 0; index < pages; index += 1) {
                const dot = document.createElement('span');
                dot.className = index === recommendedPage ? 'active' : '';
                dot.addEventListener('click', () => {
                    recommendedPage = index;
                    renderRecommendedCarousel();
                });
                recommendedDots.appendChild(dot);
            }
            recommendedDots.classList.remove('is-hidden');
        } else {
            recommendedDots.classList.add('is-hidden');
        }
    }
}

function getVisibleCards() {
    return window.matchMedia('(max-width: 560px)').matches ? 1 : window.matchMedia('(max-width: 900px)').matches ? 2 : 5;
}

function renderCarousel() {
    const visibleCards = getVisibleCards();
    const pages = Math.max(Math.ceil(carouselCards.length / visibleCards), 1);
    carouselPage = (carouselPage + pages) % pages;

    carouselCards.forEach((card, index) => {
        const start = carouselPage * visibleCards;
        card.classList.toggle('is-hidden', index < start || index >= start + visibleCards);
    });
    carouselDots.innerHTML = '';
    for (let index = 0; index < pages; index += 1) {
        const dot = document.createElement('span');
        dot.classList.toggle('active', index === carouselPage);
        dot.addEventListener('click', () => {
            carouselPage = index;
            renderCarousel();
            restartCarousel();
        });
        carouselDots.appendChild(dot);
    }
}

function restartCarousel() {
    if (!carouselTimer) return; // Evitar errores si el temporizador no está inicializado
    window.clearInterval(carouselTimer);
    carouselTimer = window.setInterval(() => {
        carouselPage += 1;
        renderCarousel();
    }, 7000);
}

const bookImageFallbacks = {
    literatura: 'https://images.unsplash.com/photo-1516979187457-637abb4f9353?auto=format&fit=crop&w=720&q=84',
    investigacion: 'https://images.unsplash.com/photo-1456513080510-7bf3a84b82f8?auto=format&fit=crop&w=720&q=84',
    tecnologia: 'https://images.unsplash.com/photo-1498050108023-c5249f4df085?auto=format&fit=crop&w=720&q=84',
    infantil: 'https://images.unsplash.com/photo-1513475382585-d06e58bcb0e0?auto=format&fit=crop&w=720&q=84',
    historia: 'https://images.unsplash.com/photo-1497633762265-9d179a990aa6?auto=format&fit=crop&w=720&q=84',
    bienestar: 'https://images.unsplash.com/photo-1503676260728-1c00da094a0b?auto=format&fit=crop&w=720&q=84',
    default: 'https://images.unsplash.com/photo-1481627834876-b7833e8f5570?auto=format&fit=crop&w=720&q=84'
};

function resolveBookImage(libro) {
    // Prioridad 1: Imagen local guardada en el servidor (si no es la por defecto)
    if (libro.imagen && libro.imagen !== 'logo.png') {
        return `/static/img/libros/${libro.imagen}`;
    }
    const categoria = normalize(libro.materia || '');
    const key = Object.keys(bookImageFallbacks).find((item) => categoria.includes(item));
    return bookImageFallbacks[key] || bookImageFallbacks.default;
}

function buildBookCard(libro) {
    const article = document.createElement('article');
    article.className = 'result-card';
    article.style.transition = 'all 0.4s cubic-bezier(0.165, 0.84, 0.44, 1)';
    article.style.borderRadius = '20px';
    article.style.boxShadow = '0 15px 35px rgba(0,0,0,0.1)';
    article.style.backgroundColor = '#fff';
    article.style.display = 'flex';
    article.style.flexDirection = 'column';
    article.style.border = '1px solid #f0f0f0';
    article.style.overflow = 'hidden';

    article.addEventListener('mouseenter', () => {
        article.style.transform = 'translateY(-12px)';
        article.style.boxShadow = '0 25px 50px rgba(0,0,0,0.15)';
    });
    article.addEventListener('mouseleave', () => {
        article.style.transform = 'translateY(0)';
        article.style.boxShadow = '0 15px 35px rgba(0,0,0,0.1)';
    });

    const imageWrap = document.createElement('div');
    imageWrap.className = 'result-cover';
    imageWrap.style.aspectRatio = '1 / 1';
    imageWrap.style.height = 'auto';
    imageWrap.style.overflow = 'hidden';
    imageWrap.style.borderRadius = '20px 20px 0 0';
    imageWrap.style.position = 'relative';
    imageWrap.style.backgroundColor = '#f8f9fa';

    const disp = Number(libro.ejemplares_disponibles || 0);
    const image = document.createElement('img');
    image.src = resolveBookImage(libro);
    image.alt = libro.titulo;
    image.loading = 'lazy';
    image.style.width = '100%';
    image.style.height = '100%';
    image.style.objectFit = 'cover';
    image.style.objectPosition = 'top'; // Priorizar la parte superior de la portada
    image.style.transition = 'transform 0.8s ease';
    image.addEventListener('error', () => { image.src = bookImageFallbacks.default; }, { once: true });
    imageWrap.appendChild(image);

    const availability = document.createElement('span');
    availability.className = 'availability-pill';
    availability.textContent = disp > 0 ? `${disp} Disponibles` : 'Agotado';
    availability.classList.toggle('is-empty', disp <= 0);
    imageWrap.appendChild(availability);
    article.appendChild(imageWrap);

    const body = document.createElement('div');
    body.className = 'result-body';
    body.style.padding = '20px'; // Ajuste de padding para tarjetas compactas
    body.style.display = 'flex';
    body.style.flexDirection = 'column';
    body.style.flex = '1';

    const category = document.createElement('span');
    category.className = 'result-category-tag';
    category.textContent = libro.materia || 'General';
    category.style.fontWeight = '600';
    category.style.textTransform = 'uppercase';
    category.style.letterSpacing = '0.5px';
    body.appendChild(category);

    const title = document.createElement('h3');
    title.textContent = libro.titulo || 'Libro sin título';
    title.style.margin = '8px 0';
    title.style.fontSize = '1.2rem'; // Fuente reducida acorde al tamaño de la portada
    title.style.fontWeight = '700';
    title.style.color = '#060b14';
    title.style.lineHeight = '1.3';
    body.appendChild(title);

    const meta = document.createElement('p');
    meta.className = 'result-meta';
    meta.style.fontSize = '1rem';
    meta.innerHTML = `<i class="fas fa-user-edit"></i> ${libro.autor || 'Anónimo'} ${libro.anio ? `<span style="opacity:0.6">| ${libro.anio}</span>` : ''}`;
    body.appendChild(meta);

    const desc = document.createElement('p');
    desc.className = 'result-desc';
    desc.style.margin = '15px 0';
    const fullDesc = libro.descripcion || 'Sin descripción disponible.';
    desc.textContent = fullDesc.length > 85 ? fullDesc.substring(0, 85) + '...' : fullDesc;
    body.appendChild(desc);

    const actions = document.createElement('div');
    actions.className = 'result-actions';
    actions.style.marginTop = 'auto';
    actions.style.paddingTop = '15px';
    actions.style.display = 'flex';
    actions.style.gap = '10px';
    
    const details = document.createElement('button');
    details.type = 'button';
    details.style.padding = '10px';
    details.style.borderRadius = '12px';
    details.style.border = '1px solid #e2e8f0';
    details.style.backgroundColor = '#ffffff';
    details.style.color = '#64748b';
    details.style.cursor = 'pointer';
    details.style.transition = 'all 0.2s';
    details.innerHTML = '<i class="fas fa-info-circle"></i>';
    details.title = "Ver detalles";
    details.addEventListener('click', () => {
        addMessage(`${libro.titulo}: ${libro.descripcion || 'Sin descripción disponible.'}`, 'bot');
        toggleTech(true);
    });

    const loan = document.createElement('button');
    loan.type = 'button';
    loan.style.flex = '1';
    loan.style.padding = '10px 20px';
    loan.style.borderRadius = '12px';
    loan.style.border = 'none';
    loan.style.backgroundColor = '#060b14';
    loan.style.color = '#ffffff';
    loan.style.fontWeight = '600';
    loan.style.cursor = 'pointer';
    loan.style.display = 'flex';
    loan.style.alignItems = 'center';
    loan.style.justifyContent = 'center';
    loan.style.gap = '8px';
    loan.innerHTML = '<span>Solicitar</span> <i class="fas fa-chevron-right"></i>';
    loan.disabled = disp <= 0;
    loan.addEventListener('click', () => {
        window.location.href = '/login';
    });
    actions.append(details, loan);
    body.appendChild(actions);
    article.appendChild(body);

    return article;
}

async function loadCategories() {
    try {
        const response = await fetch('/api/books/categorias');
        const data = await response.json();
        if (!data.success || !categorySelect) return;
        
        // Limpiar opciones previas manteniendo la primera
        while (categorySelect.options.length > 1) {
            categorySelect.remove(1);
        }

        data.categorias.forEach((categoria) => {
            const option = document.createElement('option'); // Declarar 'option'
            const name = categoria.materia || categoria.nombre || 'Sin nombre';
            option.value = name;
            option.textContent = name;
            categorySelect.appendChild(option);
            categoryNames.push(name);
        });
    } catch (error) {
        console.error("Error loading categories:", error);
    }
}

async function searchBooks() {
    if (!catalogForm) return [];
    const params = new URLSearchParams();
    new FormData(catalogForm).forEach((value, key) => {
        if (String(value).trim()) {
            params.append(key, String(value).trim());
        }
    });

    // Restablecer el Spinner de carga antes de la petición
    resultsGrid.innerHTML = `
        <div style="grid-column: 1 / -1; display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 100px 0; width: 100%;">
            <div class="loading-spinner" style="width: 50px; height: 50px; border: 3px solid rgba(6, 11, 20, 0.1); border-top: 3px solid #c5a87e; border-radius: 50%; animation: spin 1s linear infinite;"></div>
            <p style="margin-top: 20px; color: #060b14; font-size: 0.85rem; font-weight: 600; letter-spacing: 1.5px; text-transform: uppercase; font-family: inherit;">Buscando libros...</p>
        </div>
    `;

    try {
        const response = await fetch(`/api/books/?${params.toString()}`);
        const data = await response.json();
        const libros = data.libros || [];
        resultsGrid.innerHTML = ''; // Clear spinner
        if (resultsCount) {
            resultsCount.textContent = libros.length > 0
                ? `Se han encontrado ${libros.length} libros en nuestro catálogo`
                : "No se encontraron libros con esos criterios";
            resultsCount.style.display = 'block';
        }
        if (!libros.length) { // No se encontraron resultados
            const empty = document.createElement('p');
            empty.className = 'result-desc';
            empty.style.width = '100%';
            empty.style.textAlign = 'center';
            empty.style.padding = '50px 0';
            empty.textContent = 'No encontramos libros con esos criterios. Prueba con otra palabra.';
            resultsGrid.appendChild(empty);
            if (recommendedPrev) recommendedPrev.classList.add('is-hidden');
            if (recommendedNext) recommendedNext.classList.add('is-hidden');
            return [];
        }

        recommendedPage = 0; // Reiniciar posicion del carrusel
        libros.forEach((libro) => resultsGrid.appendChild(buildBookCard(libro)));
        renderRecommendedCarousel();
        return libros;
    } catch (error) { // Manejo de errores
        if (resultsCount) resultsCount.textContent = 'Error de conexión';
        const empty = document.createElement('p');
        empty.className = 'result-desc';
        empty.textContent = 'No fue posible consultar la base de datos en este momento.';
        resultsGrid.appendChild(empty);
        return [];
    }
}

function toggleTech(open) {
    techChat.classList.toggle('is-open', open);
    techToggle.setAttribute('aria-expanded', String(open));
    if (open) {
        techInput.focus();
    }
}

function addMessage(text, type = 'bot') {
    const message = document.createElement('div');
    message.className = `tech-message ${type}`;
    const paragraph = document.createElement('p');
    paragraph.textContent = text;
    message.appendChild(paragraph);
    techMessages.appendChild(message);
    techMessages.scrollTop = techMessages.scrollHeight;
}

function setSuggestions(items = []) {
    techSuggestions.innerHTML = '';
    items.slice(0, 3).forEach((item) => {
        const button = document.createElement('button');
        button.type = 'button';
        button.textContent = item;
        techSuggestions.appendChild(button);
    });
}

async function askTech(message) {
    addMessage(message, 'user');
    techInput.value = '';
    const intent = parseTechIntent(message);

    if (intent.type === 'categories') {
        const list = categoryNames.length > 0
            ? categoryNames.join(', ')
            : 'Aún no tengo la lista de categorías disponible.';
        addMessage(`¡Claro! Estas categorías están disponibles: ${list}. Elige una y te busco libros con mucho gusto.`, 'bot');
        setSuggestions(['Recomiéndame un libro', 'Buscar por autor', 'Mostrar categorías']);
        return;
    }

    if (intent.type === 'recommendation' || intent.type === 'search') {
        addMessage('¡Perfecto! Voy a buscar algo interesante para ti...', 'bot');
        const searchParams = {};
        const topic = intent.topic || getBookTopicFromMessage(message);
        let category = intent.category;

        if (!category && topic) {
            category = mapTopicToCategory(topic);
        }
        if (category) {
            searchParams.categoria = category;
        }
        if (intent.author) {
            searchParams.autor = intent.author;
        }
        if (intent.type === 'search' && !category && !intent.author) {
            // Usar el mensaje original (limpio) para la búsqueda q, no la versión normalizada extrema
            searchParams.q = message.toLowerCase().replace(/buscar|encuentra|mostrar|ver|busca|quiero.*leer|leer/i, '').trim();
        }
        if (intent.type === 'recommendation' && !category && !intent.author) {
            searchParams.q = topic || message.toLowerCase().replace(/recomiend|sugier|propone|quiero.*libro|busca.*libro|dame.*libro|necesito.*libro|tengo ganas de leer|me gustaría leer/i, '').trim();
        }

        setSearchValues(searchParams);
        const libros = await searchBooks();
        techState.lastBooks = libros;
        techState.lastQuery = searchParams;

        if (!libros.length) {
            addMessage(getTechNoResultReply(), 'bot');
        } else {
            const main = buildTechBookRecommendation(libros[0]);
            const reason = getRecommendationReason(libros[0]);
            addMessage(`${main} ${reason}`, 'bot');
        }
        setSuggestions(['Por qué me recomiendas ese', 'Buscar por autor', 'Mostrar categorías']);
        return;
    }

    if (intent.type === 'why') {
        if (techState.lastBooks.length > 0) {
            addMessage(getRecommendationReason(techState.lastBooks[0]), 'bot');
        } else {
            addMessage('Te lo explico con gusto: selecciono libros que coinciden con lo que me pides y que están disponibles en el catálogo. ¿Qué tema te interesa?', 'bot');
        }
        setSuggestions(['Recomiéndame un libro', 'Buscar por autor', 'Mostrar categorías']);
        return;
    }

    const reply = getTechFallbackReply(message);
    addMessage(reply, 'bot');
    setSuggestions(['Recomiéndame un libro', 'Qué tengo que hacer', 'Contacto']);
}

techToggle.addEventListener('click', () => toggleTech(!techChat.classList.contains('is-open')));
techClose.addEventListener('click', () => toggleTech(false));

techForm.addEventListener('submit', (event) => {
    event.preventDefault();
    const message = techInput.value.trim();
    if (message) {
        askTech(message);
    }
});

techSuggestions.addEventListener('click', (event) => {
    if (event.target.matches('button')) {
        askTech(event.target.textContent);
    }
});

if (catalogForm) {
    catalogForm.addEventListener('submit', (event) => {
        event.preventDefault();
        searchBooks();
    });

    catalogForm.addEventListener('change', (event) => {
        if (event.target.matches('select, input[type="number"]')) {
            searchBooks();
        }
    });

    clearSearch.addEventListener('click', () => {
        catalogForm.reset();
        searchBooks();
    });

    document.querySelectorAll('.cat-action[data-query], .cat-action[data-category]').forEach((action) => {
        action.addEventListener('click', () => {
            catalogForm.reset();
            catalogForm.elements.q.value = action.dataset.query || '';
            categorySelect.value = action.dataset.category || '';
            searchBooks();
        });
    });

    loadCategories().then(searchBooks);
}

if (recommendedPrev && recommendedNext) {
    recommendedPrev.addEventListener('click', () => { recommendedPage -= 1; renderRecommendedCarousel(); });
    recommendedNext.addEventListener('click', () => { recommendedPage += 1; renderRecommendedCarousel(); });
    window.addEventListener('resize', renderRecommendedCarousel);
}

if (carousel && carouselCards.length) { // Lógica del carrusel de categorías
    prevCarousel.addEventListener('click', () => { carouselPage -= 1; renderCarousel(); restartCarousel(); });
    nextCarousel.addEventListener('click', () => { carouselPage += 1; renderCarousel(); restartCarousel(); });
    window.addEventListener('resize', renderCarousel); // Volver a renderizar al cambiar tamaño de ventana
    renderCarousel(); // Renderizado inicial
    restartCarousel(); // Iniciar desplazamiento automático
}