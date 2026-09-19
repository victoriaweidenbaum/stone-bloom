(function () {
  // Mobile menu
  var burger = document.querySelector('.burger');
  if (burger) {
    burger.addEventListener('click', function () {
      var open = document.documentElement.classList.toggle('menu-open');
      burger.setAttribute('aria-expanded', open);
      burger.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
      if (open) window.scrollTo(0, 0);
    });
  }

  // Fade elements in as they enter the viewport, slightly staggered
  var fades = document.querySelectorAll('.fade');
  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (entries) {
      var n = 0;
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        entry.target.style.setProperty('--delay', (n++ * 0.1) + 's');
        entry.target.classList.add('in');
        io.unobserve(entry.target);
      });
    }, { rootMargin: '0px 0px -5% 0px' });
    fades.forEach(function (el) { io.observe(el); });
  } else {
    fades.forEach(function (el) { el.classList.add('in'); });
  }

  // Forms post to FormSubmit, which forwards each submission by email
  document.querySelectorAll('form[data-ajax]').forEach(function (form) {
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var button = form.querySelector('button[type="submit"]');
      var error = form.querySelector('.form-error');
      if (error) error.remove();
      button.disabled = true;

      var data = {};
      new FormData(form).forEach(function (value, key) { data[key] = value; });

      fetch(form.getAttribute('data-ajax'), {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'Accept': 'application/json' },
        body: JSON.stringify(data)
      })
        .then(function (res) { return res.ok ? res.json() : Promise.reject(res); })
        .then(function () {
          var message = document.createElement('p');
          message.className = 'form-message';
          message.textContent = form.getAttribute('data-success') || 'Thank you!';
          form.replaceWith(message);
        })
        .catch(function () {
          button.disabled = false;
          var p = document.createElement('p');
          p.className = 'form-error';
          p.textContent = 'Something went wrong. Please try again or email vweidenbaum@gmail.com.';
          form.insertBefore(p, button);
        });
    });
  });
})();
