/**
 * Heatmap visualization — fetches aggregated results and renders a colored 6x5 grid.
 */
(function() {
    'use strict';

    const LEVELS = [0, 1, 2, 3, 4, 5];
    const LEVEL_NAMES = {
        0: 'L0: Manual', 1: 'L1: AI-Assisted', 2: 'L2: Partial',
        3: 'L3: Guided', 4: 'L4: Mostly Auto', 5: 'L5: Full Auto'
    };
    const STAGES = ['E', 'P', 'I', 'A', 'S'];
    const STAGE_NAMES = {E: 'Explorer', P: 'Practitioner', I: 'Integrator', A: 'Architect', S: 'Steward'};

    function cellColor(count, maxCount) {
        if (count === 0) return '#f8fafc';
        const intensity = 0.15 + 0.75 * (count / maxCount);
        return `hsla(221, 83%, 53%, ${intensity})`;
    }

    function textColor(count, maxCount) {
        if (count === 0) return '#94a3b8';
        const intensity = count / maxCount;
        return intensity > 0.5 ? '#ffffff' : '#1e293b';
    }

    function renderHeatmap(data) {
        const counts = data.counts;
        const maxCount = Math.max(1, ...Object.values(counts));
        const container = document.getElementById('heatmapContainer');
        document.getElementById('totalCount').textContent = data.total;

        let html = '<table class="matrix-table"><thead><tr><th></th>';
        STAGES.forEach(s => {
            html += `<th>${s}<br><small>${STAGE_NAMES[s]}</small></th>`;
        });
        html += '</tr></thead><tbody>';

        LEVELS.forEach(level => {
            html += `<tr><th>${LEVEL_NAMES[level]}</th>`;
            STAGES.forEach(stage => {
                const key = `${level}_${stage}`;
                const count = counts[key] || 0;
                const bg = cellColor(count, maxCount);
                const fg = textColor(count, maxCount);
                html += `<td class="heatmap-cell" style="background:${bg};color:${fg}">${count || ''}</td>`;
            });
            html += '</tr>';
        });

        html += '</tbody></table>';
        container.innerHTML = html;
    }

    fetch('/api/heatmap')
        .then(r => r.json())
        .then(renderHeatmap)
        .catch(err => {
            console.error('Failed to load heatmap:', err);
            document.getElementById('heatmapContainer').innerHTML =
                '<p style="text-align:center;color:var(--text-muted);">Could not load heatmap data.</p>';
        });
})();
