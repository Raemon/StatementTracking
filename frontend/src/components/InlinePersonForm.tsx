import { useState } from 'react';
import type { PersonCreate } from '../types';

interface Props {
  defaultName?: string;
  onSave: (person: PersonCreate) => void;
  onCancel: () => void;
}

const PARTIES = ['Democrat', 'Republican', 'Independent', 'Other'];
const CHAMBERS = ['Senate', 'House', 'Executive', 'Other'];
const US_STATES = [
  'AL','AK','AZ','AR','CA','CO','CT','DE','FL','GA','HI','ID','IL','IN','IA',
  'KS','KY','LA','ME','MD','MA','MI','MN','MS','MO','MT','NE','NV','NH','NJ',
  'NM','NY','NC','ND','OH','OK','OR','PA','RI','SC','SD','TN','TX','UT','VT',
  'VA','WA','WV','WI','WY','DC',
];

export default function InlinePersonForm({ defaultName = '', onSave, onCancel }: Props) {
  const [form, setForm] = useState<PersonCreate>({
    name: defaultName,
    type: 'elected',
    party: null,
    role: null,
    chamber: null,
    state: null,
    employer: null,
  });

  function update(field: string, value: string | null) {
    setForm((prev) => ({ ...prev, [field]: value || null }));
  }

  function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    if (!form.name.trim()) return;
    onSave(form);
  }

  return (
    <form
      onSubmit={handleSubmit}
      className="mt-2 p-3 bg-slate-50 border border-slate-200 rounded-lg space-y-3"
    >
      <p className="text-xs font-semibold text-slate-600 uppercase tracking-wider">
        New Person
      </p>

      <div className="grid grid-cols-2 gap-2">
        <div className="col-span-2">
          <input
            type="text"
            value={form.name}
            onChange={(e) => update('name', e.target.value)}
            placeholder="Full name"
            className="w-full px-2.5 py-1.5 border border-slate-300 rounded text-sm"
            required
          />
        </div>

        <select
          value={form.type}
          onChange={(e) => update('type', e.target.value)}
          className="px-2.5 py-1.5 border border-slate-300 rounded text-sm"
        >
          <option value="elected">Elected</option>
          <option value="staff">Staff</option>
        </select>

        <select
          value={form.party || ''}
          onChange={(e) => update('party', e.target.value)}
          className="px-2.5 py-1.5 border border-slate-300 rounded text-sm"
        >
          <option value="">Party...</option>
          {PARTIES.map((p) => <option key={p} value={p}>{p}</option>)}
        </select>

        <input
          type="text"
          value={form.role || ''}
          onChange={(e) => update('role', e.target.value)}
          placeholder="Role (e.g. Senator)"
          className="px-2.5 py-1.5 border border-slate-300 rounded text-sm"
        />

        <select
          value={form.chamber || ''}
          onChange={(e) => update('chamber', e.target.value)}
          className="px-2.5 py-1.5 border border-slate-300 rounded text-sm"
        >
          <option value="">Chamber...</option>
          {CHAMBERS.map((c) => <option key={c} value={c}>{c}</option>)}
        </select>

        <select
          value={form.state || ''}
          onChange={(e) => update('state', e.target.value)}
          className="px-2.5 py-1.5 border border-slate-300 rounded text-sm"
        >
          <option value="">State...</option>
          {US_STATES.map((s) => <option key={s} value={s}>{s}</option>)}
        </select>

        {form.type === 'staff' && (
          <input
            type="text"
            value={form.employer || ''}
            onChange={(e) => update('employer', e.target.value)}
            placeholder="Employer"
            className="px-2.5 py-1.5 border border-slate-300 rounded text-sm"
          />
        )}
      </div>

      <div className="flex gap-2">
        <button
          type="submit"
          className="px-3 py-1.5 bg-blue-600 text-white text-sm rounded hover:bg-blue-700 font-medium"
        >
          Create Person
        </button>
        <button
          type="button"
          onClick={onCancel}
          className="px-3 py-1.5 text-sm text-slate-600 hover:text-slate-800"
        >
          Cancel
        </button>
      </div>
    </form>
  );
}
