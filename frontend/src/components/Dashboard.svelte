<script>
  import { onMount } from 'svelte';
  import { api } from '../services/api.js';
  import { offlineStorage } from '../services/storage.js';
  import SparkLine from './SparkLine.svelte';

  let dashboard = null;
  let loading = true;
  let error = '';
  let offline = false;

  onMount(async () => {
    try {
      dashboard = await api.getDashboard();
      offlineStorage.cacheDashboard(dashboard);
      offline = false;
    } catch {
      const cached = await offlineStorage.getCachedDashboard();
      if (cached) {
        dashboard = cached;
        offline = true;
      } else {
        error = 'Impossible de charger le tableau de bord';
      }
    } finally {
      loading = false;
    }
  });

  function formatAmount(amount, currency) {
    return new Intl.NumberFormat('fr-FR').format(Math.round(amount)) + '\u00a0' + (currency || 'FCFA');
  }

  function riskLabel(level) {
    if (level === 'HIGH') return 'Risque élevé';
    if (level === 'MEDIUM') return 'Risque modéré';
    return 'Risque faible';
  }

  function riskBadgeClass(level) {
    if (level === 'HIGH') return 'badge-risk-high';
    if (level === 'MEDIUM') return 'badge-risk-medium';
    return 'badge-risk-low';
  }

  function riskBorderClass(level) {
    if (level === 'HIGH') return 'border-l-danger';
    if (level === 'MEDIUM') return 'border-l-amber-500';
    return 'border-l-emerald-500';
  }

  // Mock recent transactions for display (replace with real API data when available)
  const mockTransactions = [
    { type: 'income', amount: 75000, note: 'Vente tissu wax', date: '2024-06-01' },
    { type: 'expense', amount: 18500, note: 'Transport marchandises', date: '2024-05-31' },
    { type: 'income', amount: 42000, note: 'Commande client Dakar', date: '2024-05-31' },
    { type: 'expense', amount: 31200, note: 'Paiement fournisseur', date: '2024-05-30' },
  ];

  function formatDateShort(dateStr) {
    return new Date(dateStr).toLocaleDateString('fr-FR', { day: 'numeric', month: 'short' });
  }

  // Derive display-level data with fallbacks for demo purposes
  $: balance = dashboard?.current_balance ?? 1_254_800;
  $: currency = dashboard?.currency ?? 'FCFA';
  $: weeklyIncome = dashboard?.weekly_income ?? 312_000;
  $: weeklyExpense = dashboard?.weekly_expense ?? 188_500;
  $: weeklyNet = dashboard?.weekly_net ?? (weeklyIncome - weeklyExpense);
  $: riskLevel = dashboard?.risk_level ?? 'MEDIUM';
  $: forecastBalance = dashboard?.forecast_15d?.[dashboard.forecast_15d.length - 1]?.predicted_balance ?? 1_480_000;
  $: forecastConfidence = dashboard?.forecast_15d?.[dashboard.forecast_15d.length - 1]?.confidence ?? 0.78;
  $: sparkData = dashboard?.daily_flows_7d?.map(d => d.net) ?? [12000, -8000, 45000, 32000, -15000, 67000, 23000];
  $: forecastData = dashboard?.forecast_15d?.map(d => d.predicted_balance) ?? Array.from({ length: 15 }, (_, i) => balance + i * 15000 - Math.random() * 5000);
  $: alerts = dashboard?.alerts ?? [{ message: 'Paiement fournisseur mercredi — solde critique potentiel', days_until: 3 }];
  $: recentTxns = mockTransactions;
</script>

{#if loading}
  <div class="flex flex-col items-center justify-center py-24 gap-4">
    <div class="w-10 h-10 rounded-full border-2 border-navy-800/15 border-t-navy-800 animate-spin"></div>
    <p class="text-navy-800/50 text-sm">Chargement…</p>
  </div>
{:else if error}
  <div class="card border border-danger/20 bg-danger/5 text-center py-8">
    <p class="text-danger text-sm font-medium">{error}</p>
  </div>
{:else}

  {#if offline}
    <div class="flex items-center gap-2 bg-amber-500/10 text-amber-700 text-xs px-4 py-2.5 rounded-xl mb-4 border border-amber-500/20">
      <span class="w-1.5 h-1.5 rounded-full bg-amber-500 flex-shrink-0"></span>
      Mode hors-ligne — affichage depuis le cache
    </div>
  {/if}

  <!-- Balance Card (Hero) -->
  <div class="rounded-2xl overflow-hidden mb-4" style="background: linear-gradient(135deg, #1A2B48 0%, #243D64 100%); box-shadow: 0 4px 20px rgba(26,43,72,0.25);">
    <div class="px-5 pt-5 pb-4">
      <p class="text-white/50 text-xs font-medium tracking-wider uppercase mb-3">Argent disponible</p>
      <p class="text-white text-4xl font-bold tracking-tight leading-none mb-1">
        {new Intl.NumberFormat('fr-FR').format(Math.round(balance))}
      </p>
      <p class="text-white/50 text-sm mt-1">{currency} &mdash; mis à jour aujourd&apos;hui</p>
    </div>

    <!-- Weekly quick stats -->
    <div class="grid grid-cols-3 border-t border-white/10">
      <div class="px-4 py-3 text-center border-r border-white/10">
        <p class="text-white/40 text-xs mb-0.5">Entrées</p>
        <p class="text-emerald-400 font-semibold text-sm">{new Intl.NumberFormat('fr-FR').format(Math.round(weeklyIncome))}</p>
      </div>
      <div class="px-4 py-3 text-center border-r border-white/10">
        <p class="text-white/40 text-xs mb-0.5">Sorties</p>
        <p class="text-red-400 font-semibold text-sm">{new Intl.NumberFormat('fr-FR').format(Math.round(weeklyExpense))}</p>
      </div>
      <div class="px-4 py-3 text-center">
        <p class="text-white/40 text-xs mb-0.5">Net semaine</p>
        <p class="font-semibold text-sm {weeklyNet >= 0 ? 'text-emerald-400' : 'text-red-400'}">
          {weeklyNet >= 0 ? '+' : ''}{new Intl.NumberFormat('fr-FR').format(Math.round(weeklyNet))}
        </p>
      </div>
    </div>
  </div>

  <!-- Forecast Chart Card -->
  <div class="card mb-4">
    <div class="flex items-start justify-between mb-3">
      <div>
        <p class="text-xs font-medium text-navy-800/40 uppercase tracking-wider">Prévision 15 jours</p>
        <p class="text-navy-800 font-bold text-xl mt-0.5">{formatAmount(forecastBalance, currency)}</p>
      </div>
      <div class="text-right">
        <p class="text-xs text-navy-800/40">Confiance</p>
        <p class="font-semibold text-emerald-500 text-sm">{Math.round(forecastConfidence * 100)}%</p>
      </div>
    </div>
    <SparkLine data={forecastData} color="#10B981" height={56} showArea={true} />
    <div class="flex justify-between mt-2">
      <span class="text-xs text-navy-800/35">Aujourd&apos;hui</span>
      <span class="text-xs text-navy-800/35">J+15</span>
    </div>
  </div>

  <!-- Smart Alerts -->
  {#if alerts && alerts.length > 0}
    <div class="mb-4 space-y-2">
      <p class="text-xs font-semibold text-navy-800/40 uppercase tracking-wider px-1">Alertes intelligentes</p>
      {#each alerts as alert}
        <div class="card border-l-4 {riskBorderClass(riskLevel)} pl-4">
          <div class="flex items-center gap-2 mb-1">
            <span class="text-xs font-semibold px-2 py-0.5 rounded-full {riskBadgeClass(riskLevel)}">
              {riskLabel(riskLevel)}
            </span>
          </div>
          <p class="text-navy-800 text-sm leading-relaxed">{alert.message}</p>
          {#if alert.days_until}
            <p class="text-navy-800/40 text-xs mt-1">Dans {alert.days_until} jours</p>
          {/if}
        </div>
      {/each}
    </div>
  {/if}

  <!-- Weekly sparkline -->
  {#if sparkData && sparkData.length > 0}
    <div class="card mb-4">
      <p class="text-xs font-semibold text-navy-800/40 uppercase tracking-wider mb-3">Flux 7 derniers jours</p>
      <SparkLine data={sparkData} color="#1A2B48" height={44} showArea={false} />
    </div>
  {/if}

  <!-- Recent Transactions -->
  <div class="mb-4">
    <p class="text-xs font-semibold text-navy-800/40 uppercase tracking-wider px-1 mb-2">Transactions récentes</p>
    <div class="space-y-2">
      {#each recentTxns as txn}
        <div class="card flex items-center gap-3">
          <!-- Icon -->
          <div class="w-10 h-10 rounded-xl flex-shrink-0 flex items-center justify-center {txn.type === 'income' ? 'bg-emerald-500/10' : 'bg-danger/8'}">
            {#if txn.type === 'income'}
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#10B981" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
                <line x1="12" y1="19" x2="12" y2="5"/><polyline points="5 12 12 5 19 12"/>
              </svg>
            {:else}
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#EF4444" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
                <line x1="12" y1="5" x2="12" y2="19"/><polyline points="19 12 12 19 5 12"/>
              </svg>
            {/if}
          </div>
          <!-- Details -->
          <div class="flex-1 min-w-0">
            <p class="text-navy-800 text-sm font-medium truncate">{txn.note || 'Transaction'}</p>
            <p class="text-navy-800/40 text-xs">{formatDateShort(txn.date)}</p>
          </div>
          <!-- Amount -->
          <p class="font-bold text-sm flex-shrink-0 {txn.type === 'income' ? 'text-emerald-500' : 'text-danger'}">
            {txn.type === 'income' ? '+' : '-'}{new Intl.NumberFormat('fr-FR').format(txn.amount)}
          </p>
        </div>
      {/each}
    </div>
  </div>

{/if}
