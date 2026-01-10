/**
 * Authentication Context Provider
 *
 * This module provides a React context for managing global authentication state
 * across the frontend application. It handles JWT token storage, user state,
 * and authentication actions (sign-in, sign-out).
 *
 * Spec: 002-authentication-jwt
 * Created: 2026-01-09
 */

'use client';

import React, { createContext, useContext, useState, useEffect, useCallback } from 'react';
import { getStoredToken, saveToken, clearStoredToken } from './jwt-storage';

/**
 * User information extracted from JWT token
 */
interface User {
  userId: string;
  email: string;
}

/**
 * Authentication context value
 */
interface AuthContextValue {
  user: User | null;
  token: string | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  signIn: (token: string) => void;
  signOut: () => void;
  refreshAuth: () => void;
}

/**
 * Authentication context (use via useAuth hook)
 */
const AuthContext = createContext<AuthContextValue | undefined>(undefined);

/**
 * Decode JWT token payload (without verification)
 *
 * This is a client-side helper to extract user info from the token.
 * The backend performs full JWT validation.
 *
 * @param token - JWT token string
 * @returns Decoded payload or null if invalid
 */
function decodeJwtPayload(token: string): any | null {
  try {
    // JWT format: header.payload.signature
    const parts = token.split('.');

    if (parts.length !== 3) {
      return null;
    }

    // Decode base64url payload
    const payload = parts[1];
    const base64 = payload.replace(/-/g, '+').replace(/_/g, '/');
    const jsonPayload = decodeURIComponent(
      atob(base64)
        .split('')
        .map((c) => '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2))
        .join('')
    );

    return JSON.parse(jsonPayload);
  } catch (error) {
    console.error('Failed to decode JWT payload:', error);
    return null;
  }
}

/**
 * Extract user information from JWT token
 *
 * @param token - JWT token string
 * @returns User object or null if token is invalid
 */
function extractUserFromToken(token: string): User | null {
  const payload = decodeJwtPayload(token);

  if (!payload || !payload.sub || !payload.email) {
    return null;
  }

  return {
    userId: payload.sub,
    email: payload.email,
  };
}

/**
 * Authentication Context Provider Props
 */
interface AuthProviderProps {
  children: React.ReactNode;
}

/**
 * Authentication Context Provider Component
 *
 * Wrap your app with this provider to enable authentication context.
 *
 * @example
 * ```tsx
 * <AuthProvider>
 *   <App />
 * </AuthProvider>
 * ```
 */
export function AuthProvider({ children }: AuthProviderProps) {
  const [user, setUser] = useState<User | null>(null);
  const [token, setToken] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  /**
   * Initialize auth state from stored token on mount
   */
  useEffect(() => {
    const storedToken = getStoredToken();

    if (storedToken) {
      const extractedUser = extractUserFromToken(storedToken);

      if (extractedUser) {
        setToken(storedToken);
        setUser(extractedUser);
      } else {
        // Invalid token - clear storage
        clearStoredToken();
      }
    }

    setIsLoading(false);
  }, []);

  /**
   * Sign in with JWT token
   *
   * @param newToken - JWT token received from Better Auth
   */
  const signIn = useCallback((newToken: string) => {
    const extractedUser = extractUserFromToken(newToken);

    if (!extractedUser) {
      console.error('Invalid JWT token received');
      return;
    }

    // Save token to storage
    saveToken(newToken);

    // Update state
    setToken(newToken);
    setUser(extractedUser);
  }, []);

  /**
   * Sign out (clear token and redirect to sign-in page)
   */
  const signOut = useCallback(() => {
    // Clear storage
    clearStoredToken();

    // Clear state
    setToken(null);
    setUser(null);

    // Redirect to sign-in page
    if (typeof window !== 'undefined') {
      window.location.href = '/auth/signin';
    }
  }, []);

  /**
   * Refresh authentication state from storage
   *
   * This is useful after token updates or when syncing state across tabs.
   */
  const refreshAuth = useCallback(() => {
    const storedToken = getStoredToken();

    if (storedToken) {
      const extractedUser = extractUserFromToken(storedToken);

      if (extractedUser) {
        setToken(storedToken);
        setUser(extractedUser);
      } else {
        // Invalid token - clear everything
        clearStoredToken();
        setToken(null);
        setUser(null);
      }
    } else {
      // No token - clear state
      setToken(null);
      setUser(null);
    }
  }, []);

  const value: AuthContextValue = {
    user,
    token,
    isAuthenticated: !!user && !!token,
    isLoading,
    signIn,
    signOut,
    refreshAuth,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

/**
 * Hook to access authentication context
 *
 * @returns Authentication context value
 * @throws Error if used outside AuthProvider
 *
 * @example
 * ```tsx
 * function MyComponent() {
 *   const { user, isAuthenticated, signOut } = useAuth();
 *
 *   if (!isAuthenticated) {
 *     return <div>Please sign in</div>;
 *   }
 *
 *   return (
 *     <div>
 *       <p>Welcome, {user.email}</p>
 *       <button onClick={signOut}>Sign Out</button>
 *     </div>
 *   );
 * }
 * ```
 */
export function useAuth(): AuthContextValue {
  const context = useContext(AuthContext);

  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }

  return context;
}

/**
 * Higher-order component to require authentication
 *
 * @param Component - Component to wrap
 * @returns Wrapped component that requires authentication
 *
 * @example
 * ```tsx
 * const ProtectedPage = withAuth(() => {
 *   return <div>Protected content</div>;
 * });
 * ```
 */
export function withAuth<P extends object>(
  Component: React.ComponentType<P>
): React.ComponentType<P> {
  return function AuthenticatedComponent(props: P) {
    const { isAuthenticated, isLoading } = useAuth();

    if (isLoading) {
      return <div>Loading...</div>;
    }

    if (!isAuthenticated) {
      // Redirect to sign-in page
      if (typeof window !== 'undefined') {
        window.location.href = '/auth/signin';
      }
      return null;
    }

    return <Component {...props} />;
  };
}
