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
    return new Intl.NumberFormat('fr-FR').format(Math.round(amount)) + ' ' + currency;
  }

  function riskColor(level) {
    if (level === 'HIGH') return 'text-red-600 bg-red-50 border-red-200';
    if (level === 'MEDIUM') return 'text-yellow-600 bg-yellow-50 border-yellow-200';
    return 'text-green-600 bg-green-50 border-green-200';
  }

  function riskIcon(level) {
    if (level === 'HIGH') return '🔴';
    if (level === 'MEDIUM') return '🟡';
    return '🟢';
  }
</script>

{#if loading}
  <div class="flex items-center justify-center py-12">
    <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600"></div>
  </div>
{:else if error}
  <div class="bg-red-50 text-red-600 p-4 rounded-lg text-center">{error}</div>
{:else if dashboard}
  {#if offline}
    <div class="bg-yellow-50 text-yellow-700 text-xs p-2 rounded-lg mb-3 text-center">
      Mode hors-ligne — données du cache
    </div>
  {/if}

  <!-- Balance card -->
  <div class="card mb-3">
    <p class="text-sm text-gray-500">Aujourd'hui</p>
    <p class="text-3xl font-bold text-gray-900 mt-1">
      {formatAmount(dashboard.current_balance, dashboard.currency)}
    </p>
  </div>

  <!-- Weekly summary -->
  <div class="card mb-3">
    <p class="text-sm text-gray-500 mb-2">Cette semaine</p>
    <div class="space-y-1">
      <div class="flex justify-between">
        <span class="text-sm text-green-600">+ Entrées</span>
        <span class="font-medium text-green-600">
          {formatAmount(dashboard.weekly_income, dashboard.currency)}
        </span>
      </div>
      <div class="flex justify-between">
        <span class="text-sm text-red-500">- Sorties</span>
        <span class="font-medium text-red-500">
          {formatAmount(dashboard.weekly_expense, dashboard.currency)}
        </span>
      </div>
      <hr class="my-1" />
      <div class="flex justify-between">
        <span class="text-sm font-medium">= Net</span>
        <span class="font-bold {dashboard.weekly_net >= 0 ? 'text-green-600' : 'text-red-500'}">
          {dashboard.weekly_net >= 0 ? '+' : ''}{formatAmount(dashboard.weekly_net, dashboard.currency)}
        </span>
      </div>
    </div>
  </div>

  <!-- 7-day sparkline -->
  {#if dashboard.daily_flows_7d && dashboard.daily_flows_7d.length > 0}
    <div class="card mb-3">
      <p class="text-sm text-gray-500 mb-2">Flux 7 derniers jours</p>
      <SparkLine data={dashboard.daily_flows_7d.map(d => d.net)} />
    </div>
  {/if}

  <!-- Forecast / Risk card -->
  <div class="card mb-3 border {riskColor(dashboard.risk_level)}">
    <div class="flex items-center gap-2 mb-2">
      <span class="text-lg">{riskIcon(dashboard.risk_level)}</span>
      <p class="text-sm font-medium">Prévision 15 jours</p>
    </div>
    {#if dashboard.forecast_15d && dashboard.forecast_15d.length > 0}
      {@const lastForecast = dashboard.forecast_15d[dashboard.forecast_15d.length - 1]}
      <p class="text-xl font-bold">
        {formatAmount(lastForecast.predicted_balance, dashboard.currency)}
      </p>
      <p class="text-xs text-gray-500 mt-1">
        Confiance: {Math.round(lastForecast.confidence * 100)}%
      </p>
    {/if}
  </div>

  <!-- Alerts -->
  {#if dashboard.alerts && dashboard.alerts.length > 0}
    <div class="space-y-2 mb-3">
      {#each dashboard.alerts as alert}
        <div class="card border-l-4 border-l-red-500 bg-red-50">
          <p class="text-sm text-red-700">{alert.message}</p>
          {#if alert.days_until}
            <p class="text-xs text-red-500 mt-1">Dans {alert.days_until} jours</p>
          {/if}
        </div>
      {/each}
    </div>
  {/if}
{/if}
