import { useState } from 'react';
import './index.css';
import { AuthProvider, useAuth } from './AuthContext';
import { LoginPage, RegisterPage } from './AuthPages';
import { Sidebar } from './Sidebar';
import { DashboardPage } from './DashboardPage';
import {
  CareerPredictionPage,
  PlacementPredictionPage,
  SalaryForecastPage,
  SuccessScorePage,
  ClusterPage,
} from './PredictionPages';
import {
  RecommendationsPage,
  ResumeAnalyzerPage,
  AnalyticsPage,
  ProfilePage,
} from './OtherPages';

type Page =
  | 'dashboard' | 'career' | 'placement' | 'salary'
  | 'success' | 'cluster' | 'recommendations'
  | 'resume' | 'profile' | 'analytics';

type AuthPage = 'login' | 'register';

function AppShell() {
  const { isAuthenticated, isLoading } = useAuth();
  const [authPage, setAuthPage] = useState<AuthPage>('login');
  const [page, setPage] = useState<Page>('dashboard');

  if (isLoading) {
    return (
      <div style={{
        minHeight: '100vh', display: 'flex', alignItems: 'center',
        justifyContent: 'center', background: 'var(--clr-bg)',
        flexDirection: 'column', gap: '1rem',
      }}>
        <div style={{
          width: 60, height: 60,
          borderRadius: 'var(--radius-lg)',
          background: 'var(--gradient-primary)',
          display: 'flex', alignItems: 'center', justifyContent: 'center',
          fontSize: '2rem', animation: 'pulse 1.5s infinite',
          boxShadow: 'var(--shadow-glow)',
        }}>🎓</div>
        <div style={{ color: 'var(--clr-text-muted)', fontSize: '0.875rem' }}>Loading…</div>
      </div>
    );
  }

  if (!isAuthenticated) {
    return authPage === 'login'
      ? <LoginPage onNavigate={p => setAuthPage(p as AuthPage)} />
      : <RegisterPage onNavigate={p => setAuthPage(p as AuthPage)} />;
  }

  const renderPage = () => {
    switch (page) {
      case 'dashboard':       return <DashboardPage />;
      case 'career':          return <CareerPredictionPage />;
      case 'placement':       return <PlacementPredictionPage />;
      case 'salary':          return <SalaryForecastPage />;
      case 'success':         return <SuccessScorePage />;
      case 'cluster':         return <ClusterPage />;
      case 'recommendations': return <RecommendationsPage />;
      case 'analytics':       return <AnalyticsPage />;
      case 'resume':          return <ResumeAnalyzerPage />;
      case 'profile':         return <ProfilePage />;
      default:                return <DashboardPage />;
    }
  };

  return (
    <div className="app-shell">
      {/* Background orbs */}
      <div className="orb orb-1" />
      <div className="orb orb-2" />

      <Sidebar current={page} onNavigate={p => setPage(p)} />
      <main className="main-content" style={{ position: 'relative', zIndex: 1 }}>
        {renderPage()}
      </main>
    </div>
  );
}

export default function App() {
  return (
    <AuthProvider>
      <AppShell />
    </AuthProvider>
  );
}
