document.addEventListener('DOMContentLoaded', function () {
  const SIDEBAR_BREAKPOINT = 992;

  // Fecha en topbar
  const dateEl = document.getElementById('current-date');
  if (dateEl) {
    try {
      const now = new Date();
      dateEl.textContent = now.toLocaleDateString('es-ES', {
        weekday: 'long',
        year: 'numeric',
        month: 'long',
        day: 'numeric',
      });
    } catch {
      // noop
    }
  }

  // Estado del sistema (placeholder liviano)
  const statsEl = document.getElementById('system-stats');
  if (statsEl) {
    statsEl.textContent = 'OK';
  }

  // Sidebar behavior (single source of truth)
  const sidebarToggle = document.getElementById('sidebarToggle');
  const sidebar = document.querySelector('.sidebar');

  const isMobile = () => window.innerWidth <= SIDEBAR_BREAKPOINT;

  const closeMobileSidebar = () => {
    if (sidebar && sidebar.classList.contains('active')) {
      sidebar.classList.remove('active');
    }
  };

  const normalizeSidebarState = () => {
    if (!sidebar) return;

    if (isMobile()) {
      // En móvil, el sidebar es off-canvas: no debe quedar colapsado
      sidebar.classList.remove('collapsed');
    } else {
      // En escritorio, el sidebar siempre visible: no debe quedar como "active"
      sidebar.classList.remove('active');
    }
  };

  normalizeSidebarState();
  window.addEventListener('resize', normalizeSidebarState);

  if (sidebarToggle && sidebar) {
    sidebarToggle.addEventListener('click', function (e) {
      e.preventDefault();

      if (isMobile()) {
        sidebar.classList.toggle('active');
        return;
      }

      sidebar.classList.toggle('collapsed');
      sidebar.classList.remove('active');
    });

    // Cerrar sidebar al hacer clic fuera (solo en móvil/tablet)
    document.addEventListener('click', function (e) {
      if (!isMobile()) return;
      if (!sidebar.classList.contains('active')) return;

      if (!sidebar.contains(e.target) && !sidebarToggle.contains(e.target)) {
        sidebar.classList.remove('active');
      }
    });
  }

  // Si el sidebar está abierto en móvil, cerrarlo al navegar
  if (sidebar) {
    document.querySelectorAll('.sidebar a').forEach((a) => {
      a.addEventListener('click', () => {
        if (isMobile()) {
          closeMobileSidebar();
        }
      });
    });
  }
});
