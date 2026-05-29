<script>
  import { createEventDispatcher } from 'svelte';
  import { api } from '../services/api.js';
  import { offlineStorage } from '../services/storage.js';

  const dispatch = createEventDispatcher();

  let type = 'income';
  let amount = '';
  let note = '';
  let date = new Date().toISOString().split('T')[0];
  let loading = false;
  let error = '';
  let success = '';

  async function handleSubmit() {
    if (!amount || parseFloat(amount) <= 0) {
      error = 'Montant invalide';
      return;
    }

    error = '';
    success = '';
    loading = true;

    const txnData = {
      type,
      amount: parseFloat(amount),
      date,
      note: note || null,
      source: 'manual',
    };

    try {
      await api.addTransaction(txnData);
      success = 'Transaction ajoutée !';
      amount = '';
      note = '';
      setTimeout(() => dispatch('done'), 1000);
    } catch {
      await offlineStorage.saveTransaction({
        id: 'offline_' + Date.now(),
        ...txnData,
      });
      success = 'Sauvegardé hors-ligne. Sera synchronisé plus tard.';
    } finally {
      loading = false;
    }
  }
</script>

<div class="space-y-4">
  <h2 class="text-lg font-bold text-gray-800">Ajouter une transaction</h2>

  {#if error}
    <div class="bg-red-50 text-red-600 text-sm p-3 rounded-lg">{error}</div>
  {/if}
  {#if success}
    <div class="bg-green-50 text-green-600 text-sm p-3 rounded-lg">{success}</div>
  {/if}

  <form on:submit|preventDefault={handleSubmit} class="space-y-4">
    <!-- Type toggle -->
    <div class="flex gap-2">
      <button
        type="button"
        on:click={() => (type = 'income')}
        class="flex-1 py-3 rounded-lg font-medium text-center transition-colors
               {type === 'income' ? 'bg-green-500 text-white' : 'bg-gray-100 text-gray-600'}"
      >
        + Entrée
      </button>
      <button
        type="button"
        on:click={() => (type = 'expense')}
        class="flex-1 py-3 rounded-lg font-medium text-center transition-colors
               {type === 'expense' ? 'bg-red-500 text-white' : 'bg-gray-100 text-gray-600'}"
      >
        - Sortie
      </button>
    </div>

    <!-- Amount -->
    <div>
      <label for="amount" class="block text-sm font-medium text-gray-700 mb-1">Montant (FCFA)</label>
      <input
        id="amount"
        type="number"
        bind:value={amount}
        class="input-field text-2xl text-center font-bold"
        placeholder="0"
        min="1"
        required
      />
    </div>

    <!-- Date -->
    <div>
      <label for="txn-date" class="block text-sm font-medium text-gray-700 mb-1">Date</label>
      <input id="txn-date" type="date" bind:value={date} class="input-field" required />
    </div>

    <!-- Note -->
    <div>
      <label for="note" class="block text-sm font-medium text-gray-700 mb-1">Note (optionnel)</label>
      <input id="note" type="text" bind:value={note} class="input-field" placeholder="Ex: Vente tissu, Loyer..." />
    </div>

    <button type="submit" class="btn-primary w-full text-lg py-3" disabled={loading}>
      {loading ? 'Enregistrement...' : 'Enregistrer'}
    </button>
  </form>
</div>
