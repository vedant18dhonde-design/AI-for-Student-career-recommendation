import { useState } from 'react';
import { useAuth } from './AuthContext';

interface Props { onNavigate: (page: string) => void; }

export function LoginPage({ onNavigate }: Props) {
  const { login } = useAuth();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(''); setLoading(true);
    try {
      await login(email, password);
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : 'Login failed');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="auth-page">
      <div className="auth-card animate-fade-in">
        <div className="auth-logo">
          <div className="auth-logo-icon">🎓</div>
          <div>
            <div className="auth-title gradient-text">Welcome back</div>
            <div className="auth-subtitle">Sign in to your career dashboard</div>
          </div>
        </div>

        <form className="auth-form" onSubmit={handleSubmit}>
          {error && (
            <div style={{
              padding: '0.75rem 1rem',
              background: 'rgba(239,68,68,0.1)',
              border: '1px solid rgba(239,68,68,0.3)',
              borderRadius: 'var(--radius-md)',
              color: 'var(--clr-danger)',
              fontSize: '0.875rem'
            }}>
              ⚠️ {error}
            </div>
          )}
          <div className="form-group">
            <label className="form-label">Email address</label>
            <input
              id="login-email"
              type="email" required
              className="form-input"
              placeholder="you@example.com"
              value={email}
              onChange={e => setEmail(e.target.value)}
            />
          </div>
          <div className="form-group">
            <label className="form-label">Password</label>
            <input
              id="login-password"
              type="password" required
              className="form-input"
              placeholder="••••••••"
              value={password}
              onChange={e => setPassword(e.target.value)}
            />
          </div>
          <button id="btn-login" type="submit" className="btn btn-primary btn-lg w-full" disabled={loading}>
            {loading ? <span className="animate-spin">⟳</span> : null}
            {loading ? 'Signing in…' : 'Sign In'}
          </button>
        </form>

        <div className="auth-footer">
          Don't have an account?{' '}
          <button
            className="btn btn-outline btn-sm"
            style={{ marginLeft: '0.5rem' }}
            onClick={() => onNavigate('register')}
          >
            Register
          </button>
        </div>
      </div>
    </div>
  );
}

export function RegisterPage({ onNavigate }: Props) {
  const { register } = useAuth();
  const [form, setForm] = useState({ full_name: '', email: '', password: '', confirm: '' });
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (form.password !== form.confirm) { setError('Passwords do not match'); return; }
    setError(''); setLoading(true);
    try {
      await register({ email: form.email, password: form.password, full_name: form.full_name });
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : 'Registration failed');
    } finally {
      setLoading(false);
    }
  };

  const set = (k: string) => (e: React.ChangeEvent<HTMLInputElement>) => setForm(f => ({ ...f, [k]: e.target.value }));

  return (
    <div className="auth-page">
      <div className="auth-card animate-fade-in">
        <div className="auth-logo">
          <div className="auth-logo-icon">🚀</div>
          <div>
            <div className="auth-title gradient-text">Create account</div>
            <div className="auth-subtitle">Start your career journey today</div>
          </div>
        </div>

        <form className="auth-form" onSubmit={handleSubmit}>
          {error && (
            <div style={{
              padding: '0.75rem 1rem',
              background: 'rgba(239,68,68,0.1)',
              border: '1px solid rgba(239,68,68,0.3)',
              borderRadius: 'var(--radius-md)',
              color: 'var(--clr-danger)',
              fontSize: '0.875rem'
            }}>
              ⚠️ {error}
            </div>
          )}
          <div className="form-group">
            <label className="form-label">Full name</label>
            <input id="reg-name" type="text" required className="form-input" placeholder="John Doe" value={form.full_name} onChange={set('full_name')} />
          </div>
          <div className="form-group">
            <label className="form-label">Email address</label>
            <input id="reg-email" type="email" required className="form-input" placeholder="you@example.com" value={form.email} onChange={set('email')} />
          </div>
          <div className="grid-2">
            <div className="form-group">
              <label className="form-label">Password</label>
              <input id="reg-password" type="password" required minLength={8} className="form-input" placeholder="Min 8 chars" value={form.password} onChange={set('password')} />
            </div>
            <div className="form-group">
              <label className="form-label">Confirm</label>
              <input id="reg-confirm" type="password" required className="form-input" placeholder="Repeat" value={form.confirm} onChange={set('confirm')} />
            </div>
          </div>
          <button id="btn-register" type="submit" className="btn btn-primary btn-lg w-full" disabled={loading}>
            {loading ? <span className="animate-spin">⟳</span> : null}
            {loading ? 'Creating account…' : 'Create Account'}
          </button>
        </form>

        <div className="auth-footer">
          Already have an account?{' '}
          <button className="btn btn-outline btn-sm" style={{ marginLeft: '0.5rem' }} onClick={() => onNavigate('login')}>
            Sign in
          </button>
        </div>
      </div>
    </div>
  );
}
