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
      error = 'Veuillez saisir un montant valide';
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
      success = 'Transaction enregistrée !';
      amount = '';
      note = '';
      setTimeout(() => dispatch('done'), 900);
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

<div class="space-y-5">

  <!-- Page header -->
  <div>
    <p class="text-xs font-semibold text-navy-800/40 uppercase tracking-wider">Nouvelle transaction</p>
    <h2 class="text-xl font-bold text-navy-800 mt-0.5">Ajouter un mouvement</h2>
  </div>

  {#if error}
    <div class="flex items-center gap-2 bg-danger/8 text-danger text-sm px-4 py-3 rounded-xl border border-danger/15">
      <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>
      {error}
    </div>
  {/if}

  {#if success}
    <div class="flex items-center gap-2 bg-emerald-500/10 text-emerald-600 text-sm px-4 py-3 rounded-xl border border-emerald-500/20">
      <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><polyline points="20 6 9 17 4 12"/></svg>
      {success}
    </div>
  {/if}

  <form on:submit|preventDefault={handleSubmit} class="space-y-4">

    <!-- Type toggle -->
    <div class="card p-1 flex gap-1">
      <button
        type="button"
        on:click={() => (type = 'income')}
        class="flex-1 py-3 rounded-xl font-semibold text-sm text-center transition-all
               {type === 'income'
                 ? 'bg-emerald-500 text-white shadow-sm'
                 : 'text-navy-800/50 hover:text-navy-800'}"
      >
        <span class="flex items-center justify-center gap-1.5">
          <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><line x1="12" y1="19" x2="12" y2="5"/><polyline points="5 12 12 5 19 12"/></svg>
          Entrée d&apos;argent
        </span>
      </button>
      <button
        type="button"
        on:click={() => (type = 'expense')}
        class="flex-1 py-3 rounded-xl font-semibold text-sm text-center transition-all
               {type === 'expense'
                 ? 'bg-danger text-white shadow-sm'
                 : 'text-navy-800/50 hover:text-navy-800'}"
      >
        <span class="flex items-center justify-center gap-1.5">
          <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><line x1="12" y1="5" x2="12" y2="19"/><polyline points="19 12 12 19 5 12"/></svg>
          Dépense
        </span>
      </button>
    </div>

    <!-- Amount -->
    <div class="card">
      <label for="amount" class="block text-xs font-semibold text-navy-800/40 uppercase tracking-wider mb-2">Montant (FCFA)</label>
      <div class="relative">
        <input
          id="amount"
          type="number"
          bind:value={amount}
          class="w-full text-4xl font-bold text-navy-800 text-center bg-transparent outline-none placeholder-navy-800/20 py-2"
          placeholder="0"
          min="1"
          inputmode="numeric"
          required
        />
        <p class="text-center text-navy-800/30 text-sm">francs CFA</p>
      </div>
    </div>

    <!-- Date -->
    <div>
      <label for="txn-date" class="block text-xs font-semibold text-navy-800/40 uppercase tracking-wider mb-1.5">Date</label>
      <input id="txn-date" type="date" bind:value={date} class="input-field" required />
    </div>

    <!-- Note -->
    <div>
      <label for="note" class="block text-xs font-semibold text-navy-800/40 uppercase tracking-wider mb-1.5">Note (optionnel)</label>
      <input
        id="note"
        type="text"
        bind:value={note}
        class="input-field"
        placeholder="Ex: Vente tissu, Loyer, Transport…"
      />
    </div>

    <button
      type="submit"
      class="btn-primary w-full text-base py-4 mt-2"
      disabled={loading}
      style="{type === 'income' ? 'background:#10B981;' : type === 'expense' ? 'background:#EF4444;' : ''}"
    >
      {#if loading}
        <span class="flex items-center justify-center gap-2">
          <span class="w-4 h-4 border-2 border-white/40 border-t-white rounded-full animate-spin"></span>
          Enregistrement…
        </span>
      {:else}
        Enregistrer la transaction
      {/if}
    </button>

  </form>
</div>
