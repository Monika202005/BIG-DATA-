import React, { useState, useEffect } from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { Activity, BarChart2 } from 'lucide-react';
import axios from 'axios';

const AnalyticsDashboard = () => {
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchAnalytics = async () => {
      try {
        const response = await axios.get('http://localhost:8000/analytics');
        setStats(response.data);
      } catch (error) {
        console.error("Error fetching analytics:", error);
      } finally {
        setLoading(false);
      }
    };
    
    fetchAnalytics();
  }, []);

  if (loading) return <div className="text-center p-10 text-slate-500 animate-pulse">Loading analytics...</div>;
  if (!stats) return <div className="text-center p-10 text-red-500 bg-red-50 rounded-lg">Failed to load analytics data.</div>;

  const chartData = Object.entries(stats.top_items).map(([name, count]) => ({
    name,
    purchases: count
  }));

  return (
    <div className="bg-white rounded-2xl shadow-sm border border-slate-200 overflow-hidden">
      <div className="bg-slate-50 px-6 py-4 border-b border-slate-200 flex items-center">
        <Activity className="text-brand-500 mr-2" size={20} />
        <h2 className="text-lg font-bold text-slate-800">System Analytics Engine</h2>
      </div>
      
      <div className="p-6 grid grid-cols-1 lg:grid-cols-2 gap-8">
        
        {/* Frequent Items Chart */}
        <div>
          <h3 className="font-semibold text-slate-700 mb-4 flex items-center">
            <BarChart2 size={16} className="mr-2 text-brand-600" />
            Top 10 Most Frequent Products
          </h3>
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={chartData} layout="vertical" margin={{ top: 5, right: 30, left: 20, bottom: 5 }}>
                <CartesianGrid strokeDasharray="3 3" horizontal={false} stroke="#E2E8F0" />
                <XAxis type="number" stroke="#64748B" />
                <YAxis dataKey="name" type="category" width={100} stroke="#64748B" fontSize={12} tick={{fill: '#334155'}} />
                <Tooltip 
                  contentStyle={{ borderRadius: '8px', border: '1px solid #E2E8F0', boxShadow: '0 4px 6px -1px rgb(0 0 0 / 0.1)' }}
                  cursor={{fill: '#F8FAFC'}}
                />
                <Bar dataKey="purchases" fill="#3B82F6" radius={[0, 4, 4, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Top Rules List */}
        <div>
          <h3 className="font-semibold text-slate-700 mb-4 flex items-center">
            Top Association Rules by Lift
          </h3>
          <div className="space-y-3 max-h-64 overflow-y-auto pr-2">
            {stats.top_rules.map((rule, idx) => (
              <div key={idx} className="bg-slate-50 p-3 rounded-lg border border-slate-100 flex justify-between items-center group hover:bg-brand-50 transition-colors">
                <div className="font-medium text-slate-700 font-mono text-sm">{rule.rule}</div>
                <div className="flex space-x-4 text-xs">
                  <span className="text-slate-500">Conf: <span className="font-bold text-slate-800">{rule.confidence}</span></span>
                  <span className="text-slate-500">Lift: <span className="font-bold text-emerald-600">{rule.lift}</span></span>
                </div>
              </div>
            ))}
          </div>
        </div>
        
      </div>
    </div>
  );
};

export default AnalyticsDashboard;
