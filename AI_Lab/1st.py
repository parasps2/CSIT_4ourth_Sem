/* ===========================================================
   VESSEL — Scientific Console
   =========================================================== */

/* ---------- Mode Switching ---------- */
const tabs = document.querySelectorAll('.tab');
const panels = document.querySelectorAll('.mode-panel');
tabs.forEach(tab=>{
  tab.addEventListener('click',()=>{
    tabs.forEach(t=>t.classList.remove('active'));
    panels.forEach(p=>p.classList.remove('active'));
    tab.classList.add('active');
    document.getElementById('panel-'+tab.dataset.mode).classList.add('active');
  });
});

/* ===========================================================
   1. CALCULATOR
   =========================================================== */
let expr = '';
let isDeg = false;
let memory = 0;
let invMode = false;

const calcMain = document.getElementById('calcMain');
const calcTrail = document.getElementById('calcTrail');
const angleModeEl = document.getElementById('angleMode');
const memIndicator = document.getElementById('memIndicator');

function factorial(n){
  if (n < 0) return NaN;
  if (Math.floor(n) !== n) {
    // Gamma function approximation for non-integers (Stirling)
    return gamma(n+1);
  }
  let r = 1;
  for (let i=2;i<=n;i++) r*=i;
  return r;
}
function gamma(x){
  const g = 7;
  const p = [0.99999999999980993,676.5203681218851,-1259.1392167224028,
    771.32342877765313,-176.61502916214059,12.507343278686905,
    -0.13857109526572012,9.9843695780195716e-6,1.5056327351493116e-7];
  if (x < 0.5) return Math.PI / (Math.sin(Math.PI*x) * gamma(1-x));
  x -= 1;
  let a = p[0];
  const t = x + g + 0.5;
  for (let i=1;i<g+2;i++) a += p[i]/(x+i);
  return Math.sqrt(2*Math.PI) * Math.pow(t, x+0.5) * Math.exp(-t) * a;
}

function toRad(v){ return isDeg ? v * Math.PI/180 : v; }

function sanitizeAndEval(raw){
  let s = raw;
  // factorial: number or ) followed by !
  s = s.replace(/(\d+(\.\d+)?|\))!/g, (m, num) => {
    return `__fact(${m.slice(0,-1)})`;
  });
  s = s
    .replace(/\^/g,'**')
    .replace(/π|pi/g,'Math.PI')
    .replace(/(?<![a-zA-Z])e(?![a-zA-Z(])/g,'Math.E')
    .replace(/sin\(/g,'__sin(')
    .replace(/cos\(/g,'__cos(')
    .replace(/tan\(/g,'__tan(')
    .replace(/ln\(/g,'Math.log(')
    .replace(/log\(/g,'Math.log10(')
    .replace(/sqrt\(/g,'Math.sqrt(')
    .replace(/(\d+(\.\d+)?)%/g,'($1/100)');

  const __sin = x => Math.sin(toRad(x));
  const __cos = x => Math.cos(toRad(x));
  const __tan = x => Math.tan(toRad(x));
  const __fact = x => factorial(x);

  // eslint-disable-next-line no-new-func
  const fn = new Function('__sin','__cos','__tan','__fact','Math', `return (${s});`);
  return fn(__sin,__cos,__tan,__fact,Math);
}

function updateDisplay(){
  calcMain.textContent = expr === '' ? '0' : expr;
  angleModeEl.textContent = isDeg ? 'DEG' : 'RAD';
  memIndicator.classList.toggle('hidden', memory === 0);
}

document.querySelectorAll('#panel-calc .key[data-val]').forEach(btn=>{
  btn.addEventListener('click', ()=>{
    expr += btn.dataset.val;
    updateDisplay();
  });
});

document.querySelectorAll('#panel-calc .key[data-action]').forEach(btn=>{
  btn.addEventListener('click', ()=>{
    const action = btn.dataset.action;
    if (action==='clear'){ expr=''; calcTrail.textContent='\u00A0'; }
    else if (action==='backspace'){ expr = expr.slice(0,-1); }
    else if (action==='angle'){ isDeg = !isDeg; }
    else if (action==='inv'){ invMode = !invMode; btn.style.color = invMode ? 'var(--teal)' : ''; }
    else if (action==='memclear'){ memory = 0; }
    else if (action==='memadd'){ memory += Number(calcMain.textContent)||0; }
    else if (action==='memsub'){ memory -= Number(calcMain.textContent)||0; }
    else if (action==='memrecall'){ expr += String(memory); }
    else if (action==='equals'){
      try{
        calcTrail.textContent = expr;
        const result = sanitizeAndEval(expr);
        expr = Number.isFinite(result) ? trimNumber(result) : 'Error';
      }catch(e){
        expr = 'Error';
      }
    }
    updateDisplay();
  });
});

function trimNumber(n){
  if (Math.abs(n) < 1e-12) n = 0;
  const rounded = Math.round(n*1e10)/1e10;
  return String(rounded);
}

// keyboard support
window.addEventListener('keydown', e=>{
  if (!document.getElementById('panel-calc').classList.contains('active')) return;
  if (/[0-9.+\-*/()%]/.test(e.key)){ expr += e.key; updateDisplay(); }
  else if (e.key === 'Enter'){ document.querySelector('[data-action="equals"]').click(); }
  else if (e.key === 'Backspace'){ expr = expr.slice(0,-1); updateDisplay(); }
  else if (e.key === 'Escape'){ expr=''; updateDisplay(); }
});

updateDisplay();

/* ===========================================================
   2. MATRIX CALCULATOR
   =========================================================== */
function buildGrid(containerId, rows, cols){
  const el = document.getElementById(containerId);
  el.style.gridTemplateColumns = `repeat(${cols}, auto)`;
  el.innerHTML = '';
  for (let r=0;r<rows;r++){
    for (let c=0;c<cols;c++){
      const inp = document.createElement('input');
      inp.type = 'number';
      inp.value = 0;
      inp.dataset.r = r;
      inp.dataset.c = c;
      el.appendChild(inp);
    }
  }
}
function readGrid(containerId, rows, cols){
  const el = document.getElementById(containerId);
  const inputs = el.querySelectorAll('input');
  const m = Array.from({length:rows},()=>Array(cols).fill(0));
  inputs.forEach(inp=>{
    m[+inp.dataset.r][+inp.dataset.c] = parseFloat(inp.value) || 0;
  });
  return m;
}

document.getElementById('buildA').addEventListener('click', ()=>{
  buildGrid('gridA', +document.getElementById('aRows').value, +document.getElementById('aCols').value);
});
document.getElementById('buildB').addEventListener('click', ()=>{
  buildGrid('gridB', +document.getElementById('bRows').value, +document.getElementById('bCols').value);
});
buildGrid('gridA',2,2);
buildGrid('gridB',2,2);

function matAdd(A,B){
  if (A.length!==B.length || A[0].length!==B[0].length) throw new Error('Dimension mismatch');
  return A.map((row,r)=>row.map((v,c)=>v+B[r][c]));
}
function matSub(A,B){
  if (A.length!==B.length || A[0].length!==B[0].length) throw new Error('Dimension mismatch');
  return A.map((row,r)=>row.map((v,c)=>v-B[r][c]));
}
function matMul(A,B){
  if (A[0].length !== B.length) throw new Error('Inner dimensions must match');
  const result = Array.from({length:A.length},()=>Array(B[0].length).fill(0));
  for (let i=0;i<A.length;i++)
    for (let j=0;j<B[0].length;j++)
      for (let k=0;k<B.length;k++)
        result[i][j] += A[i][k]*B[k][j];
  return result;
}
function matTrans(A){
  return A[0].map((_,c)=>A.map(row=>row[c]));
}
function matDet(A){
  const n = A.length;
  if (n !== A[0].length) throw new Error('Matrix must be square');
  if (n === 1) return A[0][0];
  if (n === 2) return A[0][0]*A[1][1]-A[0][1]*A[1][0];
  let det = 0;
  for (let c=0;c<n;c++){
    det += ((c%2===0)?1:-1) * A[0][c] * matDet(minor(A,0,c));
  }
  return det;
}
function minor(A,row,col){
  return A.filter((_,r)=>r!==row).map(r=>r.filter((_,c)=>c!==col));
}
function matInv(A){
  const n = A.length;
  if (n !== A[0].length) throw new Error('Matrix must be square');
  const det = matDet(A);
  if (Math.abs(det) < 1e-12) throw new Error('Matrix is singular (det = 0)');
  if (n === 1) return [[1/A[0][0]]];
  const adj = Array.from({length:n},()=>Array(n).fill(0));
  for (let r=0;r<n;r++){
    for (let c=0;c<n;c++){
      const cof = ((r+c)%2===0?1:-1) * matDet(minor(A,r,c));
      adj[c][r] = cof; // transpose for adjugate
    }
  }
  return adj.map(row=>row.map(v=>v/det));
}
function matRank(A){
  const M = A.map(row=>row.slice());
  const rows = M.length, cols = M[0].length;
  let rank = 0;
  for (let col=0; col<cols && rank<rows; col++){
    let pivot = -1;
    for (let r=rank;r<rows;r++){
      if (Math.abs(M[r][col]) > 1e-9){ pivot = r; break; }
    }
    if (pivot === -1) continue;
    [M[rank],M[pivot]] = [M[pivot],M[rank]];
    for (let r=0;r<rows;r++){
      if (r!==rank){
        const factor = M[r][col]/M[rank][col];
        for (let c=col;c<cols;c++) M[r][c] -= factor*M[rank][c];
      }
    }
    rank++;
  }
  return rank;
}
function matTrace(A){
  if (A.length !== A[0].length) throw new Error('Matrix must be square');
  let t=0;
  for (let i=0;i<A.length;i++) t += A[i][i];
  return t;
}

function renderMatrixResult(M){
  const el = document.getElementById('gridResult');
  document.getElementById('scalarResult').textContent = '';
  el.style.gridTemplateColumns = `repeat(${M[0].length}, auto)`;
  el.innerHTML = '';
  M.forEach(row=>row.forEach(v=>{
    const cell = document.createElement('div');
    cell.className = 'cell';
    cell.textContent = trimNumber(v);
    el.appendChild(cell);
  }));
}
function renderScalarResult(label, value){
  document.getElementById('gridResult').innerHTML = '';
  document.getElementById('scalarResult').textContent = `${label} = ${trimNumber(value)}`;
}
function renderError(msg){
  document.getElementById('gridResult').innerHTML = '';
  const el = document.getElementById('scalarResult');
  el.style.color = 'var(--danger)';
  el.textContent = '⚠ ' + msg;
}

document.querySelectorAll('.op-chip').forEach(btn=>{
  btn.addEventListener('click', ()=>{
    document.getElementById('scalarResult').style.color = 'var(--teal)';
    const aR = +document.getElementById('aRows').value, aC = +document.getElementById('aCols').value;
    const bR = +document.getElementById('bRows').value, bC = +document.getElementById('bCols').value;
    const A = readGrid('gridA', aR, aC);
    const B = readGrid('gridB', bR, bC);
    try{
      switch(btn.dataset.op){
        case 'add': renderMatrixResult(matAdd(A,B)); break;
        case 'sub': renderMatrixResult(matSub(A,B)); break;
        case 'mul': renderMatrixResult(matMul(A,B)); break;
        case 'detA': renderScalarResult('det(A)', matDet(A)); break;
        case 'detB': renderScalarResult('det(B)', matDet(B)); break;
        case 'invA': renderMatrixResult(matInv(A)); break;
        case 'invB': renderMatrixResult(matInv(B)); break;
        case 'transA': renderMatrixResult(matTrans(A)); break;
        case 'transB': renderMatrixResult(matTrans(B)); break;
        case 'rankA': renderScalarResult('rank(A)', matRank(A)); break;
        case 'traceA': renderScalarResult('tr(A)', matTrace(A)); break;
      }
    }catch(err){
      renderError(err.message);
    }
  });
});

/* ===========================================================
   3. STATISTICS
   =========================================================== */
document.getElementById('computeStats').addEventListener('click', ()=>{
  const raw = document.getElementById('statData').value;
  const data = raw.split(/[\s,]+/).map(s=>parseFloat(s)).filter(v=>!isNaN(v));
  if (data.length === 0) return;

  const n = data.length;
  const sum = data.reduce((a,b)=>a+b,0);
  const mean = sum/n;
  const sorted = [...data].sort((a,b)=>a-b);
  const median = n%2===0 ? (sorted[n/2-1]+sorted[n/2])/2 : sorted[(n-1)/2];

  const freq = {};
  data.forEach(v=>freq[v]=(freq[v]||0)+1);
  const maxFreq = Math.max(...Object.values(freq));
  const modes = Object.keys(freq).filter(k=>freq[k]===maxFreq);
  const mode = maxFreq <= 1 ? 'none' : modes.join(', ');

  const min = Math.min(...data), max = Math.max(...data);
  const range = max-min;

  const varP = data.reduce((a,v)=>a+(v-mean)**2,0)/n;
  const stdP = Math.sqrt(varP);
  const varS = n>1 ? data.reduce((a,v)=>a+(v-mean)**2,0)/(n-1) : 0;
  const stdS = Math.sqrt(varS);
  const stErr = stdS/Math.sqrt(n);

  const skew = n>2 ? (data.reduce((a,v)=>a+((v-mean)/stdP)**3,0)/n) : 0;

  const set = (id,val)=>document.getElementById(id).textContent = typeof val==='number' ? trimNumber(val) : val;
  set('stat-n', n);
  set('stat-sum', sum);
  set('stat-mean', mean);
  set('stat-median', median);
  set('stat-mode', mode);
  set('stat-range', range);
  set('stat-min', min);
  set('stat-max', max);
  set('stat-varp', varP);
  set('stat-stdp', stdP);
  set('stat-vars', varS);
  set('stat-stds', stdS);
  set('stat-sterr', stErr);
  set('stat-skew', skew);
});

/* ===========================================================
   4. PHYSICS CONSTANTS (CODATA values)
   =========================================================== */
const PHYSICS_CONSTANTS = [
  { name:'Speed of light in vacuum', symbol:'c', value:'2.99792458 × 10⁸', unit:'m/s' },
  { name:'Planck constant', symbol:'h', value:'6.62607015 × 10⁻³⁴', unit:'J·s' },
  { name:'Reduced Planck constant', symbol:'ħ', value:'1.054571817 × 10⁻³⁴', unit:'J·s' },
  { name:'Gravitational constant', symbol:'G', value:'6.67430 × 10⁻¹¹', unit:'m³/(kg·s²)' },
  { name:'Elementary charge', symbol:'e', value:'1.602176634 × 10⁻¹⁹', unit:'C' },
  { name:'Electron mass', symbol:'mₑ', value:'9.1093837015 × 10⁻³¹', unit:'kg' },
  { name:'Proton mass', symbol:'mₚ', value:'1.67262192369 × 10⁻²⁷', unit:'kg' },
  { name:'Neutron mass', symbol:'mₙ', value:'1.67492749804 × 10⁻²⁷', unit:'kg' },
  { name:'Avogadro constant', symbol:'Nₐ', value:'6.02214076 × 10²³', unit:'1/mol' },
  { name:'Boltzmann constant', symbol:'k', value:'1.380649 × 10⁻²³', unit:'J/K' },
  { name:'Gas constant', symbol:'R', value:'8.314462618', unit:'J/(mol·K)' },
  { name:'Faraday constant', symbol:'F', value:'96485.33212', unit:'C/mol' },
  { name:'Vacuum permittivity', symbol:'ε₀', value:'8.8541878128 × 10⁻¹²', unit:'F/m' },
  { name:'Vacuum permeability', symbol:'μ₀', value:'1.25663706212 × 10⁻⁶', unit:'N/A²' },
  { name:'Coulomb constant', symbol:'k_e', value:'8.9875517923 × 10⁹', unit:'N·m²/C²' },
  { name:'Stefan–Boltzmann constant', symbol:'σ', value:'5.670374419 × 10⁻⁸', unit:'W/(m²·K⁴)' },
  { name:'Standard gravity', symbol:'g', value:'9.80665', unit:'m/s²' },
  { name:'Atomic mass unit', symbol:'u', value:'1.66053906660 × 10⁻²⁷', unit:'kg' },
  { name:'Rydberg constant', symbol:'R∞', value:'1.0973731568160 × 10⁷', unit:'1/m' },
  { name:'Bohr radius', symbol:'a₀', value:'5.29177210903 × 10⁻¹¹', unit:'m' },
  { name:'Fine-structure constant', symbol:'α', value:'7.2973525693 × 10⁻³', unit:'(dimensionless)' },
  { name:'Wien displacement constant', symbol:'b', value:'2.897771955 × 10⁻³', unit:'m·K' },
  { name:'Electron volt', symbol:'eV', value:'1.602176634 × 10⁻¹⁹', unit:'J' },
  { name:'Planck length', symbol:'ℓ_P', value:'1.616255 × 10⁻³⁵', unit:'m' },
  { name:'Planck time', symbol:'t_P', value:'5.391247 × 10⁻⁴⁴', unit:'s' },
  { name:'Planck mass', symbol:'m_P', value:'2.176434 × 10⁻⁸', unit:'kg' },
  { name:'Astronomical unit', symbol:'AU', value:'1.495978707 × 10¹¹', unit:'m' },
  { name:'Light year', symbol:'ly', value:'9.4607 × 10¹⁵', unit:'m' },
  { name:'Parsec', symbol:'pc', value:'3.0857 × 10¹⁶', unit:'m' },
  { name:'Solar mass', symbol:'M☉', value:'1.98892 × 10³⁰', unit:'kg' },
];

const constGrid = document.getElementById('constGrid');
function renderConstants(list){
  constGrid.innerHTML = '';
  list.forEach(c=>{
    const card = document.createElement('div');
    card.className = 'const-card';
    card.innerHTML = `
      <div class="const-name">${c.name}</div>
      <div class="const-symbol">${c.symbol}</div>
      <div class="const-value">${c.value}</div>
      <div class="const-unit">${c.unit}</div>
    `;
    card.addEventListener('click', ()=>{
      // pull a usable plain numeric form into the calculator
      const numeric = c.value.replace(/×\s*10([⁻⁰¹²³⁴⁵⁶⁷⁸⁹]+)/, (m, exp)=>{
        const map = {'⁰':'0','¹':'1','²':'2','³':'3','⁴':'4','⁵':'5','⁶':'6','⁷':'7','⁸':'8','⁹':'9','⁻':'-'};
        const e = exp.split('').map(ch=>map[ch]).join('');
        return `e${e}`;
      }).replace(/\s/g,'');
      const num = parseFloat(numeric);
      if (!isNaN(num)){
        expr += num.toString();
        document.querySelector('.tab[data-mode="calc"]').click();
        updateDisplay();
      }
    });
    constGrid.appendChild(card);
  });
}
renderConstants(PHYSICS_CONSTANTS);

document.getElementById('constSearch').addEventListener('input', e=>{
  const q = e.target.value.toLowerCase();
  renderConstants(PHYSICS_CONSTANTS.filter(c=>
    c.name.toLowerCase().includes(q) || c.symbol.toLowerCase().includes(q)
  ));
});