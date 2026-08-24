// frontend/app/version/page.tsx

export default async function VersionPage() {
  // Tera live Render API call ho raha hai yahan
  const res = await fetch('https://syncrights-version-api.onrender.com/version/match?track_id=trk_021', {
    cache: 'no-store' 
  });
  const data = await res.json();

  return (
    <div className="min-h-screen bg-gray-950 text-white p-10 font-sans">
      <div className="max-w-xl mx-auto bg-gray-900 border border-gray-700 rounded-xl p-6 shadow-lg mt-10">
        <h1 className="text-2xl font-bold text-indigo-400 mb-4">P2: Version Intelligence</h1>
        <p className="text-gray-400 text-sm mb-6">Fetching live data from Render API...</p>
        
        <div className="space-y-4 mt-6">
          <div className="flex justify-between border-b border-gray-800 pb-2">
            <span className="text-gray-400">Track ID</span>
            <span className="font-mono text-green-400 bg-gray-800 px-2 py-1 rounded">{data.track_id}</span>
          </div>
          
          <div className="flex justify-between border-b border-gray-800 pb-2">
            <span className="text-gray-400">Version ID</span>
            <span className="font-mono text-green-400 bg-gray-800 px-2 py-1 rounded">{data.version_id}</span>
          </div>

          <div className="flex justify-between border-b border-gray-800 pb-2">
            <span className="text-gray-400">Display Label</span>
            <span className="font-semibold text-white">{data.display_label}</span>
          </div>
          
          <div className="flex justify-between pb-2">
            <span className="text-gray-400">Version Type</span>
            <span className="font-bold text-xs uppercase tracking-wide bg-indigo-900 text-indigo-300 px-3 py-1 rounded-full">
              {data.version_type}
            </span>
          </div>
        </div>
        
      </div>
    </div>
  );
}