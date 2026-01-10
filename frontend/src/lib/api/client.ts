/**
 * API Client with JWT Authorization Header Injection
 *
 * This module provides an HTTP client wrapper that automatically injects
 * JWT tokens into the Authorization header for all API requests.
 *
 * Spec: 002-authentication-jwt
 * Created: 2026-01-09
 */

import { getStoredToken, clearStoredToken } from '../auth/jwt-storage';

/**
 * Base API configuration
 */
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

/**
 * HTTP method types
 */
type HttpMethod = 'GET' | 'POST' | 'PUT' | 'PATCH' | 'DELETE';

/**
 * API request options
 */
interface RequestOptions {
  method: HttpMethod;
  headers?: Record<string, string>;
  body?: any;
  requiresAuth?: boolean;  // Default: true
}

/**
 * API response wrapper
 */
interface ApiResponse<T = any> {
  data: T | null;
  error: string | null;
  status: number;
}

/**
 * API error class
 */
export class ApiError extends Error {
  constructor(
    message: string,
    public status: number,
    public details?: any
  ) {
    super(message);
    this.name = 'ApiError';
  }
}

/**
 * Create Authorization header with Bearer token
 *
 * @returns Authorization header object or empty object if no token
 */
function createAuthHeader(): Record<string, string> {
  const token = getStoredToken();

  if (!token) {
    return {};
  }

  return {
    'Authorization': `Bearer ${token}`
  };
}

/**
 * Handle API response and errors
 *
 * @param response - Fetch API response
 * @returns Parsed response data or throws ApiError
 */
async function handleResponse<T>(response: Response): Promise<T> {
  // Parse response body
  let body: any = null;
  const contentType = response.headers.get('content-type');

  if (contentType && contentType.includes('application/json')) {
    try {
      body = await response.json();
    } catch (e) {
      // Response claimed to be JSON but couldn't parse
      body = null;
    }
  } else {
    // Non-JSON response (e.g., 204 No Content)
    body = null;
  }

  // Handle success responses (2xx)
  if (response.ok) {
    return body as T;
  }

  // Handle authentication errors (401 Unauthorized)
  if (response.status === 401) {
    // Token is invalid or expired - clear stored token
    clearStoredToken();

    // Redirect to sign-in page (if on client side)
    if (typeof window !== 'undefined') {
      window.location.href = '/auth/signin';
    }

    throw new ApiError(
      body?.message || 'Authentication required',
      401,
      body
    );
  }

  // Handle authorization errors (403 Forbidden)
  if (response.status === 403) {
    throw new ApiError(
      body?.message || 'Access denied',
      403,
      body
    );
  }

  // Handle validation errors (422 Unprocessable Entity)
  if (response.status === 422) {
    throw new ApiError(
      body?.message || 'Validation error',
      422,
      body?.errors || body
    );
  }

  // Handle all other errors
  throw new ApiError(
    body?.message || `HTTP ${response.status}: ${response.statusText}`,
    response.status,
    body
  );
}

/**
 * Make an authenticated API request
 *
 * @param endpoint - API endpoint path (relative to API_BASE_URL)
 * @param options - Request options (method, headers, body, etc.)
 * @returns API response data
 * @throws ApiError if request fails
 */
export async function apiRequest<T = any>(
  endpoint: string,
  options: RequestOptions
): Promise<T> {
  const { method, headers = {}, body, requiresAuth = true } = options;

  // Build full URL
  const url = `${API_BASE_URL}${endpoint}`;

  // Build request headers
  const requestHeaders: Record<string, string> = {
    'Content-Type': 'application/json',
    ...headers,
  };

  // Add Authorization header if authentication is required
  if (requiresAuth) {
    const authHeader = createAuthHeader();

    if (!authHeader.Authorization) {
      throw new ApiError('No authentication token found', 401);
    }

    Object.assign(requestHeaders, authHeader);
  }

  // Build request options
  const fetchOptions: RequestInit = {
    method,
    headers: requestHeaders,
    body: body ? JSON.stringify(body) : undefined,
  };

  // Make request
  try {
    const response = await fetch(url, fetchOptions);
    return await handleResponse<T>(response);
  } catch (error) {
    // Re-throw ApiError as-is
    if (error instanceof ApiError) {
      throw error;
    }

    // Wrap network errors
    throw new ApiError(
      `Network error: ${error instanceof Error ? error.message : 'Unknown error'}`,
      0
    );
  }
}

/**
 * Convenience method for GET requests
 */
export async function get<T = any>(endpoint: string, requiresAuth: boolean = true): Promise<T> {
  return apiRequest<T>(endpoint, { method: 'GET', requiresAuth });
}

/**
 * Convenience method for POST requests
 */
export async function post<T = any>(
  endpoint: string,
  body: any,
  requiresAuth: boolean = true
): Promise<T> {
  return apiRequest<T>(endpoint, { method: 'POST', body, requiresAuth });
}

/**
 * Convenience method for PUT requests
 */
export async function put<T = any>(
  endpoint: string,
  body: any,
  requiresAuth: boolean = true
): Promise<T> {
  return apiRequest<T>(endpoint, { method: 'PUT', body, requiresAuth });
}

/**
 * Convenience method for PATCH requests
 */
export async function patch<T = any>(
  endpoint: string,
  body: any,
  requiresAuth: boolean = true
): Promise<T> {
  return apiRequest<T>(endpoint, { method: 'PATCH', body, requiresAuth });
}

/**
 * Convenience method for DELETE requests
 */
export async function del<T = any>(endpoint: string, requiresAuth: boolean = true): Promise<T> {
  return apiRequest<T>(endpoint, { method: 'DELETE', requiresAuth });
}

/**
 * Safe API request wrapper that returns response object instead of throwing
 *
 * @param endpoint - API endpoint path
 * @param options - Request options
 * @returns API response with data or error
 */
export async function safeApiRequest<T = any>(
  endpoint: string,
  options: RequestOptions
): Promise<ApiResponse<T>> {
  try {
    const data = await apiRequest<T>(endpoint, options);
    return {
      data,
      error: null,
      status: 200
    };
  } catch (error) {
    if (error instanceof ApiError) {
      return {
        data: null,
        error: error.message,
        status: error.status
      };
    }

    return {
      data: null,
      error: error instanceof Error ? error.message : 'Unknown error',
      status: 0
    };
  }
}
