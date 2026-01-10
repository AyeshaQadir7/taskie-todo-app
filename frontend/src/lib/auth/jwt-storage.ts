/**
 * JWT Token Storage Utility
 *
 * SECURITY: This module handles secure storage of JWT tokens using HttpOnly cookies
 * (server-set, not accessible from JavaScript) to prevent XSS attacks.
 *
 * Tokens are stored as HttpOnly cookies set by the server (via Next.js middleware)
 * and automatically included in all fetch requests. This prevents malicious scripts
 * from accessing the token via document.cookie or localStorage.
 *
 * Spec: 002-authentication-jwt
 * Created: 2026-01-09
 */

/**
 * Cookie name for JWT token (HttpOnly, Secure, SameSite)
 * This cookie is set by Next.js middleware from the Authorization header
 */
const JWT_COOKIE_NAME = 'taskie_jwt';

/**
 * SECURITY: Retrieve JWT token from HttpOnly cookie via API call
 *
 * Since HttpOnly cookies cannot be accessed from JavaScript, we verify token
 * presence by attempting to access a protected endpoint. The browser will
 * automatically include the cookie in the request.
 *
 * The actual token storage is handled by Next.js middleware which:
 * 1. Receives token from Better Auth authentication
 * 2. Sets HttpOnly, Secure, SameSite=Strict cookie
 * 3. Cookie is automatically sent on all same-origin requests
 *
 * @returns True if authenticated (HttpOnly cookie is valid), false otherwise
 *
 * @example
 * ```ts
 * if (await isAuthenticated()) {
 *   // User has a valid token in HttpOnly cookie
 * }
 * ```
 */
export async function isAuthenticated(): Promise<boolean> {
  if (typeof window === 'undefined') {
    return false;
  }

  try {
    // Try to access a protected endpoint to verify cookie validity
    const response = await fetch('/api/auth/verify', {
      method: 'GET',
      credentials: 'include', // Include HttpOnly cookies
    });
    return response.ok;
  } catch {
    return false;
  }
}

/**
 * SECURITY: HTTP client automatically sends HttpOnly cookies
 *
 * This function is provided for API client initialization.
 * The actual token is in an HttpOnly cookie and cannot be accessed from JavaScript.
 * Modern browsers automatically include it in requests with credentials: 'include'.
 *
 * @param token - Unused (provided for API compatibility with Better Auth)
 *
 * @example
 * ```ts
 * // After Better Auth returns token from sign-up/sign-in:
 * await initializeAuth(authToken);
 * // Browser automatically includes HttpOnly cookie in subsequent requests
 * ```
 */
export async function initializeAuth(token?: string): Promise<void> {
  if (typeof window === 'undefined') {
    return;
  }

  try {
    // If token provided, send to backend to set HttpOnly cookie via middleware
    if (token) {
      const response = await fetch('/api/auth/set-cookie', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`,
        },
        credentials: 'include',
        body: JSON.stringify({ token }),
      });

      if (!response.ok) {
        throw new Error('Failed to initialize authentication');
      }
    }
  } catch (error) {
    // Log error without exposing sensitive token data
    if (error instanceof Error) {
      console.error('Authentication initialization failed');
    }
  }
}

/**
 * SECURITY: Clear HttpOnly cookie via API call
 *
 * Since we cannot directly delete HttpOnly cookies from JavaScript,
 * we call the backend to clear the cookie and any session data.
 *
 * @example
 * ```ts
 * await clearAuth();
 * // HttpOnly cookie is cleared on backend
 * ```
 */
export async function clearAuth(): Promise<void> {
  if (typeof window === 'undefined') {
    return;
  }

  try {
    await fetch('/api/auth/logout', {
      method: 'POST',
      credentials: 'include',
    });
  } catch (error) {
    // Continue logout even if API call fails
  }
}
