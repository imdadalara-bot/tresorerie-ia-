<script>
  import { createEventDispatcher } from 'svelte';
  import { api } from '../services/api.js';
  import { user } from '../stores/user.js';

  const dispatch = createEventDispatcher();

  let name = '';
  let email = '';
  let phone = '';
  let password = '';
  let sector = 'commercant';
  let currency = 'XOF';
  let error = '';
  let loading = false;

  const sectors = [
    { value: 'commercant', label: 'Commerçant' },
    { value: 'agriculteur', label: 'Agriculteur' },
    { value: 'restaurateur', label: 'Restaurateur' },
    { value: 'autre', label: 'Autre' },
  ];

  async function handleRegister() {
    error = '';
    loading = true;
    try {
      const result = await api.register({
        name,
        email: email || undefined,
        phone: phone || undefined,
        password,
        sector,
        currency,
      });
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
      <h1 class="text-2xl font-bold text-primary-700">Créer un compte</h1>
      <p class="text-gray-500 text-sm mt-1">Commencez en 30 secondes</p>
    </div>

    <form on:submit|preventDefault={handleRegister} class="space-y-3">
      {#if error}
        <div class="bg-red-50 text-red-600 text-sm p-3 rounded-lg">{error}</div>
      {/if}

      <div>
        <label for="name" class="block text-sm font-medium text-gray-700 mb-1">Nom</label>
        <input id="name" type="text" bind:value={name} class="input-field" placeholder="Votre nom" required />
      </div>

      <div>
        <label for="reg-email" class="block text-sm font-medium text-gray-700 mb-1">Email</label>
        <input id="reg-email" type="email" bind:value={email} class="input-field" placeholder="votre@email.com" />
      </div>

      <div>
        <label for="phone" class="block text-sm font-medium text-gray-700 mb-1">Téléphone</label>
        <input id="phone" type="tel" bind:value={phone} class="input-field" placeholder="+221 xx xxx xx xx" />
      </div>

      <div>
        <label for="reg-password" class="block text-sm font-medium text-gray-700 mb-1">Mot de passe</label>
        <input id="reg-password" type="password" bind:value={password} class="input-field" placeholder="••••••••" required />
      </div>

      <div>
        <label for="sector" class="block text-sm font-medium text-gray-700 mb-1">Secteur</label>
        <select id="sector" bind:value={sector} class="input-field">
          {#each sectors as s}
            <option value={s.value}>{s.label}</option>
          {/each}
        </select>
      </div>

      <div>
        <label for="currency" class="block text-sm font-medium text-gray-700 mb-1">Devise</label>
        <select id="currency" bind:value={currency} class="input-field">
          <option value="XOF">FCFA (XOF)</option>
          <option value="EUR">Euro (EUR)</option>
          <option value="USD">Dollar (USD)</option>
        </select>
      </div>

      <button type="submit" class="btn-primary w-full" disabled={loading}>
        {loading ? 'Création...' : 'Créer mon compte'}
      </button>
    </form>

    <p class="text-center text-sm text-gray-500 mt-4">
      Déjà un compte ?
      <button on:click={() => dispatch('switch')} class="text-primary-600 font-medium">
        Se connecter
      </button>
    </p>
  </div>
</div>
