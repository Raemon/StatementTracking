import { useState, useRef, useEffect } from 'react';

interface TagOption {
  name: string;
  label?: string;
}

interface Props {
  selected: string[];
  options: TagOption[];
  onChange: (next: string[]) => void;
  placeholder?: string;
  /** Color scheme for pills: 'blue' (jurisdictions) or 'violet' (topics) */
  color?: 'blue' | 'violet';
}

export default function TagSelect({
  selected,
  options,
  onChange,
  placeholder = 'Search or add tags...',
  color = 'blue',
}: Props) {
  const [filter, setFilter] = useState('');
  const [open, setOpen] = useState(false);
  const containerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    function handleClick(e: MouseEvent) {
      if (containerRef.current && !containerRef.current.contains(e.target as Node)) {
        setOpen(false);
      }
    }
    document.addEventListener('mousedown', handleClick);
    return () => document.removeEventListener('mousedown', handleClick);
  }, []);

  const selectedSet = new Set(selected);
  const filterLower = filter.toLowerCase();

  const filtered = options.filter((o) => {
    if (selectedSet.has(o.name)) return true;
    if (!filter) return true;
    return (
      o.name.toLowerCase().includes(filterLower) ||
      (o.label && o.label.toLowerCase().includes(filterLower))
    );
  });

  const selectedFirst = [
    ...filtered.filter((o) => selectedSet.has(o.name)),
    ...filtered.filter((o) => !selectedSet.has(o.name)),
  ];

  const exactMatch = options.some((o) => o.name.toLowerCase() === filterLower);
  const canCreate = filter.trim().length > 0 && !exactMatch;

  function toggle(name: string) {
    if (selectedSet.has(name)) {
      onChange(selected.filter((s) => s !== name));
    } else {
      onChange([...selected, name]);
    }
  }

  function addNew() {
    const name = filter.trim();
    if (!name) return;
    if (!selectedSet.has(name)) {
      onChange([...selected, name]);
    }
    setFilter('');
  }

  function handleKeyDown(e: React.KeyboardEvent) {
    if (e.key === 'Enter') {
      e.preventDefault();
      if (canCreate) addNew();
    }
    if (e.key === 'Escape') {
      setOpen(false);
    }
  }

  const pillBg = color === 'violet'
    ? 'bg-violet-50 border-violet-200 text-violet-800'
    : 'bg-sky-50 border-sky-200 text-sky-800';
  const pillX = color === 'violet' ? 'text-violet-400 hover:text-violet-600' : 'text-sky-400 hover:text-sky-600';
  const checkColor = color === 'violet' ? 'text-violet-600 focus:ring-violet-500' : 'text-blue-600 focus:ring-blue-500';

  const extraNames = selected.filter((n) => !options.some((o) => o.name === n));

  return (
    <div ref={containerRef} className="relative">
      {selected.length > 0 && (
        <div className="flex flex-wrap gap-1 mb-1.5">
          {selected.map((name) => {
            const isExtra = extraNames.includes(name);
            return (
              <span
                key={name}
                className={`inline-flex items-center gap-0.5 rounded border px-1.5 py-0.5 text-[11px] font-medium ${
                  isExtra
                    ? 'bg-emerald-50 border-emerald-200 text-emerald-800'
                    : pillBg
                }`}
              >
                {name}
                <button
                  type="button"
                  onClick={(e) => {
                    e.stopPropagation();
                    toggle(name);
                  }}
                  className={`ml-0.5 ${isExtra ? 'text-emerald-400 hover:text-emerald-600' : pillX}`}
                  aria-label={`Remove ${name}`}
                >
                  &times;
                </button>
              </span>
            );
          })}
        </div>
      )}

      <input
        type="text"
        value={filter}
        onChange={(e) => setFilter(e.target.value)}
        onFocus={() => setOpen(true)}
        onKeyDown={handleKeyDown}
        placeholder={placeholder}
        className="w-full px-3 py-2 border border-slate-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
      />

      {open && (
        <div className="absolute z-20 mt-1 w-full rounded-lg border border-slate-200 bg-white shadow-lg">
          <div className="max-h-48 overflow-y-auto py-1">
            {selectedFirst.length === 0 && !canCreate && (
              <div className="px-3 py-2 text-xs text-slate-400 italic">
                No tags match &ldquo;{filter}&rdquo;
              </div>
            )}
            {selectedFirst.map((o) => (
              <label
                key={o.name}
                className="flex cursor-pointer items-center gap-2.5 px-3 py-1.5 text-sm text-slate-700 hover:bg-slate-50"
              >
                <input
                  type="checkbox"
                  checked={selectedSet.has(o.name)}
                  onChange={() => toggle(o.name)}
                  className={`rounded border-slate-300 ${checkColor}`}
                />
                <span className="min-w-0 flex-1">
                  {o.name}
                  {o.label && <span className="text-slate-400 ml-1">({o.label})</span>}
                </span>
              </label>
            ))}
            {canCreate && (
              <button
                type="button"
                onClick={addNew}
                className="w-full px-3 py-1.5 text-left text-sm text-blue-600 hover:bg-blue-50 flex items-center gap-2 border-t border-slate-100"
              >
                <svg xmlns="http://www.w3.org/2000/svg" className="h-3.5 w-3.5" viewBox="0 0 20 20" fill="currentColor">
                  <path fillRule="evenodd" d="M10 3a1 1 0 011 1v5h5a1 1 0 110 2h-5v5a1 1 0 11-2 0v-5H4a1 1 0 110-2h5V4a1 1 0 011-1z" clipRule="evenodd" />
                </svg>
                Add &ldquo;{filter.trim()}&rdquo;
              </button>
            )}
          </div>
        </div>
      )}
    </div>
  );
}
