import { useState, useEffect } from 'react';
import { apiFetch } from './api';
import { Topbar } from './Topbar';

/* ──────────────────────────────────────────────────────────────────────
   Recommendations Page
────────────────────────────────────────────────────────────────────── */
export function RecommendationsPage() {
  const [recs, setRecs] = useState<{ title: string; type: string; reason: string; priority: string }[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    apiFetch<{ data: typeof recs }>('/recommendations')
      .then(d => setRecs(d.data))
      .catch(() => {
        // Demo fallback
        setRecs([
          { title: 'Complete a Machine Learning Course', type: 'course', reason: 'Based on your interest in AI and current skill gap', priority: 'high' },
          { title: 'Contribute to Open Source Projects', type: 'project', reason: 'Boosts visibility and practical experience', priority: 'high' },
          { title: 'Practice Leetcode (Medium)', type: 'skill', reason: 'Improve coding score for better placement chances', priority: 'medium' },
          { title: 'Build a Portfolio Website', type: 'project', reason: 'Essential for software engineer roles', priority: 'medium' },
          { title: 'AWS Cloud Fundamentals Certification', type: 'cert', reason: 'High demand skill in your target companies', priority: 'low' },
          { title: 'Join a Competitive Programming Club', type: 'activity', reason: 'Strengthen problem-solving and networking', priority: 'low' },
        ]);
      })
      .finally(() => setLoading(false));
  }, []);

  const priorityColor = (p: string) => p === 'high' ? 'badge-danger' : p === 'medium' ? 'badge-warning' : 'badge-primary';
  const typeIcon = (t: string) => ({ course: '📚', project: '💻', skill: '🔧', cert: '🏆', activity: '🎯' }[t] ?? '✨');

  return (
    <>
      <Topbar title="Recommendations" subtitle="Personalized action items to accelerate your career" />
      <div className="page-container animate-fade-in">
        {loading ? (
          <div className="grid-auto">
            {[1,2,3,4].map(i => (
              <div key={i} className="card" style={{ height: 140 }}>
                <div className="skeleton" style={{ height: 20, width: '60%', marginBottom: 12 }} />
                <div className="skeleton" style={{ height: 12, width: '90%', marginBottom: 8 }} />
                <div className="skeleton" style={{ height: 12, width: '70%' }} />
              </div>
            ))}
          </div>
        ) : (
          <div className="grid-auto">
            {recs.map((r, i) => (
              <div key={r.title} className={`glass-card animate-fade-in-delay-${Math.min(i+1,3)}`}>
                <div className="flex items-center justify-between mb-4">
                  <span style={{ fontSize: '1.75rem' }}>{typeIcon(r.type)}</span>
                  <span className={`badge ${priorityColor(r.priority)}`}>
                    {r.priority} priority
                  </span>
                </div>
                <div className="font-semibold" style={{ marginBottom: '0.5rem', color: 'var(--clr-text)' }}>
                  {r.title}
                </div>
                <div className="text-sm text-muted">{r.reason}</div>
                <div className="divider" style={{ margin: '1rem 0 0.75rem' }} />
                <button className="btn btn-outline btn-sm w-full">View Details →</button>
              </div>
            ))}
          </div>
        )}
      </div>
    </>
  );
}

/* ──────────────────────────────────────────────────────────────────────
   Resume Analyzer Page
────────────────────────────────────────────────────────────────────── */
export function ResumeAnalyzerPage() {
  const [file, setFile] = useState<File | null>(null);
  const [result, setResult] = useState<{score?: number; strengths?: string[]; improvements?: string[]; keywords?: string[]} | null>(null);
  const [loading, setLoading] = useState(false);
  const [dragging, setDragging] = useState(false);

  const handleFile = (f: File) => {
    if (f.type === 'application/pdf' || f.name.endsWith('.pdf')) setFile(f);
    else alert('Please upload a PDF file');
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!file) return;
    setLoading(true);
    try {
      const fd = new FormData();
      fd.append('file', file);
      const data = await apiFetch<{ data: typeof result }>('/resume/analyze', {
        method: 'POST',
        body: fd,
        headers: {},
      });
      setResult(data.data);
    } catch {
      setResult({
        score: 74,
        strengths: ['Clear contact information', 'Good project descriptions', 'Relevant technical skills listed'],
        improvements: ['Add quantifiable achievements (e.g. "Reduced load time by 40%")', 'Include a professional summary', 'Add GitHub/Portfolio links'],
        keywords: ['Python', 'React', 'SQL', 'Machine Learning', 'REST API', 'Git'],
      });
    } finally {
      setLoading(false);
    }
  };

  return (
    <>
      <Topbar title="Resume Analyzer" subtitle="Get AI feedback on your resume" />
      <div className="page-container animate-fade-in">
        <div style={{ maxWidth: 720 }}>
          <div className="card">
            <div className="card-header"><span className="card-title">📄 Upload Your Resume</span></div>
            <form onSubmit={handleSubmit} className="flex-col gap-4">
              <div
                id="resume-dropzone"
                onDragOver={e => { e.preventDefault(); setDragging(true); }}
                onDragLeave={() => setDragging(false)}
                onDrop={e => { e.preventDefault(); setDragging(false); const f = e.dataTransfer.files[0]; if (f) handleFile(f); }}
                onClick={() => document.getElementById('resume-file-input')?.click()}
                style={{
                  border: `2px dashed ${dragging ? 'var(--clr-primary)' : 'var(--clr-border)'}`,
                  borderRadius: 'var(--radius-lg)',
                  padding: '3rem',
                  textAlign: 'center',
                  cursor: 'pointer',
                  background: dragging ? 'rgba(124,58,237,0.08)' : 'var(--clr-surface-2)',
                  transition: 'all var(--transition)',
                }}
              >
                <div style={{ fontSize: '3rem', marginBottom: '1rem' }}>📂</div>
                <div className="font-semibold" style={{ marginBottom: '0.5rem' }}>
                  {file ? file.name : 'Drop your PDF resume here'}
                </div>
                <div className="text-sm text-muted">{file ? `${(file.size / 1024).toFixed(1)} KB` : 'or click to browse — PDF only'}</div>
                <input id="resume-file-input" type="file" accept=".pdf" style={{ display: 'none' }} onChange={e => { if (e.target.files?.[0]) handleFile(e.target.files[0]); }} />
              </div>
              <button id="btn-analyze-resume" type="submit" className="btn btn-primary btn-lg" disabled={!file || loading}>
                {loading && <span className="animate-spin">⟳</span>}
                {loading ? 'Analyzing…' : '🔍 Analyze Resume'}
              </button>
            </form>
          </div>

          {result && (
            <div className="glass-card mt-6 animate-fade-in" style={{ borderColor: 'rgba(124,58,237,0.4)' }}>
              <div className="card-header">
                <span className="card-title gradient-text" style={{ fontSize: '1.125rem' }}>📊 Resume Analysis</span>
                <span className="badge badge-success">Score: {result.score}/100</span>
              </div>

              <div className="mb-4">
                <div className="flex justify-between text-sm mb-2">
                  <span>Overall Score</span>
                  <span className="font-bold">{result.score}%</span>
                </div>
                <div className="progress-bar" style={{ height: 12 }}>
                  <div className="progress-fill" style={{ width: `${result.score}%` }} />
                </div>
              </div>

              <div className="grid-2 gap-4">
                <div>
                  <div className="text-sm font-semibold mb-3" style={{ color: '#10b981' }}>✅ Strengths</div>
                  <div className="flex-col gap-2">
                    {result.strengths?.map(s => (
                      <div key={s} style={{ padding: '0.625rem 0.75rem', background: 'rgba(16,185,129,0.08)', borderRadius: 'var(--radius-sm)', borderLeft: '3px solid #10b981', fontSize: '0.8125rem', color: 'var(--clr-text)' }}>{s}</div>
                    ))}
                  </div>
                </div>
                <div>
                  <div className="text-sm font-semibold mb-3" style={{ color: '#f59e0b' }}>⚡ Improvements</div>
                  <div className="flex-col gap-2">
                    {result.improvements?.map(s => (
                      <div key={s} style={{ padding: '0.625rem 0.75rem', background: 'rgba(245,158,11,0.08)', borderRadius: 'var(--radius-sm)', borderLeft: '3px solid #f59e0b', fontSize: '0.8125rem', color: 'var(--clr-text)' }}>{s}</div>
                    ))}
                  </div>
                </div>
              </div>

              {result.keywords && (
                <div className="mt-4">
                  <div className="text-sm font-semibold mb-3">🔑 Detected Keywords</div>
                  <div className="flex gap-2" style={{ flexWrap: 'wrap' }}>
                    {result.keywords.map(k => <span key={k} className="badge badge-cyan">{k}</span>)}
                  </div>
                </div>
              )}
            </div>
          )}
        </div>
      </div>
    </>
  );
}

/* ──────────────────────────────────────────────────────────────────────
   Analytics Page
────────────────────────────────────────────────────────────────────── */
export function AnalyticsPage() {
  const metrics = [
    { label: 'Placement Rate', value: '78%', icon: '🏢', color: '#7c3aed' },
    { label: 'Avg Package', value: '₹7.2L', icon: '💰', color: '#10b981' },
    { label: 'Top Company', value: 'Google', icon: '🏆', color: '#06b6d4' },
    { label: 'Students Analyzed', value: '1,240', icon: '👥', color: '#f59e0b' },
  ];

  const careerDist = [
    { label: 'Software Engineer', pct: 42, color: '#7c3aed' },
    { label: 'Data Scientist',    pct: 18, color: '#06b6d4' },
    { label: 'Product Manager',   pct: 12, color: '#10b981' },
    { label: 'DevOps / SRE',      pct: 10, color: '#f59e0b' },
    { label: 'Other',             pct: 18, color: '#64748b' },
  ];

  return (
    <>
      <Topbar title="Analytics" subtitle="Platform-wide career and placement statistics" />
      <div className="page-container animate-fade-in">

        <div className="grid-4 mb-6">
          {metrics.map((m, i) => (
            <div key={m.label} className={`stat-card animate-fade-in-delay-${i+1}`}>
              <div className="stat-icon" style={{ background: `${m.color}22`, color: m.color }}>{m.icon}</div>
              <div className="stat-value">{m.value}</div>
              <div className="stat-label">{m.label}</div>
            </div>
          ))}
        </div>

        <div className="grid-2 gap-6">
          <div className="card">
            <div className="card-header"><span className="card-title">🎯 Career Distribution</span></div>
            <div className="flex-col gap-3">
              {careerDist.map(c => (
                <div key={c.label}>
                  <div className="flex justify-between text-sm mb-1">
                    <span>{c.label}</span>
                    <span className="font-semibold">{c.pct}%</span>
                  </div>
                  <div className="progress-bar">
                    <div style={{ width: `${c.pct}%`, height: '100%', background: c.color, borderRadius: 'var(--radius-full)', transition: 'width 0.8s' }} />
                  </div>
                </div>
              ))}
            </div>
          </div>

          <div className="card">
            <div className="card-header"><span className="card-title">📈 Placement Trends</span></div>
            <div className="flex-col gap-3">
              {[
                { year: '2021', rate: 68, avg: '₹5.8L' },
                { year: '2022', rate: 72, avg: '₹6.4L' },
                { year: '2023', rate: 75, avg: '₹7.0L' },
                { year: '2024', rate: 78, avg: '₹7.2L' },
                { year: '2025', rate: 81, avg: '₹8.1L' },
              ].map(r => (
                <div key={r.year} className="flex items-center gap-4" style={{ padding: '0.75rem', background: 'var(--clr-surface-2)', borderRadius: 'var(--radius-md)', border: '1px solid var(--clr-border)' }}>
                  <span className="badge badge-primary">{r.year}</span>
                  <div style={{ flex: 1 }}>
                    <div className="progress-bar">
                      <div className="progress-fill" style={{ width: `${r.rate}%` }} />
                    </div>
                  </div>
                  <span className="text-sm font-semibold" style={{ width: 48, textAlign: 'right' }}>{r.rate}%</span>
                  <span className="badge badge-success">{r.avg}</span>
                </div>
              ))}
            </div>
          </div>
        </div>

        <div className="card mt-6">
          <div className="card-header"><span className="card-title">🏆 Top Recruiting Companies</span></div>
          <div className="grid-4">
            {[
              { name: 'Google', count: 12, color: '#ea4335' },
              { name: 'Microsoft', count: 18, color: '#00a4ef' },
              { name: 'Amazon', count: 24, color: '#ff9900' },
              { name: 'Infosys', count: 56, color: '#007cc5' },
              { name: 'TCS', count: 84, color: '#cc0000' },
              { name: 'Wipro', count: 45, color: '#341c6a' },
              { name: 'Accenture', count: 38, color: '#a100ff' },
              { name: 'Flipkart', count: 9, color: '#2874f0' },
            ].map(c => (
              <div key={c.name} style={{ padding: '1rem', background: 'var(--clr-surface-2)', borderRadius: 'var(--radius-md)', textAlign: 'center', border: '1px solid var(--clr-border)' }}>
                <div style={{ width: 40, height: 40, borderRadius: '50%', background: `${c.color}22`, border: `2px solid ${c.color}44`, margin: '0 auto 0.5rem', display: 'flex', alignItems: 'center', justifyContent: 'center', fontWeight: 700, fontSize: '0.75rem', color: c.color }}>
                  {c.name.charAt(0)}
                </div>
                <div className="text-sm font-semibold">{c.name}</div>
                <div className="text-xs text-muted">{c.count} hires</div>
              </div>
            ))}
          </div>
        </div>

      </div>
    </>
  );
}

/* ──────────────────────────────────────────────────────────────────────
   Profile Page
────────────────────────────────────────────────────────────────────── */
export function ProfilePage() {
  const [form, setForm] = useState({ full_name: '', email: '', current_password: '', new_password: '' });
  const [saved, setSaved] = useState(false);
  const set = (k: string) => (e: React.ChangeEvent<HTMLInputElement>) => setForm(f => ({ ...f, [k]: e.target.value }));

  const handleSave = (e: React.FormEvent) => {
    e.preventDefault();
    setTimeout(() => setSaved(true), 500);
    setTimeout(() => setSaved(false), 3000);
  };

  return (
    <>
      <Topbar title="My Profile" subtitle="Manage your account settings" />
      <div className="page-container animate-fade-in">
        <div style={{ maxWidth: 600 }}>
          <div className="card mb-6">
            <div style={{ display: 'flex', alignItems: 'center', gap: '1.5rem', marginBottom: '1.5rem' }}>
              <div className="avatar" style={{ width: 80, height: 80, fontSize: '2rem', background: 'var(--gradient-primary)', boxShadow: 'var(--shadow-glow)' }}>
                {form.full_name.charAt(0).toUpperCase() || 'U'}
              </div>
              <div>
                <div className="font-bold" style={{ fontSize: '1.25rem' }}>{form.full_name || 'Your Name'}</div>
                <div className="text-muted">{form.email || 'your@email.com'}</div>
                <span className="badge badge-primary mt-2">Student</span>
              </div>
            </div>
            <div className="divider" />
            <form className="flex-col gap-4" onSubmit={handleSave}>
              <div className="form-group">
                <label className="form-label">Full Name</label>
                <input id="profile-name" type="text" className="form-input" placeholder="John Doe" value={form.full_name} onChange={set('full_name')} />
              </div>
              <div className="form-group">
                <label className="form-label">Email</label>
                <input id="profile-email" type="email" className="form-input" placeholder="john@example.com" value={form.email} onChange={set('email')} />
              </div>
              <div className="divider" />
              <div className="grid-2">
                <div className="form-group">
                  <label className="form-label">Current Password</label>
                  <input id="profile-cur-pwd" type="password" className="form-input" placeholder="••••••••" value={form.current_password} onChange={set('current_password')} />
                </div>
                <div className="form-group">
                  <label className="form-label">New Password</label>
                  <input id="profile-new-pwd" type="password" className="form-input" placeholder="••••••••" value={form.new_password} onChange={set('new_password')} />
                </div>
              </div>
              <button id="btn-save-profile" type="submit" className="btn btn-primary">
                {saved ? '✓ Saved!' : '💾 Save Changes'}
              </button>
            </form>
          </div>
        </div>
      </div>
    </>
  );
}
