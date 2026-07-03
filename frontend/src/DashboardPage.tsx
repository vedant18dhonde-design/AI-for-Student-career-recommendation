
import { useAuth } from './AuthContext';
import { Topbar } from './Topbar';

export function DashboardPage() {
  const { user } = useAuth();

  const stats = [
    { icon: '🎯', label: 'Career Predictions', value: '3', delta: '+1 this week', up: true,  bg: 'rgba(124,58,237,0.15)', color: '#a855f7' },
    { icon: '💰', label: 'Avg Salary Forecast', value: '₹8.4L', delta: '+12% industry', up: true, bg: 'rgba(16,185,129,0.15)', color: '#10b981' },
    { icon: '🏢', label: 'Placement Score', value: '78%', delta: 'Top 30%', up: true,  bg: 'rgba(6,182,212,0.15)', color: '#06b6d4' },
    { icon: '📈', label: 'Success Index', value: '82', delta: 'Excellent', up: true,  bg: 'rgba(245,158,11,0.15)', color: '#f59e0b' },
  ];

  const recentPredictions = [
    { type: 'Career Path',    result: 'Software Engineer',     date: '2 days ago',  badge: 'primary' },
    { type: 'Placement',      result: '78% placement chance',  date: '3 days ago',  badge: 'success' },
    { type: 'Salary Forecast',result: '₹8.4 LPA',             date: '5 days ago',  badge: 'warning' },
    { type: 'Success Score',  result: '82 / 100',              date: '1 week ago',  badge: 'cyan'    },
  ];

  const skills = [
    { name: 'Programming',   pct: 82 },
    { name: 'Mathematics',   pct: 74 },
    { name: 'Communication', pct: 68 },
    { name: 'Databases',     pct: 79 },
    { name: 'ML / AI',       pct: 55 },
  ];

  return (
    <>
      <Topbar
        title="Dashboard"
        subtitle="Your career intelligence at a glance"
      />
      <div className="page-container animate-fade-in">

        {/* Hero greeting */}
        <div className="glass-card mb-6" style={{
          background: 'linear-gradient(135deg, rgba(124,58,237,0.2) 0%, rgba(6,182,212,0.1) 100%)',
          borderColor: 'rgba(124,58,237,0.3)',
        }}>
          <div className="flex items-center gap-4">
            <div style={{
              width: 64, height: 64,
              borderRadius: 'var(--radius-lg)',
              background: 'var(--gradient-primary)',
              display: 'flex', alignItems: 'center', justifyContent: 'center',
              fontSize: '2rem', flexShrink: 0,
              boxShadow: 'var(--shadow-glow)',
            }}>
              🎓
            </div>
            <div>
              <h2 style={{ color: 'var(--clr-text)', marginBottom: '0.25rem' }}>
                Welcome back, <span className="gradient-text">{user?.full_name?.split(' ')[0] ?? 'Student'}</span>!
              </h2>
              <p>Your AI-powered career analysis platform is ready. Run predictions to get personalized insights.</p>
            </div>
          </div>
        </div>

        {/* Stats row */}
        <div className="grid-4 mb-6">
          {stats.map((s, i) => (
            <div
              key={s.label}
              className={`stat-card animate-fade-in-delay-${i + 1}`}
            >
              <div className="stat-icon" style={{ background: s.bg, color: s.color }}>
                {s.icon}
              </div>
              <div className="stat-value">{s.value}</div>
              <div className="stat-label">{s.label}</div>
              <div className={`stat-delta ${s.up ? 'up' : 'down'}`}>
                {s.up ? '↑' : '↓'} {s.delta}
              </div>
            </div>
          ))}
        </div>

        {/* Main content grid */}
        <div className="grid-2 gap-6">

          {/* Recent predictions */}
          <div className="card">
            <div className="card-header">
              <span className="card-title">🕐 Recent Predictions</span>
              <span className="badge badge-primary">Last 7 days</span>
            </div>
            <div className="flex-col gap-3">
              {recentPredictions.map((p) => (
                <div key={p.type} className="flex items-center justify-between" style={{
                  padding: '0.75rem',
                  background: 'var(--clr-surface-2)',
                  borderRadius: 'var(--radius-md)',
                  border: '1px solid var(--clr-border)',
                }}>
                  <div>
                    <div className="text-sm font-semibold">{p.type}</div>
                    <div className="text-xs text-muted">{p.date}</div>
                  </div>
                  <span className={`badge badge-${p.badge}`}>{p.result}</span>
                </div>
              ))}
            </div>
          </div>

          {/* Skill snapshot */}
          <div className="card">
            <div className="card-header">
              <span className="card-title">💡 Skill Snapshot</span>
              <span className="badge badge-cyan">Based on inputs</span>
            </div>
            <div className="flex-col gap-4">
              {skills.map(sk => (
                <div key={sk.name} className="skill-item">
                  <div className="skill-header">
                    <span className="skill-name">{sk.name}</span>
                    <span className="skill-pct">{sk.pct}%</span>
                  </div>
                  <div className="progress-bar">
                    <div className="progress-fill" style={{ width: `${sk.pct}%` }} />
                  </div>
                </div>
              ))}
            </div>
          </div>

        </div>

        {/* Quick actions */}
        <div className="card mt-6">
          <div className="card-header">
            <span className="card-title">⚡ Quick Actions</span>
          </div>
          <div className="grid-4">
            {[
              { icon: '🎯', label: 'Career Prediction', page: 'career',  color: '#7c3aed' },
              { icon: '🏢', label: 'Placement Check',   page: 'placement',color: '#06b6d4' },
              { icon: '💰', label: 'Salary Estimate',   page: 'salary',   color: '#10b981' },
              { icon: '📄', label: 'Resume Analyze',    page: 'resume',   color: '#f59e0b' },
            ].map(qa => (
              <div
                key={qa.page}
                className="glass-card text-center"
                style={{ cursor: 'pointer', padding: '1.25rem' }}
              >
                <div style={{ fontSize: '2rem', marginBottom: '0.5rem' }}>{qa.icon}</div>
                <div className="text-sm font-semibold">{qa.label}</div>
                <div style={{
                  width: '100%', height: '3px', marginTop: '0.75rem',
                  background: `linear-gradient(90deg, ${qa.color}, transparent)`,
                  borderRadius: 'var(--radius-full)',
                }} />
              </div>
            ))}
          </div>
        </div>

      </div>
    </>
  );
}
