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
      a.download = `tresorier_rapport.pdf`;
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
  <div class="flex items-center justify-between">
    <h2 class="text-lg font-bold text-gray-800">Historique</h2>
    <button on:click={handleExport} class="btn-secondary text-xs" disabled={exporting}>
      {exporting ? '...' : '📄 PDF'}
    </button>
  </div>

  <!-- Period selector -->
  <div class="flex gap-2">
    {#each [7, 30, 90] as d}
      <button
        on:click={() => { days = d; loadTransactions(); }}
        class="flex-1 py-2 rounded-lg text-sm font-medium
               {days === d ? 'bg-primary-600 text-white' : 'bg-gray-100 text-gray-600'}"
      >
        {d}j
      </button>
    {/each}
  </div>

  {#if loading}
    <div class="text-center py-8">
      <div class="animate-spin rounded-full h-6 w-6 border-b-2 border-primary-600 mx-auto"></div>
    </div>
  {:else if error}
    <div class="bg-red-50 text-red-600 text-sm p-3 rounded-lg">{error}</div>
  {:else if transactions.length === 0}
    <div class="text-center py-8 text-gray-400">
      <p class="text-3xl mb-2">📭</p>
      <p>Aucune transaction sur cette période</p>
    </div>
  {:else}
    <div class="space-y-2">
      {#each transactions as txn}
        <div class="card flex items-center justify-between">
          <div>
            <p class="font-medium text-sm {txn.type === 'income' ? 'text-green-600' : 'text-red-500'}">
              {txn.type === 'income' ? '+' : '-'}{new Intl.NumberFormat('fr-FR').format(txn.amount)} FCFA
            </p>
            <p class="text-xs text-gray-400">
              {formatDate(txn.date)}
              {#if txn.note} — {txn.note}{/if}
            </p>
          </div>
          <button
            on:click={() => deleteTransaction(txn.id)}
            class="text-gray-300 hover:text-red-500 text-sm"
            title="Supprimer"
          >✕</button>
        </div>
      {/each}
    </div>
  {/if}
</div>
