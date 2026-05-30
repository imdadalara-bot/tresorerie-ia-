<script>
  import { createEventDispatcher } from 'svelte';
  import { api } from '../services/api.js';
  import { user } from '../stores/user.js';

  const dispatch = createEventDispatcher();

  let email = '';
  let password = '';
  let error = '';
  let loading = false;

  async function handleLogin() {
    error = '';
    loading = true;
    try {
      const result = await api.login({ email, password });
      localStorage.setItem('token', result.access_token);
      const me = await api.getMe();
      user.set(me);
    } catch (e) {
      error = e.message;
    } finally {
      loading = false;
    }
  }
</script>

<div class="min-h-screen flex items-center justify-center bg-gradient-to-b from-primary-600 to-primary-800 p-4">
  <div class="bg-white rounded-2xl shadow-xl p-6 w-full max-w-sm">
    <div class="text-center mb-6">
      <h1 class="text-2xl font-bold text-primary-700">Trésorier IA</h1>
      <p class="text-gray-500 text-sm mt-1">Gérez votre trésorerie intelligemment</p>
    </div>

    <form on:submit|preventDefault={handleLogin} class="space-y-4">
      {#if error}
        <div class="bg-red-50 text-red-600 text-sm p-3 rounded-lg">{error}</div>
      {/if}

      <div>
        <label for="email" class="block text-sm font-medium text-gray-700 mb-1">Email</label>
        <input
          id="email"
          type="email"
          bind:value={email}
          class="input-field"
          placeholder="votre@email.com"
          required
        />
      </div>

      <div>
        <label for="password" class="block text-sm font-medium text-gray-700 mb-1">Mot de passe</label>
        <input
          id="password"
          type="password"
          bind:value={password}
          class="input-field"
          placeholder="••••••••"
          required
        />
      </div>

      <button type="submit" class="btn-primary w-full" disabled={loading}>
        {loading ? 'Connexion...' : 'Se connecter'}
      </button>
    </form>

    <p class="text-center text-sm text-gray-500 mt-4">
      Pas encore de compte ?
      <button on:click={() => dispatch('switch')} class="text-primary-600 font-medium">
        Créer un compte
      </button>
    </p>
  </div>
</div>
