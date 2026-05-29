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

  function navigate(page) {
    currentPage = page;
  }

  function logout() {
    user.set(null);
    localStorage.removeItem('token');
    localStorage.removeItem('user');
  }
</script>

{#if !$isAuthenticated}
  {#if showRegister}
    <Register on:switch={() => (showRegister = false)} />
  {:else}
    <Login on:switch={() => (showRegister = true)} />
  {/if}
{:else}
  <div class="max-w-md mx-auto min-h-screen bg-gray-50">
    <!-- Header -->
    <header class="bg-primary-600 text-white px-4 py-3 flex items-center justify-between">
      <h1 class="text-lg font-bold">Trésorier IA</h1>
      <button on:click={logout} class="text-sm opacity-80 hover:opacity-100">
        Déconnexion
      </button>
    </header>

    <!-- Content -->
    <main class="p-4 pb-20">
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

    <!-- Bottom nav -->
    <nav class="fixed bottom-0 left-0 right-0 max-w-md mx-auto bg-white border-t border-gray-200 flex">
      <button
        on:click={() => navigate('dashboard')}
        class="flex-1 py-3 text-center text-xs {currentPage === 'dashboard' ? 'text-primary-600 font-bold' : 'text-gray-500'}"
      >
        <div class="text-lg">📊</div>
        Tableau
      </button>
      <button
        on:click={() => navigate('add')}
        class="flex-1 py-3 text-center text-xs {currentPage === 'add' ? 'text-primary-600 font-bold' : 'text-gray-500'}"
      >
        <div class="text-lg">➕</div>
        Ajouter
      </button>
      <button
        on:click={() => navigate('history')}
        class="flex-1 py-3 text-center text-xs {currentPage === 'history' ? 'text-primary-600 font-bold' : 'text-gray-500'}"
      >
        <div class="text-lg">📋</div>
        Historique
      </button>
      <button
        on:click={() => navigate('settings')}
        class="flex-1 py-3 text-center text-xs {currentPage === 'settings' ? 'text-primary-600 font-bold' : 'text-gray-500'}"
      >
        <div class="text-lg">⚙️</div>
        Réglages
      </button>
    </nav>
  </div>
{/if}
