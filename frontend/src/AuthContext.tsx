import { createContext, useContext, useState, useEffect, useCallback, type ReactNode } from 'react';
import { apiFetch, setTokens, clearTokens, getToken } from './api';

interface User {
  id: string;
  email: string;
  full_name: string;
  role: string;
  profile_picture?: string;
}

interface AuthState {
  user: User | null;
  isLoading: boolean;
  isAuthenticated: boolean;
  login: (email: string, password: string) => Promise<void>;
  register: (data: RegisterData) => Promise<void>;
  logout: () => void;
}

interface RegisterData {
  email: string;
  password: string;
  full_name: string;
}

const AuthContext = createContext<AuthState | null>(null);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  const fetchMe = useCallback(async () => {
    try {
      if (!getToken()) { setIsLoading(false); return; }
      const data = await apiFetch<{ data: User }>('/users/me');
      setUser(data.data);
    } catch {
      clearTokens();
      setUser(null);
    } finally {
      setIsLoading(false);
    }
  }, []);

  useEffect(() => { fetchMe(); }, [fetchMe]);

  const login = async (email: string, password: string) => {
    const data = await apiFetch<{ data: { access_token: string; refresh_token: string; user: User } }>(
      '/auth/login',
      { method: 'POST', body: JSON.stringify({ email, password }) }
    );
    setTokens(data.data.access_token, data.data.refresh_token);
    setUser(data.data.user);
  };

  const register = async (payload: RegisterData) => {
    const data = await apiFetch<{ data: { access_token: string; refresh_token: string; user: User } }>(
      '/auth/register',
      { method: 'POST', body: JSON.stringify({ name: payload.full_name, email: payload.email, password: payload.password }) }
    );
    setTokens(data.data.access_token, data.data.refresh_token);
    setUser(data.data.user);
  };

  const logout = () => {
    clearTokens();
    setUser(null);
  };

  return (
    <AuthContext.Provider value={{ user, isLoading, isAuthenticated: !!user, login, register, logout }}>
      {children}
    </AuthContext.Provider>
  );
}

export const useAuth = () => {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error('useAuth must be used within AuthProvider');
  return ctx;
};
