/**
 * DIT 2026 — E-P-I-A-S x SAE Matrix Visualization.
 * Renders the 6x5 matrix as an HTML table with highlighted position.
 */

function renderMatrix(containerId, placement) {
    const container = document.getElementById(containerId);
    if (!container) return;

    const levels = [0, 1, 2, 3, 4, 5];
    const stages = ['E', 'P', 'I', 'A', 'S'];

    const levelLabels = {
        0: 'L0\nManual',
        1: 'L1\nAI-Assisted',
        2: 'L2\nPartially\nAutomated',
        3: 'L3\nGuided\nAutomation',
        4: 'L4\nMostly\nAutomated',
        5: 'L5\nFull\nAutomation',
    };

    const stageLabels = {
        'E': 'Explorer',
        'P': 'Practitioner',
        'I': 'Integrator',
        'A': 'Architect',
        'S': 'Steward',
    };

    const stageEmojis = {
        'E': '\u2776',  // circled 1
        'P': '\u2777',
        'I': '\u2778',
        'A': '\u2779',
        'S': '\u277A',
    };

    const currentLevel = placement.sae_level;
    const currentStage = placement.epias_stage;
    const nextStep = placement.growth_path && placement.growth_path.next;

    let html = '<table class="matrix-table">';

    // Header row
    html += '<tr><th></th>';
    levels.forEach(level => {
        const label = levelLabels[level].replace(/\n/g, '<br>');
        const isCurrent = level === currentLevel;
        html += `<th style="${isCurrent ? 'background: var(--primary-light); color: var(--primary);' : ''}">${label}</th>`;
    });
    html += '</tr>';

    // Data rows
    stages.forEach(stage => {
        const isStageCurrent = stage === currentStage;
        html += `<tr>`;
        html += `<th style="${isStageCurrent ? 'background: #d1fae5; color: var(--success);' : ''}">
            ${stageEmojis[stage]} ${stageLabels[stage]}
        </th>`;

        levels.forEach(level => {
            const isCurrent = level === currentLevel && stage === currentStage;
            const isNext = nextStep &&
                level === nextStep.sae_level &&
                stage === nextStep.epias_stage;

            let classes = 'matrix-cell';
            if (isCurrent) classes += ' current';
            else if (isNext) classes += ' next-step';

            let title = '';
            if (isCurrent) title = 'You are here';
            else if (isNext) title = 'Next step';

            html += `<td class="${classes}" title="${title}">`;
            if (isCurrent) {
                html += '<span style="font-size: 1.2rem;">You</span>';
            } else if (isNext) {
                html += '<span style="font-size: 0.9rem; color: var(--success);">Next</span>';
            }
            html += '</td>';
        });

        html += '</tr>';
    });

    html += '</table>';

    // Legend
    html += `
        <div style="display: flex; gap: 1.5rem; margin-top: 0.75rem; font-size: 0.8rem; color: var(--text-muted);">
            <span><span style="display: inline-block; width: 12px; height: 12px; background: var(--primary-light); border: 2px solid var(--primary); border-radius: 2px; vertical-align: middle;"></span> Your position</span>
            <span><span style="display: inline-block; width: 12px; height: 12px; background: #d1fae5; border: 2px dashed var(--success); border-radius: 2px; vertical-align: middle;"></span> Suggested next step</span>
        </div>
    `;

    container.innerHTML = html;
}
