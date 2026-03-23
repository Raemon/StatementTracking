import { useRef, useState } from 'react';
import { useQueryClient } from '@tanstack/react-query';
import { exportDatabase, importDatabase, clearDatabase } from '../api/client';

type Status = { type: 'idle' } | { type: 'loading'; action: string } | { type: 'success'; message: string } | { type: 'error'; message: string };

export default function Admin() {
  const queryClient = useQueryClient();
  const fileRef = useRef<HTMLInputElement>(null);
  const [status, setStatus] = useState<Status>({ type: 'idle' });
  const [confirmClear, setConfirmClear] = useState(false);

  const busy = status.type === 'loading';

  async function handleExport() {
    setStatus({ type: 'loading', action: 'Exporting' });
    try {
      const blob = await exportDatabase();
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `quote_tracker_${new Date().toISOString().slice(0, 10)}.json`;
      a.click();
      URL.revokeObjectURL(url);
      setStatus({ type: 'success', message: 'Database exported successfully.' });
    } catch (e: any) {
      setStatus({ type: 'error', message: e.message });
    }
  }

  async function handleImport() {
    const file = fileRef.current?.files?.[0];
    if (!file) return;
    setStatus({ type: 'loading', action: 'Importing' });
    try {
      const result = await importDatabase(file);
      queryClient.invalidateQueries();
      const { people, articles, quotes } = result.imported;
      setStatus({
        type: 'success',
        message: `Imported ${people} people, ${articles} articles, ${quotes} quotes.`,
      });
      if (fileRef.current) fileRef.current.value = '';
    } catch (e: any) {
      setStatus({ type: 'error', message: e.message });
    }
  }

  async function handleClear() {
    if (!confirmClear) {
      setConfirmClear(true);
      return;
    }
    setConfirmClear(false);
    setStatus({ type: 'loading', action: 'Clearing' });
    try {
      const result = await clearDatabase();
      queryClient.invalidateQueries();
      const { people, articles, quotes } = result.deleted;
      setStatus({
        type: 'success',
        message: `Deleted ${quotes} quotes, ${articles} articles, ${people} people.`,
      });
    } catch (e: any) {
      setStatus({ type: 'error', message: e.message });
    }
  }

  return (
    <div className="max-w-2xl mx-auto space-y-8">
      <div>
        <h1 className="text-2xl font-bold text-slate-900">Admin</h1>
        <p className="text-sm text-slate-500 mt-1">
          Export, import, or clear the database to transfer data between environments.
        </p>
      </div>

      {status.type === 'loading' && (
        <div className="flex items-center gap-3 px-4 py-3 bg-blue-50 border border-blue-200 text-blue-700 rounded-lg text-sm">
          <span className="inline-block w-4 h-4 border-2 border-blue-300 border-t-blue-600 rounded-full animate-spin" />
          {status.action}…
        </div>
      )}

      {status.type === 'success' && (
        <div className="px-4 py-3 bg-emerald-50 border border-emerald-200 text-emerald-700 rounded-lg text-sm">
          {status.message}
        </div>
      )}

      {status.type === 'error' && (
        <div className="px-4 py-3 bg-red-50 border border-red-200 text-red-700 rounded-lg text-sm">
          {status.message}
        </div>
      )}

      {/* Export */}
      <section className="bg-white rounded-xl border border-slate-200 p-6">
        <h2 className="text-lg font-semibold text-slate-800">Export Database</h2>
        <p className="text-sm text-slate-500 mt-1">
          Download the full database as a JSON file you can import elsewhere.
        </p>
        <button
          onClick={handleExport}
          disabled={busy}
          className="mt-4 px-4 py-2 bg-blue-600 text-white text-sm font-medium rounded-lg hover:bg-blue-700 disabled:opacity-50 transition-colors"
        >
          Download Export
        </button>
      </section>

      {/* Import */}
      <section className="bg-white rounded-xl border border-slate-200 p-6">
        <h2 className="text-lg font-semibold text-slate-800">Import Database</h2>
        <p className="text-sm text-slate-500 mt-1">
          Upload a previously exported JSON file. This replaces all existing data.
        </p>
        <div className="mt-4 flex items-center gap-3">
          <input
            ref={fileRef}
            type="file"
            accept=".json"
            className="text-sm text-slate-600 file:mr-3 file:px-4 file:py-2 file:rounded-lg file:border-0 file:text-sm file:font-medium file:bg-slate-100 file:text-slate-700 hover:file:bg-slate-200 file:cursor-pointer file:transition-colors"
          />
          <button
            onClick={handleImport}
            disabled={busy}
            className="px-4 py-2 bg-blue-600 text-white text-sm font-medium rounded-lg hover:bg-blue-700 disabled:opacity-50 transition-colors"
          >
            Import
          </button>
        </div>
      </section>

      {/* Clear */}
      <section className="bg-white rounded-xl border border-red-200 p-6">
        <h2 className="text-lg font-semibold text-red-700">Clear Database</h2>
        <p className="text-sm text-slate-500 mt-1">
          Permanently delete all people, articles, and quotes. This cannot be undone.
        </p>
        {confirmClear ? (
          <div className="mt-4 flex items-center gap-3">
            <span className="text-sm font-medium text-red-600">Are you sure?</span>
            <button
              onClick={handleClear}
              disabled={busy}
              className="px-4 py-2 bg-red-600 text-white text-sm font-medium rounded-lg hover:bg-red-700 disabled:opacity-50 transition-colors"
            >
              Yes, delete everything
            </button>
            <button
              onClick={() => setConfirmClear(false)}
              className="px-4 py-2 bg-slate-100 text-slate-700 text-sm font-medium rounded-lg hover:bg-slate-200 transition-colors"
            >
              Cancel
            </button>
          </div>
        ) : (
          <button
            onClick={handleClear}
            disabled={busy}
            className="mt-4 px-4 py-2 bg-red-600 text-white text-sm font-medium rounded-lg hover:bg-red-700 disabled:opacity-50 transition-colors"
          >
            Clear All Data
          </button>
        )}
      </section>
    </div>
  );
}
