import { FormEvent, useEffect, useState } from 'react'
import { NavLink, Route, Routes, useLocation } from 'react-router-dom'
import {
  Activity, ArrowRight, BarChart3, Beaker, BookOpen, Boxes, ChevronRight, CircleHelp,
  FileText, FlaskConical, Gauge, Info, Layers3, LayoutDashboard, Menu, PanelLeftClose,
  PanelLeftOpen, Settings2, Sparkles, X,
} from 'lucide-react'
import { TextureBackground } from './components/TextureBackground'
import { API_BASE_URL, apiRequest, checkHealth } from './api/client'

type NavItem = { label: string; path: string; icon: typeof Activity; section?: string }
type Material = {
  name: string; family: string; reinforcement: string; matrix: string; form: string
  status: string; valid_temperature_range_k: [number, number]; supported_models: string[]
  fibre_modulus_pa?: number; matrix_modulus_pa?: number; fibre_alpha_per_k?: number
  matrix_alpha_per_k?: number; poisson12?: number; fibre_shear_modulus_pa?: number
  matrix_shear_modulus_pa?: number; density_kg_m3?: number; source?: string
}
type Simulation = {
  id: number; material_name: string; created_at: string; request_payload: Record<string, unknown>
  result_payload: Record<string, any>
}
type SimulationResult = Record<string, any>

const navItems: NavItem[] = [
  { label: 'Dashboard', path: '/', icon: LayoutDashboard, section: 'Workspace' },
  { label: 'Material explorer', path: '/materials', icon: Boxes },
  { label: 'Material builder', path: '/builder', icon: Beaker },
  { label: 'Thermal simulator', path: '/thermal', icon: Gauge },
  { label: 'Laminate designer', path: '/laminate', icon: Layers3 },
  { label: 'Simulation comparison', path: '/compare', icon: BarChart3, section: 'Analysis' },
  { label: 'Results & reports', path: '/reports', icon: FileText },
  { label: 'Methodology', path: '/methodology', icon: BookOpen, section: 'Reference' },
  { label: 'Settings', path: '/settings', icon: Settings2 },
  { label: 'About', path: '/about', icon: Info },
]

const pageTitles: Record<string, string> = {
  '/': 'Dashboard', '/materials': 'Material explorer', '/builder': 'Material builder',
  '/thermal': 'Thermal simulator', '/laminate': 'Laminate designer',
  '/compare': 'Simulation comparison', '/reports': 'Results & reports',
  '/methodology': 'Methodology', '/settings': 'Settings', '/about': 'About',
}

async function loadMaterials() { return apiRequest<Material[]>('/materials') }
async function loadSimulations() { return apiRequest<Simulation[]>('/simulations') }
function formatPa(value?: number) { return value == null ? '—' : `${(value / 1e9).toFixed(2)} GPa` }
function formatDate(value: string) { return new Date(value).toLocaleString() }

function AppShell() {
  const [collapsed, setCollapsed] = useState(false)
  const [mobileOpen, setMobileOpen] = useState(false)
  const location = useLocation()
  const closeMobile = () => setMobileOpen(false)
  useEffect(() => {
    if (!mobileOpen) return
    const closeOnEscape = (event: KeyboardEvent) => {
      if (event.key === 'Escape') closeMobile()
    }
    document.addEventListener('keydown', closeOnEscape)
    document.body.classList.add('navigation-locked')
    return () => {
      document.removeEventListener('keydown', closeOnEscape)
      document.body.classList.remove('navigation-locked')
    }
  }, [mobileOpen])
  useEffect(() => { closeMobile() }, [location.pathname])
  return <div className={`app-shell ${collapsed ? 'sidebar-collapsed' : ''} ${mobileOpen ? 'drawer-open' : ''}`}>
    <TextureBackground />
    <aside className="sidebar">
      <div className="sidebar-top">
        <NavLink to="/" className="brand" onClick={closeMobile}><span className="brand-mark">TC</span><span className="brand-text"><strong>Thermo</strong>Composite <small>LAB / 01</small></span></NavLink>
        <button className="icon-button sidebar-close" onClick={() => setCollapsed(!collapsed)} aria-label={collapsed ? 'Expand sidebar' : 'Collapse sidebar'} aria-expanded={!collapsed}>{collapsed ? <PanelLeftOpen size={18} /> : <PanelLeftClose size={18} />}</button>
      </div>
      <nav className="navigation" aria-label="Primary navigation">{navItems.map((item, index) => <div key={item.path}>{item.section && <div className="nav-section">{item.section}</div>}<NavLink to={item.path} onClick={closeMobile} className={({ isActive }) => `nav-link ${isActive ? 'active' : ''}`} end={item.path === '/'}><item.icon size={17} strokeWidth={1.8} /><span>{item.label}</span></NavLink>{index === 4 && <div className="nav-divider" />}</div>)}</nav>
      <div className="sidebar-footer"><div className="api-status"><span className="status-dot" /> API connection <span className="api-url">{API_BASE_URL}</span></div><p>Preliminary engineering workspace</p></div>
    </aside>
    {mobileOpen && <button className="drawer-scrim" onClick={closeMobile} aria-label="Close navigation" />}
    <main className="main-content">
      <header className="topbar"><button className="icon-button mobile-menu" onClick={() => setMobileOpen(!mobileOpen)} aria-label={mobileOpen ? 'Close navigation' : 'Open navigation'} aria-expanded={mobileOpen}>{mobileOpen ? <X size={20} /> : <Menu size={20} />}</button><div className="breadcrumbs"><span>Workspace</span><ChevronRight size={14} /><strong>{pageTitles[location.pathname] || 'Not found'}</strong></div><div className="topbar-actions"><button className="icon-button" aria-label="Help"><CircleHelp size={18} /></button><div className="avatar" aria-label="Rudrajyoti Paul">RP</div></div></header>
      <div className="content"><Routes><Route path="/" element={<Dashboard />} /><Route path="/materials" element={<MaterialExplorer />} /><Route path="/builder" element={<MaterialBuilder />} /><Route path="/thermal" element={<ThermalSimulator laminate={false} />} /><Route path="/laminate" element={<ThermalSimulator laminate />} /><Route path="/compare" element={<Comparison />} /><Route path="/reports" element={<Reports />} /><Route path="/methodology" element={<Methodology />} /><Route path="/settings" element={<Settings />} /><Route path="/about" element={<About />} /><Route path="*" element={<NotFound />} /></Routes></div>
    </main>
  </div>
}

function PageIntro({ eyebrow, title, description }: { eyebrow: string; title: string; description: string }) {
  return <div className="page-intro"><div className="eyebrow">{eyebrow}</div><h1>{title}</h1><p>{description}</p></div>
}
function ErrorState({ error, retry }: { error: string; retry?: () => void }) { return <div className="error-state"><strong>Unable to load this workspace</strong><span>{error}</span>{retry && <button className="button button-quiet" onClick={retry}>Retry</button>}</div> }
function Loading() { return <div className="empty-state">Loading verified data…</div> }

function Dashboard() {
  const [runs, setRuns] = useState<Simulation[]>([])
  const [error, setError] = useState('')
  useEffect(() => { loadSimulations().then(setRuns).catch((e) => setError(e.message)) }, [])
  return <div className="dashboard"><section className="hero"><div className="hero-copy"><div className="eyebrow"><Sparkles size={13} /> Decision-ready material intelligence</div><h1>Understand how<br /><em>materials respond.</em></h1><p>ThermoComposite Lab keeps thermal and laminate calculations transparent, traceable, and easy to interrogate.</p><div className="hero-actions"><NavLink className="button button-primary" to="/thermal">Run a simulation <ArrowRight size={16} /></NavLink><NavLink className="button button-quiet" to="/methodology">Read the methodology</NavLink></div></div><div className="hero-orbit"><div className="orbit-ring ring-one" /><div className="orbit-ring ring-two" /><div className="orbit-core"><FlaskConical size={28} /><span>CLT<br />READY</span></div></div></section>
    <div className="section-heading"><div><div className="eyebrow">Workspace pulse</div><h2>Current study</h2></div><span className="muted mono">{runs.length ? `${runs.length} SAVED RUNS` : 'NO RUNS SAVED'}</span></div>
    {error ? <ErrorState error={error} /> : <div className="metric-grid">{[['Saved simulations', String(runs.length), 'Persisted API records'], ['Latest material', runs[0]?.material_name || '—', 'From the latest run'], ['Latest ΔT', runs[0] ? `${runs[0].result_payload.delta_temperature_k} K` : '—', 'Returned by engine'], ['Latest record', runs[0] ? `#${runs[0].id}` : '—', 'Traceable result']].map(([label, value, note]) => <div className="metric-card" key={label}><span className="metric-label">{label}</span><strong>{value}</strong><span className="metric-note">{note}</span></div>)}</div>}
    <section className="lower-grid"><div className="panel"><div className="panel-heading"><div><div className="eyebrow">Recent calculations</div><h3>Run history</h3></div></div>{!runs.length && !error ? <div className="empty-state">No persisted simulations yet. Run a study to populate this view.</div> : <RunTable runs={runs.slice(0, 5)} />}</div><div className="panel quick-panel"><div className="eyebrow">Quick actions</div><h3>Move from question to model.</h3>{[['Material catalogue','Review verified reference systems.','/materials',Boxes],['Thermal simulator','Calculate returned thermal response.','/thermal',Gauge],['Laminate designer','Explore stacking sequences.','/laminate',Layers3]].map(([title, desc, path, icon]) => { const Icon = icon as typeof Activity; return <NavLink className="quick-action" to={path as string} key={title as string}><span className="quick-icon"><Icon size={17} /></span><span><strong>{title as string}</strong><small>{desc as string}</small></span><ArrowRight size={15} /></NavLink> })}</div></section>
    <footer className="app-footer"><span>THERMOCOMPOSITE LAB / v0.1</span><span>Built for transparent engineering decisions · <strong>Rudrajyoti Paul</strong></span></footer></div>
}

function MaterialExplorer() {
  const [materials, setMaterials] = useState<Material[]>([]); const [query, setQuery] = useState(''); const [selected, setSelected] = useState<Material | null>(null); const [error, setError] = useState(''); const [detailLoading, setDetailLoading] = useState(false)
  const fetchData = () => loadMaterials().then(setMaterials).catch((e) => setError(e.message))
  useEffect(() => { fetchData() }, [])
  const selectMaterial = async (name: string) => {
    setDetailLoading(true)
    setError('')
    try { setSelected(await apiRequest<Material>(`/materials/${encodeURIComponent(name)}`)) }
    catch (e) { setError(e instanceof Error ? e.message : 'Material detail request failed.') }
    finally { setDetailLoading(false) }
  }
  const filtered = materials.filter((m) => `${m.name} ${m.family} ${m.reinforcement} ${m.matrix}`.toLowerCase().includes(query.toLowerCase()))
  return <div className="page-frame"><PageIntro eyebrow="Material library" title="Explore material systems." description="Browse the verified registry, its units, supported models, and data provenance." />{error ? <ErrorState error={error} retry={fetchData} /> : !materials.length ? <Loading /> : <div className="workspace-grid"><section className="panel"><div className="toolbar"><input aria-label="Search materials" value={query} onChange={(e) => setQuery(e.target.value)} placeholder="Search material, fibre or matrix" /><span className="muted mono">{filtered.length} SYSTEMS</span></div><div className="material-list">{filtered.map((m) => <button className={`material-row ${selected?.name === m.name ? 'selected' : ''}`} key={m.name} onClick={() => selectMaterial(m.name)}><span><strong>{m.name}</strong><small>{m.family} · {m.form}</small></span><span className="pill">{m.status}</span></button>)}</div>{!filtered.length && <div className="empty-state">No registered materials match this search.</div>}</section><section className="panel detail-panel">{detailLoading ? <Loading /> : selected ? <><div className="eyebrow">Verified material detail</div><h3>{selected.name}</h3><p className="body-copy">{selected.reinforcement} reinforcement in {selected.matrix} matrix.</p><DataGrid items={[['Fibre modulus',formatPa(selected.fibre_modulus_pa)],['Matrix modulus',formatPa(selected.matrix_modulus_pa)],['Density',selected.density_kg_m3 ? `${selected.density_kg_m3} kg/m³` : '—'],['Temperature range',`${selected.valid_temperature_range_k[0]}–${selected.valid_temperature_range_k[1]} K`],['Models',selected.supported_models.join(', ')],['Source',selected.source || 'Not recorded']]} /></> : <div className="empty-state">Select a material to inspect its properties and provenance.</div>}</section></div>}<footer className="app-footer"><span>REFERENCE DATA · SI UNITS</span><span>Rudrajyoti Paul</span></footer></div>
}

function MaterialBuilder() {
  const [materials, setMaterials] = useState<Material[]>([]); const [fibreVolume, setFibreVolume] = useState('0.6'); const [selected, setSelected] = useState(''); const [saved, setSaved] = useState(false); const [error, setError] = useState('')
  useEffect(() => { loadMaterials().then(setMaterials).catch((e) => setError(e.message)) }, [])
  const material = materials.find((m) => m.name === selected)
  const saveDraft = (e: FormEvent) => { e.preventDefault(); const value = Number(fibreVolume); if (!material || !Number.isFinite(value) || value <= 0 || value >= 1) { setError('Select a registered material and use a fibre volume fraction strictly between 0 and 1.'); return } setError(''); setSaved(true) }
  return <div className="page-frame"><PageIntro eyebrow="System builder" title="Compose a material system." description="Configure a registered composite system before sending it to the scientific engine. This draft is not persisted until a simulation is run." />{error && <ErrorState error={error} />}{!materials.length && !error ? <Loading /> : <div className="workspace-grid"><form className="panel form-panel" onSubmit={saveDraft}><div className="eyebrow">Configuration inputs</div><label>Registered material<select value={selected} onChange={(e) => { setSelected(e.target.value); setSaved(false) }}><option value="">Select a material</option>{materials.map((m) => <option key={m.name} value={m.name}>{m.name}</option>)}</select></label><label>Fibre volume fraction<input type="number" min="0.01" max="0.99" step="0.01" value={fibreVolume} onChange={(e) => setFibreVolume(e.target.value)} /><small>Dimensionless · valid range 0–1</small></label><button className="button button-primary" type="submit"><Beaker size={16} /> Validate configuration</button>{saved && <div className="success-state">Configuration validated. Run a simulation to persist a scientific result.</div>}</form><section className="panel"><div className="eyebrow">Configuration preview</div>{material ? <><h3>{material.name}</h3><DataGrid items={[['Fibre',material.reinforcement],['Matrix',material.matrix],['Supported models',material.supported_models.join(', ')],['Source',material.source || 'Not recorded'],['Status',material.status]]} /></> : <div className="empty-state">Choose a registered system to preview its compatible properties.</div>}</section></div>}<footer className="app-footer"><span>BUILDER · VALIDATED INPUTS ONLY</span><span>Rudrajyoti Paul</span></footer></div>
}

function ThermalSimulator({ laminate }: { laminate: boolean }) {
  const [materials, setMaterials] = useState<Material[]>([]); const [material, setMaterial] = useState(''); const [vf, setVf] = useState('0.6'); const [reference, setReference] = useState('293.15'); const [operating, setOperating] = useState('353.15'); const [angles, setAngles] = useState('0, 90, 90, 0'); const [thickness, setThickness] = useState('0.000125'); const [result, setResult] = useState<SimulationResult | null>(null); const [error, setError] = useState(''); const [busy, setBusy] = useState(false)
  useEffect(() => { loadMaterials().then((items) => { setMaterials(items); if (items[0]) setMaterial(items[0].name) }).catch((e) => setError(e.message)) }, [])
  const run = async (e: FormEvent) => { e.preventDefault(); setBusy(true); setError(''); setResult(null); try { const payload: any = { material_name: material, fibre_volume_fraction: Number(vf), reference_temperature_k: Number(reference), operating_temperature_k: Number(operating) }; if (laminate) payload.laminate = { angles_deg: angles.split(',').map(Number), ply_thickness_m: Number(thickness) }; setResult(await apiRequest<SimulationResult>('/simulations', { method: 'POST', body: JSON.stringify(payload) })) } catch (err) { setError(err instanceof Error ? err.message : 'Simulation request failed.') } finally { setBusy(false) } }
  return <div className="page-frame"><PageIntro eyebrow={laminate ? 'Laminate design' : 'Thermal response'} title={laminate ? 'Lay up the response.' : 'Model the temperature step.'} description={laminate ? 'Define a supported stacking sequence and inspect the returned Classical Laminate Theory result.' : 'Submit explicit temperatures and composition to the backend scientific engine.'} /><div className="workspace-grid"><form className="panel form-panel" onSubmit={run}><div className="eyebrow">Scientific request</div><label>Material system<select required value={material} onChange={(e) => setMaterial(e.target.value)}>{materials.map((m) => <option key={m.name}>{m.name}</option>)}</select></label><label>Fibre volume fraction<input required type="number" min="0" max="1" step="0.01" value={vf} onChange={(e) => setVf(e.target.value)} /></label><div className="field-row"><label>Reference temperature<input required type="number" step="0.01" value={reference} onChange={(e) => setReference(e.target.value)} /><small>K</small></label><label>Operating temperature<input required type="number" step="0.01" value={operating} onChange={(e) => setOperating(e.target.value)} /><small>K</small></label></div>{laminate && <><label>Stacking sequence<input required value={angles} onChange={(e) => setAngles(e.target.value)} /><small>Degrees, comma-separated</small></label><label>Ply thickness<input required type="number" min="0.0000001" step="0.000001" value={thickness} onChange={(e) => setThickness(e.target.value)} /><small>m</small></label></>}<button className="button button-primary" disabled={busy || !material}>{busy ? 'Running engine…' : 'Run calculation'} <ArrowRight size={16} /></button></form><section className="panel result-panel"><div className="eyebrow">Returned result</div>{error && <ErrorState error={error} />}{!result && !error && <div className="empty-state">Validated API results will appear here. No browser-side scientific result is generated.</div>}{result && <ResultView result={result} laminate={laminate} />}</section></div><footer className="app-footer"><span>{laminate ? 'CLT · A/B/D MATRICES' : 'THERMAL · SI UNITS'}</span><span>Rudrajyoti Paul</span></footer></div>
}

function ResultView({ result, laminate }: { result: SimulationResult; laminate: boolean }) { const props = result.effective_properties || {}; return <div><div className="result-id">Persisted record #{result.record_id}</div><DataGrid items={[['ΔT',`${result.delta_temperature_k} K`],['Thermal strain',String(result.thermal_strain_1)],['Restrained stress',result.restrained_stress_1_pa == null ? 'Not calculated' : `${(result.restrained_stress_1_pa / 1e6).toFixed(2)} MPa`],['E₁',formatPa(props.e1_pa)],['E₂',formatPa(props.e2_pa)],['Warnings',result.warnings?.length ? result.warnings.join(' ') : 'None']]} />{laminate && result.laminate && <><h4>Laminate calculation</h4><DataGrid items={[['A matrix','Returned 3×3 matrix'],['B matrix','Returned 3×3 matrix'],['D matrix','Returned 3×3 matrix'],['Ply stress recovery',`${result.laminate.ply_stresses?.length || 0} surfaces`]]} /></>}</div> }

function Comparison() { const [runs, setRuns] = useState<Simulation[]>([]); const [error, setError] = useState(''); useEffect(() => { loadSimulations().then(setRuns).catch((e) => setError(e.message)) }, []); return <div className="page-frame"><PageIntro eyebrow="Analysis" title="Compare simulations." description="Compare persisted results only. Runs with different inputs remain explicitly labelled rather than treated as equivalent." />{error ? <ErrorState error={error} /> : !runs.length ? <div className="panel empty-state">No saved simulations are available for comparison.</div> : <section className="panel"><RunTable runs={runs} detailed /></section>}<footer className="app-footer"><span>COMPARISON · PERSISTED RESULTS</span><span>Rudrajyoti Paul</span></footer></div> }
function Reports() { const [runs, setRuns] = useState<Simulation[]>([]); const [error, setError] = useState(''); useEffect(() => { loadSimulations().then(setRuns).catch((e) => setError(e.message)) }, []); return <div className="page-frame"><PageIntro eyebrow="Evidence" title="Results & reports." description="Inspect actual persisted inputs, outputs, warnings, and model provenance." />{error ? <ErrorState error={error} /> : <section className="panel"><RunTable runs={runs} detailed empty="No persisted reports yet. Run a simulation first." /></section>}<footer className="app-footer"><span>REPORTS · ENGINE OUTPUTS</span><span>Rudrajyoti Paul</span></footer></div> }
function RunTable({ runs, detailed = false, empty = 'No saved runs.' }: { runs: Simulation[]; detailed?: boolean; empty?: string }) { if (!runs.length) return <div className="empty-state">{empty}</div>; return <div className="run-table">{runs.map((run) => <div className="run-row" key={run.id}><span><strong>#{run.id} · {run.material_name}</strong><small>{formatDate(run.created_at)} · ΔT {run.result_payload.delta_temperature_k} K</small></span>{detailed && <span className="pill">{run.result_payload.warnings?.length || 0} warnings</span>}<span className="mono">{run.result_payload.laminate ? 'LAMINATE' : 'THERMAL'}</span></div>)}</div> }
function DataGrid({ items }: { items: [string, string][] }) { return <div className="data-grid">{items.map(([label, value]) => <div key={label}><span>{label}</span><strong>{value}</strong></div>)}</div> }
function Methodology() { return <div className="page-frame"><PageIntro eyebrow="Reference" title="Know what the model can tell you." description="The frontend presents the implemented preliminary models without overstating their scope." /><div className="info-grid"><section className="panel"><div className="eyebrow">Effective properties</div><h3>Rule-of-mixtures estimates</h3><p className="body-copy">The engine derives longitudinal and transverse modulus, shear modulus, and directional coefficients of thermal expansion from the registered material properties and fibre volume fraction.</p></section><section className="panel"><div className="eyebrow">Laminate model</div><h3>Classical Laminate Theory</h3><p className="body-copy">When a stacking sequence is supplied, the backend returns A, B, and D matrices, thermal resultants, curvature, and ply stress recovery in SI units.</p></section><section className="panel"><div className="eyebrow">Limitations</div><h3>Preliminary engineering estimate</h3><p className="body-copy">Results are linear-elastic estimates, not certification or safety evidence. Supplier properties and temperature histories require verification.</p></section></div><footer className="app-footer"><span>MODEL REFERENCE · SI UNITS</span><span>Rudrajyoti Paul</span></footer></div> }
function Settings() { const [health, setHealth] = useState('Not checked'); const probe = () => { setHealth('Checking…'); checkHealth().then(() => setHealth('Backend online')).catch(() => setHealth('Backend unavailable')) }; return <div className="page-frame"><PageIntro eyebrow="Workspace" title="Configure your lab." description="Connection diagnostics for this browser session. No setting is reported as saved unless the backend confirms it." /><section className="panel settings-panel"><label>API base URL<input readOnly value={API_BASE_URL} /></label><div className="connection-state"><span className="status-dot" />{health}</div><button className="button button-primary" onClick={probe} disabled={health === 'Checking…'}><Activity size={16} /> Check API health</button></section><footer className="app-footer"><span>SETTINGS · LOCAL SESSION</span><span>Rudrajyoti Paul</span></footer></div> }
function About() { return <div className="page-frame"><PageIntro eyebrow="ThermoComposite Lab" title="A calmer way to reason about composites." description="A React and FastAPI engineering workspace for traceable thermal and laminate exploration." /><div className="info-grid"><section className="panel"><div className="eyebrow">Technology</div><h3>React · TypeScript · FastAPI</h3><p className="body-copy">The frontend requests validated results from the backend, which reuses the preserved Python scientific engine and persistence layer.</p></section><section className="panel"><div className="eyebrow">Scope</div><h3>Transparent preliminary analysis</h3><p className="body-copy">Material provenance, units, boundary conditions, warnings, and model limitations remain visible alongside results.</p></section></div><footer className="app-footer"><span>THERMOCOMPOSITE LAB / v0.1</span><span>Rudrajyoti Paul</span></footer></div> }
function NotFound() { return <div className="page-frame"><PageIntro eyebrow="404" title="Workspace route not found." description="Use the navigation to return to a supported ThermoComposite Lab workflow." /><NavLink className="button button-primary" to="/">Return to dashboard</NavLink></div> }
function AuthScreen({ mode }: { mode: 'login' | 'register' }) { return <div className="auth-screen"><TextureBackground /><div className="auth-card"><NavLink to="/" className="brand"><span className="brand-mark">TC</span><span className="brand-text"><strong>Thermo</strong>Composite <small>LAB / 01</small></span></NavLink><div className="eyebrow">{mode === 'login' ? 'Welcome back' : 'Create workspace'}</div><h1>{mode === 'login' ? 'Enter the lab.' : 'Start a study.'}</h1><p>Authentication endpoints are not yet connected in this migration foundation.</p><label>Email address<input type="email" placeholder="you@organisation.com" /></label><label>Password<input type="password" placeholder="••••••••" /></label><button className="button button-primary" disabled>Authentication pending</button><div className="auth-switch"><NavLink to="/">Continue to local workspace</NavLink></div><div className="auth-foot">PRELIMINARY ENGINEERING WORKSPACE · RUDRAJYOTI PAUL</div></div></div> }
export default function App() { return <Routes><Route path="/login" element={<AuthScreen mode="login" />} /><Route path="/register" element={<AuthScreen mode="register" />} /><Route path="*" element={<AppShell />} /></Routes> }
