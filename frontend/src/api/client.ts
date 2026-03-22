import type {
  ExtractResponse,
  SaveRequest,
  SaveResponse,
  Person,
  PersonDetail,
  QuoteListResponse,
  QuoteWithDetails,
  Stats,
} from '../types';

const BASE = '/api';

async function request<T>(path: string, options?: RequestInit): Promise<T> {
  const res = await fetch(`${BASE}${path}`, {
    headers: { 'Content-Type': 'application/json' },
    ...options,
  });
  if (!res.ok) {
    const body = await res.json().catch(() => ({}));
    throw new Error(body.detail || `Request failed: ${res.status}`);
  }
  return res.json();
}

// ── Articles ─────────────────────────────────────────────────────────

export function extractArticle(url: string): Promise<ExtractResponse> {
  return request('/articles/extract', {
    method: 'POST',
    body: JSON.stringify({ url }),
  });
}

export function saveArticle(data: SaveRequest): Promise<SaveResponse> {
  return request('/articles/save', {
    method: 'POST',
    body: JSON.stringify(data),
  });
}

// ── People ───────────────────────────────────────────────────────────

export function fetchPeople(search?: string): Promise<Person[]> {
  const params = search ? `?search=${encodeURIComponent(search)}` : '';
  return request(`/people${params}`);
}

export function fetchPerson(id: number): Promise<PersonDetail> {
  return request(`/people/${id}`);
}

export function updatePerson(
  id: number,
  data: Partial<Person>,
): Promise<Person> {
  return request(`/people/${id}`, {
    method: 'PUT',
    body: JSON.stringify(data),
  });
}

// ── Quotes ───────────────────────────────────────────────────────────

export interface QuoteFilters {
  person_id?: number;
  search?: string;
  party?: string;
  type?: string;
  from_date?: string;
  to_date?: string;
  page?: number;
  page_size?: number;
}

export function fetchQuotes(filters: QuoteFilters = {}): Promise<QuoteListResponse> {
  const params = new URLSearchParams();
  Object.entries(filters).forEach(([key, val]) => {
    if (val !== undefined && val !== null && val !== '') {
      params.set(key, String(val));
    }
  });
  const qs = params.toString();
  return request(`/quotes${qs ? '?' + qs : ''}`);
}

export function fetchQuote(id: number): Promise<QuoteWithDetails> {
  return request(`/quotes/${id}`);
}

export function updateQuote(
  id: number,
  data: { quote_text?: string; context?: string; date_said?: string | null; person_id?: number },
): Promise<QuoteWithDetails> {
  return request(`/quotes/${id}`, {
    method: 'PUT',
    body: JSON.stringify(data),
  });
}

export function deleteQuote(id: number): Promise<{ ok: boolean }> {
  return request(`/quotes/${id}`, { method: 'DELETE' });
}

// ── Stats ────────────────────────────────────────────────────────────

export function fetchStats(): Promise<Stats> {
  return request('/stats');
}
