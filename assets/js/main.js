/* ClimatComfort39 static prototype interactions */
(() => {
  const iconArrow = `<svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h13"/><path d="m13 6 6 6-6 6"/></svg>`;
  const iconPin = `<svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><path d="M20 10c0 5-8 11-8 11S4 15 4 10a8 8 0 1 1 16 0Z"/><circle cx="12" cy="10" r="2.4"/></svg>`;
  const iconClock = `<svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="8"/><path d="M12 7v5l3 2"/></svg>`;
  const iconMail = `<svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="5" width="18" height="14" rx="2"/><path d="m3 7 9 6 9-6"/></svg>`;

  const pages = {
    home: "index.html",
    services: "services.html",
    partners: "partners.html",
    about: "about.html",
    journal: "journal.html",
    contacts: "contacts.html"
  };

  function navLink(key, label) {
    const current = document.body.dataset.page === key ? ` aria-current="page"` : "";
    return `<a href="${pages[key]}"${current}>${label}</a>`;
  }

  function renderChrome() {
    const headerTarget = document.querySelector("[data-site-header]");
    const footerTarget = document.querySelector("[data-site-footer]");
    if (headerTarget) {
      headerTarget.innerHTML = `
        <a class="skip-link" href="#main-content">К содержанию</a>
        <header class="site-header" id="site-header">
          <div class="container nav-shell">
            <a class="brand" href="index.html" aria-label="КлиматКомфорт39 — главная">
              <span class="brand-mark">CC</span>
              <span class="brand-copy">КлиматКомфорт39 <span>инженерный комфорт</span></span>
            </a>
            <nav class="main-nav" id="main-nav" aria-label="Основная навигация">
              ${navLink("home", "Главная")}
              ${navLink("services", "Решения")}
              ${navLink("partners", "Партнёрам")}
              ${navLink("about", "О нас")}
              ${navLink("journal", "Журнал")}
              ${navLink("contacts", "Контакты")}
            </nav>
            <a href="#quick-request" class="button header-cta" data-open-modal>Получить расчёт ${iconArrow}</a>
            <button class="nav-toggle" type="button" aria-label="Открыть меню" aria-controls="main-nav" aria-expanded="false"><span></span></button>
          </div>
        </header>`;
    }
    if (footerTarget) {
      footerTarget.innerHTML = `
        <footer class="site-footer">
          <div class="container">
            <div class="footer-grid">
              <div class="footer-brand">
                <a class="brand" href="index.html" aria-label="КлиматКомфорт39 — главная">
                  <span class="brand-mark">CC</span>
                  <span class="brand-copy">КлиматКомфорт39 <span>инженерный комфорт</span></span>
                </a>
                <p class="footer-copy">Комплексные решения по кондиционированию, вентиляции, отоплению, автоматизации и проектированию ОВКВ в Калининграде и области.</p>
              </div>
              <div>
                <p class="footer-heading">Решения</p>
                <ul class="footer-list"><li><a href="services.html#air">Кондиционирование</a></li><li><a href="services.html#vent">Вентиляция</a></li><li><a href="services.html#heat">Отопление и тёплый пол</a></li><li><a href="services.html#auto">Автоматика и ОВКВ</a></li></ul>
              </div>
              <div>
                <p class="footer-heading">Сотрудничество</p>
                <ul class="footer-list"><li><a href="partners.html">Дизайнерам интерьера</a></li><li><a href="partners.html#project-org">Проектным организациям</a></li><li><a href="journal.html">Полезные статьи</a></li><li><a href="contacts.html">Запросить консультацию</a></li></ul>
              </div>
              <div>
                <p class="footer-heading">География</p>
                <ul class="footer-list"><li><a href="contacts.html">Калининград</a></li><li><a href="contacts.html">Калининградская область</a></li><li><a href="contacts.html">Работа на объекте</a></li><li><a href="privacy.html">Политика конфиденциальности</a></li></ul>
              </div>
            </div>
            <div class="footer-note"><div class="footer-note-row"><span>© <span data-current-year>2026</span> КлиматКомфорт39. Прототип для climatcomfort39.ru</span><span>Материалы и характеристики уточняются в проекте и смете.</span></div></div>
          </div>
        </footer>`;
    }
  }

  function mountModal() {
    const modal = document.createElement("div");
    modal.className = "modal";
    modal.id = "quick-request";
    modal.setAttribute("role", "dialog");
    modal.setAttribute("aria-modal", "true");
    modal.setAttribute("aria-label", "Быстрый запрос расчёта");
    modal.innerHTML = `
      <div class="modal__dialog">
        <button type="button" class="modal__close" aria-label="Закрыть окно">×</button>
        <div class="modal__content">
          <div class="form-card">
            <p class="eyebrow">Первый шаг</p>
            <h2>Обсудим ваш объект</h2>
            <p>Оставьте минимум данных — в рабочей версии сайта форма подключается к CRM или Telegram. В этом прототипе она показывает сценарий отправки.</p>
            <form data-demo-form>
              <div class="form-grid">
                <div class="form-field"><label for="quick-name">Как к вам обращаться</label><input id="quick-name" name="name" required placeholder="Имя"></div>
                <div class="form-field"><label for="quick-contact">Телефон или мессенджер</label><input id="quick-contact" name="contact" required placeholder="+7 … / @username"></div>
                <div class="form-field form-field--wide"><label for="quick-task">Что нужно сделать</label><select id="quick-task" name="task"><option>Кондиционирование</option><option>Вентиляция</option><option>Отопление / тёплый пол</option><option>Проектирование ОВКВ</option><option>Комплекс инженерных систем</option><option>Партнёрство</option></select></div>
                <div class="form-field form-field--wide"><label for="quick-message">Коротко об объекте</label><textarea id="quick-message" name="message" placeholder="Тип объекта, площадь, стадия ремонта, сроки"></textarea></div>
              </div>
              <p class="form-consent">Нажимая кнопку, вы соглашаетесь с <a href="privacy.html">политикой обработки персональных данных</a>.</p>
              <button class="button button--sand" type="submit">Отправить запрос ${iconArrow}</button>
              <p class="form-status" aria-live="polite"></p>
            </form>
          </div>
        </div>
      </div>`;
    document.body.append(modal);
    return modal;
  }

  function setModalState(modal, open) {
    modal.classList.toggle("is-open", open);
    document.body.classList.toggle("menu-open", open);
    if (open) {
      setTimeout(() => modal.querySelector("input")?.focus(), 100);
    }
  }

  function initInteractions() {
    const header = document.querySelector(".site-header");
    const nav = document.querySelector(".main-nav");
    const toggle = document.querySelector(".nav-toggle");
    const modal = mountModal();
    const updateHeader = () => header?.classList.toggle("scrolled", window.scrollY > 4);
    updateHeader();
    window.addEventListener("scroll", updateHeader, { passive: true });

    toggle?.addEventListener("click", () => {
      const expanded = toggle.getAttribute("aria-expanded") === "true";
      toggle.setAttribute("aria-expanded", String(!expanded));
      toggle.setAttribute("aria-label", expanded ? "Открыть меню" : "Закрыть меню");
      nav.classList.toggle("is-open", !expanded);
      document.body.classList.toggle("menu-open", !expanded);
    });
    nav?.querySelectorAll("a").forEach(link => link.addEventListener("click", () => {
      toggle?.setAttribute("aria-expanded", "false");
      toggle?.setAttribute("aria-label", "Открыть меню");
      nav.classList.remove("is-open");
      document.body.classList.remove("menu-open");
    }));

    document.querySelectorAll("[data-open-modal]").forEach(trigger => {
      trigger.addEventListener("click", event => {
        event.preventDefault();
        setModalState(modal, true);
      });
    });
    modal.querySelector(".modal__close").addEventListener("click", () => setModalState(modal, false));
    modal.addEventListener("click", event => { if (event.target === modal) setModalState(modal, false); });
    document.addEventListener("keydown", event => { if (event.key === "Escape") setModalState(modal, false); });

    document.querySelectorAll("[data-demo-form]").forEach(form => {
      form.addEventListener("submit", event => {
        event.preventDefault();
        const status = form.querySelector(".form-status");
        const button = form.querySelector("button[type=submit]");
        button.disabled = true;
        button.style.opacity = ".72";
        status.textContent = "Спасибо. В прототипе заявка не отправляется — подключите CRM, почту или Telegram-бот при запуске.";
        form.reset();
        setTimeout(() => { button.disabled = false; button.style.opacity = ""; }, 1000);
      });
    });

    document.querySelectorAll("[data-current-year]").forEach(el => { el.textContent = new Date().getFullYear(); });
  }

  renderChrome();
  initInteractions();
})();
