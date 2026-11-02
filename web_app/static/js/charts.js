// charts.js — Global Chart.js defaults for the dark theme
// Individual page charts are inlined in each template's {% block scripts %}

if (typeof Chart !== 'undefined') {
  Chart.defaults.color = '#8fa3b8';
  Chart.defaults.borderColor = '#1e3a5f';
  Chart.defaults.backgroundColor = '#112240';
  Chart.defaults.font.family = "'Segoe UI', system-ui, sans-serif";
  Chart.defaults.font.size = 12;
}
