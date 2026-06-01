<script>
  export let data = [];
  export let width = 320;
  export let height = 56;
  export let color = '#10B981';
  export let showArea = true;

  const uid = Math.random().toString(36).slice(2, 8);

  $: pts = (() => {
    if (data.length < 2) return [];
    const min = Math.min(...data);
    const max = Math.max(...data);
    const range = max - min || 1;
    const step = width / (data.length - 1);
    const pad = 4;
    return data.map((v, i) => ({
      x: i * step,
      y: pad + ((max - v) / range) * (height - pad * 2),
    }));
  })();

  $: linePath = (() => {
    if (pts.length < 2) return '';
    return pts.map((p, i) => `${i === 0 ? 'M' : 'L'}${p.x.toFixed(1)},${p.y.toFixed(1)}`).join(' ');
  })();

  $: areaPath = (() => {
    if (pts.length < 2) return '';
    const line = pts.map((p, i) => `${i === 0 ? 'M' : 'L'}${p.x.toFixed(1)},${p.y.toFixed(1)}`).join(' ');
    return `${line} L${(pts[pts.length - 1].x).toFixed(1)},${height} L0,${height} Z`;
  })();
</script>

<svg
  viewBox="0 0 {width} {height}"
  class="w-full"
  style="height: {height}px; overflow: visible;"
  aria-hidden="true"
>
  <defs>
    <linearGradient id="area-grad-{uid}" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color={color} stop-opacity="0.18"/>
      <stop offset="100%" stop-color={color} stop-opacity="0.01"/>
    </linearGradient>
  </defs>

  <!-- Area fill -->
  {#if showArea && areaPath}
    <path d={areaPath} fill="url(#area-grad-{uid})" />
  {/if}

  <!-- Line -->
  {#if linePath}
    <path
      d={linePath}
      fill="none"
      stroke={color}
      stroke-width="2"
      stroke-linecap="round"
      stroke-linejoin="round"
    />
  {/if}

  <!-- End dot -->
  {#if pts.length > 0}
    {@const last = pts[pts.length - 1]}
    <circle cx={last.x} cy={last.y} r="3.5" fill={color} />
    <circle cx={last.x} cy={last.y} r="6" fill={color} fill-opacity="0.2" />
  {/if}
</svg>
