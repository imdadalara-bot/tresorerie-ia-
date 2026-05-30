<script>
  export let data = [];
  export let width = 280;
  export let height = 40;

  $: points = (() => {
    if (data.length < 2) return '';
    const max = Math.max(...data.map(Math.abs), 1);
    const step = width / (data.length - 1);
    return data
      .map((v, i) => {
        const x = i * step;
        const y = height / 2 - (v / max) * (height / 2 - 4);
        return `${x},${y}`;
      })
      .join(' ');
  })();

  $: fillPoints = (() => {
    if (data.length < 2) return '';
    const max = Math.max(...data.map(Math.abs), 1);
    const step = width / (data.length - 1);
    const pts = data.map((v, i) => {
      const x = i * step;
      const y = height / 2 - (v / max) * (height / 2 - 4);
      return `${x},${y}`;
    });
    return `0,${height / 2} ${pts.join(' ')} ${width},${height / 2}`;
  })();
</script>

<svg viewBox="0 0 {width} {height}" class="w-full" style="height: {height}px;">
  <!-- Zero line -->
  <line x1="0" y1={height / 2} x2={width} y2={height / 2} stroke="#e5e7eb" stroke-width="1" />
  <!-- Fill -->
  {#if fillPoints}
    <polygon points={fillPoints} fill="#3b82f6" opacity="0.1" />
  {/if}
  <!-- Line -->
  {#if points}
    <polyline points={points} fill="none" stroke="#3b82f6" stroke-width="2" />
  {/if}
</svg>
