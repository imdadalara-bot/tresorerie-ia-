<script>
  import { user, isAuthenticated } from './stores/user.js';
  import Login from './components/Login.svelte';
  import Register from './components/Register.svelte';
  import Dashboard from './components/Dashboard.svelte';
  import AddTransaction from './components/AddTransaction.svelte';
  import History from './components/History.svelte';
  import Settings from './components/Settings.svelte';

  let currentPage = 'dashboard';
  let showRegister = false;
  let showAddModal = false;

  function navigate(page) {
    currentPage = page;
  }

  function logout() {
    user.set(null);
    localStorage.removeItem('token');
    localStorage.removeItem('user');
  }

  // SVG icon helpers (inline, no emoji)
  const icons = {
    dashboard: `<svg xmlns="http://www.w3.org/2000/svg" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="7" height="7" rx="1"/><rect x="14" y="3" width="7" height="7" rx="1"/><rect x="3" y="14" width="7" height="7" rx="1"/><rect x="14" y="14" width="7" height="7" rx="1"/></svg>`,
    history: `<svg xmlns="http://www.w3.org/2000/svg" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="14 2 14 8 20 8"/><path d="M16 13H8"/><path d="M16 17H8"/><path d="M10 9H8"/><path d="M20 8l-6-6H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/></svg>`,
    settings: `<svg xmlns="http://www.w3.org/2000/svg" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1-2.83 2.83l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-4 0v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83-2.83l.06-.06A1.65 1.65 0 0 0 4.68 15a1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1 0-4h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 2.83-2.83l.06.06A1.65 1.65 0 0 0 9 4.68a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 4 0v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 2.83l-.06.06A1.65 1.65 0 0 0 19.4 9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 0 4h-.09a1.65 1.65 0 0 0-1.51 1z"/></svg>`,
    plus: `<svg xmlns="http://www.w3.org/2000/svg" width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/></svg>`,
    sync: `<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="23 4 23 10 17 10"/><polyline points="1 20 1 14 7 14"/><path d="M3.51 9a9 9 0 0 1 14.85-3.36L23 10M1 14l4.64 4.36A9 9 0 0 0 20.49 15"/></svg>`,
    user: `<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>`,
  };
</script>

{#if !$isAuthenticated}
  {#if showRegister}
    <Register on:switch={() => (showRegister = false)} />
  {:else}
    <Login on:switch={() => (showRegister = true)} />
  {/if}
{:else}
  <div class="max-w-md mx-auto min-h-screen bg-surface flex flex-col">

    <!-- Header -->
    <header class="bg-navy-800 text-white px-5 pt-12 pb-5 flex-shrink-0">
      <div class="flex items-center justify-between">
        <!-- Left: brand -->
        <div>
          <p class="text-white/50 text-xs font-medium tracking-widest uppercase mb-0.5">Tableau de bord</p>
          <h1 class="text-xl font-bold tracking-tight">Trésorier IA</h1>
        </div>

        <!-- Right: OM sync + avatar -->
        <div class="flex items-center gap-3">
          <!-- Orange Money sync badge -->
          <div class="flex items-center gap-1.5 bg-white/10 rounded-full px-3 py-1.5">
            <span class="w-2 h-2 rounded-full bg-amber-400 animate-pulse"></span>
            <span class="text-xs font-medium text-white/80">OM</span>
            {@html icons.sync}
          </div>
          <!-- Avatar / logout -->
          <button
            on:click={logout}
            aria-label="Déconnexion"
            class="w-9 h-9 rounded-full bg-white/15 flex items-center justify-center active:scale-95 transition-transform"
          >
            {@html icons.user}
          </button>
        </div>
      </div>
    </header>

    <!-- Content -->
    <main class="flex-1 overflow-y-auto pb-24 px-4 pt-5">
      {#if currentPage === 'dashboard'}
        <Dashboard />
      {:else if currentPage === 'add'}
        <AddTransaction on:done={() => navigate('dashboard')} />
      {:else if currentPage === 'history'}
        <History />
      {:else if currentPage === 'settings'}
        <Settings />
      {/if}
    </main>

    <!-- Floating Action Button -->
    <button
      on:click={() => navigate('add')}
      aria-label="Ajouter une transaction"
      class="fixed bottom-20 right-4 z-50 w-14 h-14 rounded-full bg-emerald-500 text-white flex items-center justify-center active:scale-95 transition-transform"
      style="box-shadow: 0 8px 24px rgba(16,185,129,0.40);"
    >
      {@html icons.plus}
    </button>

    <!-- Bottom Navigation -->
    <nav
      class="fixed bottom-0 left-0 right-0 max-w-md mx-auto bg-white border-t border-navy-800/8 flex z-40"
      style="padding-bottom: env(safe-area-inset-bottom, 0px);"
    >
      <button
        on:click={() => navigate('dashboard')}
        class="nav-btn {currentPage === 'dashboard' ? 'active' : ''}"
        aria-label="Tableau de bord"
      >
        {@html icons.dashboard}
        <span>Accueil</span>
      </button>

      <!-- Spacer for FAB -->
      <div class="flex-1"></div>

      <button
        on:click={() => navigate('history')}
        class="nav-btn {currentPage === 'history' ? 'active' : ''}"
        aria-label="Historique"
      >
        {@html icons.history}
        <span>Historique</span>
      </button>

      <button
        on:click={() => navigate('settings')}
        class="nav-btn {currentPage === 'settings' ? 'active' : ''}"
        aria-label="Réglages"
      >
        {@html icons.settings}
        <span>Réglages</span>
      </button>
    </nav>

  </div>
{/if}
