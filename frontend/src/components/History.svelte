<script>
  import { onMount } from 'svelte';
  import { api } from '../services/api.js';

  let transactions = [];
  let loading = true;
  let error = '';
  let days = 30;
  let exporting = false;

  onMount(() => loadTransactions());

  async function loadTransactions() {
    loading = true;
    error = '';
    try {
      const result = await api.getTransactions(days);
      transactions = result.transactions;
    } catch (e) {
      error = e.message;
    } finally {
      loading = false;
    }
  }

  async function deleteTransaction(id) {
    if (!confirm('Supprimer cette transaction ?')) return;
    try {
      await api.deleteTransaction(id);
      transactions = transactions.filter((t) => t.id !== id);
    } catch (e) {
      error = e.message;
    }
  }

  async function handleExport() {
    exporting = true;
    try {
      const res = await api.exportPdf(days);
      const blob = await res.blob();
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = 'tresorier_rapport.pdf';
      a.click();
      URL.revokeObjectURL(url);
    } catch (e) {
      error = 'Erreur export PDF';
    } finally {
      exporting = false;
    }
  }

  function formatDate(dateStr) {
    return new Date(dateStr).toLocaleDateString('fr-FR', {
      day: 'numeric',
      month: 'short',
    });
  }
</script>

<div class="space-y-4">

  <!-- Header -->
  <div class="flex items-start justify-between">
    <div>
      <p class="text-xs font-semibold text-navy-800/40 uppercase tracking-wider">Vos mouvements</p>
      <h2 class="text-xl font-bold text-navy-800 mt-0.5">Historique</h2>
    </div>
    <button
      on:click={handleExport}
      disabled={exporting}
      class="flex items-center gap-1.5 bg-navy-800 text-white text-xs font-semibold px-3 py-2 rounded-xl active:scale-95 transition-transform disabled:opacity-50"
    >
      {#if exporting}
        <span class="w-3.5 h-3.5 border-2 border-white/30 border-t-white rounded-full animate-spin"></span>
      {:else}
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/><polyline points="10 9 9 9 8 9"/></svg>
      {/if}
      PDF
    </button>
  </div>

  <!-- Period selector -->
  <div class="card p-1 flex gap-1">
    {#each [7, 30, 90] as d}
      <button
        on:click={() => { days = d; loadTransactions(); }}
        class="flex-1 py-2.5 rounded-xl text-sm font-semibold transition-all
               {days === d ? 'bg-navy-800 text-white shadow-sm' : 'text-navy-800/50 hover:text-navy-800'}"
      >
        {d} jours
      </button>
    {/each}
  </div>

  {#if loading}
    <div class="flex flex-col items-center justify-center py-16 gap-3">
      <div class="w-8 h-8 rounded-full border-2 border-navy-800/15 border-t-navy-800 animate-spin"></div>
      <p class="text-navy-800/40 text-sm">Chargement…</p>
    </div>
  {:else if error}
    <div class="card bg-danger/5 border border-danger/15 text-center py-6">
      <p class="text-danger text-sm">{error}</p>
    </div>
  {:else if transactions.length === 0}
    <div class="flex flex-col items-center justify-center py-16 gap-3">
      <div class="w-14 h-14 rounded-2xl bg-navy-800/6 flex items-center justify-center">
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#1A2B48" stroke-opacity="0.3" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M20 12V22H4V12"/><path d="M22 7H2v5h20V7z"/><path d="M12 22V7"/><path d="M12 7H7.5a2.5 2.5 0 0 1 0-5C11 2 12 7 12 7z"/><path d="M12 7h4.5a2.5 2.5 0 0 0 0-5C13 2 12 7 12 7z"/></svg>
      </div>
      <p class="text-navy-800/40 text-sm font-medium">Aucune transaction sur cette période</p>
    </div>
  {:else}
    <div class="space-y-2">
      {#each transactions as txn}
        <div class="card flex items-center gap-3">
          <!-- Direction icon -->
          <div class="w-10 h-10 rounded-xl flex-shrink-0 flex items-center justify-center {txn.type === 'income' ? 'bg-emerald-500/10' : 'bg-danger/8'}">
            {#if txn.type === 'income'}
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#10B981" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><line x1="12" y1="19" x2="12" y2="5"/><polyline points="5 12 12 5 19 12"/></svg>
            {:else}
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#EF4444" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><line x1="12" y1="5" x2="12" y2="19"/><polyline points="19 12 12 19 5 12"/></svg>
            {/if}
          </div>

          <!-- Details -->
          <div class="flex-1 min-w-0">
            <p class="text-navy-800 text-sm font-medium truncate">{txn.note || (txn.type === 'income' ? 'Entrée' : 'Dépense')}</p>
            <p class="text-navy-800/40 text-xs">{formatDate(txn.date)}</p>
          </div>

          <!-- Amount + delete -->
          <div class="flex items-center gap-2 flex-shrink-0">
            <p class="font-bold text-sm {txn.type === 'income' ? 'text-emerald-500' : 'text-danger'}">
              {txn.type === 'income' ? '+' : '-'}{new Intl.NumberFormat('fr-FR').format(txn.amount)}
            </p>
            <button
              on:click={() => deleteTransaction(txn.id)}
              aria-label="Supprimer"
              class="w-7 h-7 rounded-lg flex items-center justify-center text-navy-800/20 hover:text-danger hover:bg-danger/8 transition-colors"
            >
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>
            </button>
          </div>
        </div>
      {/each}
    </div>
  {/if}

</div>
