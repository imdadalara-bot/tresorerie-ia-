<script>
  import { onMount } from 'svelte';
  import { api } from '../services/api.js';
  import { user } from '../stores/user.js';

  let omStatus = null;
  let saving = false;
  let message = '';

  let name = '';
  let sector = '';
  let currency = '';

  onMount(async () => {
    if ($user) {
      name = $user.name;
      sector = $user.sector;
      currency = $user.currency;
    }
    try {
      omStatus = await api.getOmStatus();
    } catch {
      omStatus = { connected: false };
    }
  });

  async function saveProfile() {
    saving = true;
    message = '';
    try {
      await api.updateProfile({ name, sector, currency });
      user.set({ ...$user, name, sector, currency });
      message = 'Profil mis à jour !';
    } catch (e) {
      message = 'Erreur: ' + e.message;
    } finally {
      saving = false;
    }
  }

  async function connectOrangeMoney() {
    try {
      const result = await api.getOmAuthUrl();
      if (result.url) {
        window.location.href = result.url;
      } else {
        message = result.message || 'Orange Money non configuré';
      }
    } catch (e) {
      message = e.message;
    }
  }

  async function syncOrangeMoney() {
    try {
      await api.syncOm();
      omStatus = await api.getOmStatus();
      message = 'Synchronisation effectuée !';
    } catch (e) {
      message = e.message;
    }
  }
</script>

<div class="space-y-6">
  <h2 class="text-lg font-bold text-gray-800">Réglages</h2>

  {#if message}
    <div class="bg-blue-50 text-blue-600 text-sm p-3 rounded-lg">{message}</div>
  {/if}

  <!-- Profile -->
  <div class="card">
    <h3 class="font-medium text-gray-700 mb-3">Profil</h3>
    <div class="space-y-3">
      <div>
        <label for="settings-name" class="text-sm text-gray-600">Nom</label>
        <input id="settings-name" type="text" bind:value={name} class="input-field" />
      </div>
      <div>
        <label for="settings-sector" class="text-sm text-gray-600">Secteur</label>
        <select id="settings-sector" bind:value={sector} class="input-field">
          <option value="commercant">Commerçant</option>
          <option value="agriculteur">Agriculteur</option>
          <option value="restaurateur">Restaurateur</option>
          <option value="autre">Autre</option>
        </select>
      </div>
      <div>
        <label for="settings-currency" class="text-sm text-gray-600">Devise</label>
        <select id="settings-currency" bind:value={currency} class="input-field">
          <option value="XOF">FCFA (XOF)</option>
          <option value="EUR">Euro (EUR)</option>
          <option value="USD">Dollar (USD)</option>
        </select>
      </div>
      <button on:click={saveProfile} class="btn-primary w-full" disabled={saving}>
        {saving ? 'Enregistrement...' : 'Enregistrer'}
      </button>
    </div>
  </div>

  <!-- Orange Money -->
  <div class="card">
    <h3 class="font-medium text-gray-700 mb-3">Orange Money</h3>
    {#if omStatus?.connected}
      <div class="flex items-center gap-2 mb-3">
        <span class="w-2 h-2 bg-green-500 rounded-full"></span>
        <span class="text-sm text-green-600">Connecté</span>
      </div>
      {#if omStatus.last_sync}
        <p class="text-xs text-gray-400 mb-3">
          Dernière sync: {new Date(omStatus.last_sync).toLocaleString('fr-FR')}
        </p>
      {/if}
      <button on:click={syncOrangeMoney} class="btn-secondary w-full">
        Synchroniser maintenant
      </button>
    {:else}
      <p class="text-sm text-gray-500 mb-3">
        Connectez votre compte Orange Money pour synchroniser automatiquement vos transactions.
      </p>
      <button on:click={connectOrangeMoney} class="btn-primary w-full">
        Connecter Orange Money
      </button>
    {/if}
  </div>

  <!-- App info -->
  <div class="card text-center text-xs text-gray-400">
    <p>Trésorier IA v1.0</p>
    <p>Gestion intelligente de trésorerie</p>
    <p class="mt-1">Afrique de l'Ouest</p>
  </div>
</div>
