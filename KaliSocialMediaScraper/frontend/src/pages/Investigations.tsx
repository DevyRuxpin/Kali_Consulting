import React, { useEffect, useState } from 'react';
import { fetchInvestigations } from '../services/investigations';

interface Investigation {
  id: number;
  title: string;
  description?: string;
  target_type: string;
  target_value: string;
  status: string;
  progress: number;
  created_at: string;
  updated_at?: string;
}

interface CreateInvestigationForm {
  target_type: string;
  target_value: string;
  analysis_depth: string;
  include_network_analysis: boolean;
  include_timeline_analysis: boolean;
  include_threat_assessment: boolean;
}

const Investigations: React.FC = () => {
  const [investigations, setInvestigations] = useState<Investigation[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [showCreateForm, setShowCreateForm] = useState(false);
  const [creating, setCreating] = useState(false);
  const [formData, setFormData] = useState<CreateInvestigationForm>({
    target_type: 'domain',
    target_value: '',
    analysis_depth: 'standard',
    include_network_analysis: true,
    include_timeline_analysis: true,
    include_threat_assessment: true,
  });

  useEffect(() => {
    fetchInvestigations()
      .then(setInvestigations)
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false));
  }, []);

  const handleCreateInvestigation = async (e: React.FormEvent) => {
    e.preventDefault();
    setCreating(true);
    
    const payload = {
      ...formData,
      platforms: [],
      analysis_options: {},
    };
    try {
      const response = await fetch('/api/v1/investigations/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(payload),
      });
      
      if (response.ok) {
        const result = await response.json();
        setShowCreateForm(false);
        setFormData({
          target_type: 'domain',
          target_value: '',
          analysis_depth: 'standard',
          include_network_analysis: true,
          include_timeline_analysis: true,
          include_threat_assessment: true,
        });
        // Refresh the investigations list
        fetchInvestigations()
          .then(setInvestigations)
          .catch((err) => setError(err.message));
      } else {
        const errorData = await response.json();
        setError(`Failed to create investigation: ${errorData.detail || 'Unknown error'}`);
      }
    } catch (err) {
      setError(`Failed to create investigation: ${err instanceof Error ? err.message : 'Unknown error'}`);
    } finally {
      setCreating(false);
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-2xl font-bold text-gray-900 dark:text-white">
            Investigations
          </h1>
          <p className="text-gray-600 dark:text-gray-400">
            Manage and monitor your OSINT investigations
          </p>
        </div>
        <button
          onClick={() => setShowCreateForm(true)}
          className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-md"
        >
          Create Investigation
        </button>
      </div>

      {showCreateForm && (
        <div className="card">
          <div className="card-body">
            <h3 className="text-lg font-semibold mb-4">Create New Investigation</h3>
            <form onSubmit={handleCreateInvestigation} className="space-y-4">
              <div>
                <label className="block text-sm font-medium mb-1">Target Type</label>
                <select
                  value={formData.target_type}
                  onChange={(e) => setFormData({...formData, target_type: e.target.value})}
                  className="w-full p-2 border rounded-md"
                  required
                >
                  <option value="domain">Domain</option>
                  <option value="email">Email</option>
                  <option value="username">Username</option>
                  <option value="github_repository">GitHub Repository</option>
                  <option value="social_media">Social Media</option>
                </select>
              </div>
              
              <div>
                <label className="block text-sm font-medium mb-1">Target Value</label>
                <input
                  type="text"
                  value={formData.target_value}
                  onChange={(e) => setFormData({...formData, target_value: e.target.value})}
                  className="w-full p-2 border rounded-md"
                  placeholder="Enter target value..."
                  required
                />
              </div>
              
              <div>
                <label className="block text-sm font-medium mb-1">Analysis Depth</label>
                <select
                  value={formData.analysis_depth}
                  onChange={(e) => setFormData({...formData, analysis_depth: e.target.value})}
                  className="w-full p-2 border rounded-md"
                >
                  <option value="basic">Basic</option>
                  <option value="standard">Standard</option>
                  <option value="deep">Deep</option>
                  <option value="comprehensive">Comprehensive</option>
                </select>
              </div>
              
              <div className="space-y-2">
                <label className="block text-sm font-medium">Analysis Options</label>
                <div className="space-y-2">
                  <label className="flex items-center">
                    <input
                      type="checkbox"
                      checked={formData.include_network_analysis}
                      onChange={(e) => setFormData({...formData, include_network_analysis: e.target.checked})}
                      className="mr-2"
                    />
                    Include Network Analysis
                  </label>
                  <label className="flex items-center">
                    <input
                      type="checkbox"
                      checked={formData.include_timeline_analysis}
                      onChange={(e) => setFormData({...formData, include_timeline_analysis: e.target.checked})}
                      className="mr-2"
                    />
                    Include Timeline Analysis
                  </label>
                  <label className="flex items-center">
                    <input
                      type="checkbox"
                      checked={formData.include_threat_assessment}
                      onChange={(e) => setFormData({...formData, include_threat_assessment: e.target.checked})}
                      className="mr-2"
                    />
                    Include Threat Assessment
                  </label>
                </div>
              </div>
              
              <div className="flex space-x-2">
                <button
                  type="submit"
                  disabled={creating}
                  className="bg-green-600 hover:bg-green-700 text-white px-4 py-2 rounded-md disabled:opacity-50"
                >
                  {creating ? 'Creating...' : 'Create Investigation'}
                </button>
                <button
                  type="button"
                  onClick={() => setShowCreateForm(false)}
                  className="bg-gray-500 hover:bg-gray-600 text-white px-4 py-2 rounded-md"
                >
                  Cancel
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      <div className="card">
        <div className="card-body">
          {loading && <p>Loading investigations...</p>}
          {error && <p className="text-red-500">Error: {error}</p>}
          {!loading && !error && investigations.length === 0 && (
            <p className="text-gray-500 dark:text-gray-400">No investigations found.</p>
          )}
          {!loading && !error && investigations.length > 0 && (
            <table className="min-w-full divide-y divide-gray-200 dark:divide-gray-700">
              <thead>
                <tr>
                  <th className="px-4 py-2 text-left">Title</th>
                  <th className="px-4 py-2 text-left">Target</th>
                  <th className="px-4 py-2 text-left">Status</th>
                  <th className="px-4 py-2 text-left">Progress</th>
                  <th className="px-4 py-2 text-left">Created</th>
                </tr>
              </thead>
              <tbody>
                {investigations.map((inv) => (
                  <tr key={inv.id}>
                    <td className="px-4 py-2">{inv.title}</td>
                    <td className="px-4 py-2">{inv.target_type}: {inv.target_value}</td>
                    <td className="px-4 py-2">{inv.status}</td>
                    <td className="px-4 py-2">{inv.progress}%</td>
                    <td className="px-4 py-2">{new Date(inv.created_at).toLocaleString()}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
        </div>
      </div>
    </div>
  );
};

export default Investigations; 