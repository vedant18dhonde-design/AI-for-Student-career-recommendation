
import { useAuth } from './AuthContext';

interface Props { title: string; subtitle?: string; }

export function Topbar({ title, subtitle }: Props) {
  const { user } = useAuth();
  const hour = new Date().getHours();
  const greeting = hour < 12 ? '🌅 Good morning' : hour < 17 ? '☀️ Good afternoon' : '🌙 Good evening';

  return (
    <header className="topbar">
      <div>
        <div className="topbar-title">{title}</div>
        {subtitle && <div className="text-sm text-muted">{subtitle}</div>}
      </div>
      <div className="topbar-actions">
        <div style={{ fontSize: '0.875rem', color: 'var(--clr-text-muted)' }}>
          {greeting}, <strong style={{ color: 'var(--clr-text)' }}>{user?.full_name?.split(' ')[0]}</strong>
        </div>
        <div className="avatar" style={{ width: 32, height: 32, fontSize: '0.8rem' }}>
          {user?.full_name?.charAt(0).toUpperCase() ?? 'U'}
        </div>
      </div>
    </header>
  );
}
