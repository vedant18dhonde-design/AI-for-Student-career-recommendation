import React from 'react';
import { useAuth } from './AuthContext';

type Page =
  | 'dashboard'
  | 'career'
  | 'placement'
  | 'salary'
  | 'success'
  | 'cluster'
  | 'recommendations'
  | 'resume'
  | 'profile'
  | 'analytics';

interface Props { current: Page; onNavigate: (p: Page) => void; }

const NAV_ITEMS: { key: Page; icon: string; label: string; section?: string }[] = [
  { key: 'dashboard',       icon: '⊞',  label: 'Dashboard',       section: 'Overview' },
  { key: 'career',          icon: '🎯', label: 'Career Path',      section: 'Predictions' },
  { key: 'placement',       icon: '🏢', label: 'Placement',        },
  { key: 'salary',          icon: '💰', label: 'Salary Forecast',  },
  { key: 'success',         icon: '📈', label: 'Success Score',    },
  { key: 'cluster',         icon: '🧩', label: 'Peer Clustering',  },
  { key: 'recommendations', icon: '✨', label: 'Recommendations',  section: 'Insights' },
  { key: 'analytics',       icon: '📊', label: 'Analytics',        },
  { key: 'resume',          icon: '📄', label: 'Resume Analyzer',  section: 'Tools' },
  { key: 'profile',         icon: '👤', label: 'My Profile',       },
];

export function Sidebar({ current, onNavigate }: Props) {
  const { user, logout } = useAuth();
  let lastSection = '';

  return (
    <aside className="sidebar">
      <div className="sidebar-logo">
        <div className="sidebar-logo-icon">🎓</div>
        <div className="sidebar-logo-text">
          Student<span>Career</span><br />
          <span style={{ fontSize: '0.7rem', color: 'var(--clr-text-dim)', fontWeight: 400 }}>AI Analytics Platform</span>
        </div>
      </div>

      <nav className="sidebar-nav">
        {NAV_ITEMS.map(item => {
          const showSection = item.section && item.section !== lastSection;
          if (item.section) lastSection = item.section;
          return (
            <React.Fragment key={item.key}>
              {showSection && <div className="nav-section-label">{item.section}</div>}
              <button
                id={`nav-${item.key}`}
                className={`nav-item${current === item.key ? ' active' : ''}`}
                onClick={() => onNavigate(item.key)}
              >
                <span className="nav-item-icon">{item.icon}</span>
                {item.label}
              </button>
            </React.Fragment>
          );
        })}
      </nav>

      <div className="sidebar-footer">
        <div className="user-pill">
          <div className="avatar">
            {user?.full_name?.charAt(0).toUpperCase() ?? 'U'}
          </div>
          <div className="user-info">
            <div className="user-name">{user?.full_name ?? 'User'}</div>
            <div className="user-role">{user?.role ?? 'student'}</div>
          </div>
          <button
            id="btn-logout"
            className="btn btn-sm btn-secondary"
            title="Logout"
            onClick={logout}
            style={{ padding: '0.25rem 0.5rem', fontSize: '0.75rem' }}
          >
            ⏻
          </button>
        </div>
      </div>
    </aside>
  );
}
