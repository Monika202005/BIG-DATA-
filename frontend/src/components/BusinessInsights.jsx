import React, { useState, useEffect } from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import { Activity, BarChart2, TrendingUp, Lightbulb, PackageOpen } from 'lucide-react';
import axios from 'axios';

const BusinessInsights = () => {
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
    
    // Quick polling to keep it updated with ML sliders
    const interval = setInterval(fetchAnalytics, 3000);
    fetchAnalytics();
    return () => clearInterval(interval);
  }, []);

  if (loading) return <div className="text-center p-10 text-slate-500 animate-pulse bg-white rounded-2xl shadow-sm border border-slate-200">Loading Business Intelligence...</div>;
  if (!stats) return <div className="text-center p-10 text-red-500 bg-red-50 rounded-2xl">Failed to load Business Intelligence metrics.</div>;

  const chartData = Object.entries(stats.top_items).map(([name, count]) => ({
    name,
    purchases: count
  }));

  const topRule = stats.top_rules.length > 0 ? stats.top_rules[0] : null;

  return (
    <div className="bg-white rounded-[2rem] shadow-xl shadow-slate-200/40 border border-slate-200/60 overflow-hidden mt-16 group transition-all duration-500">
      <div className="bg-gradient-to-r from-slate-900 to-brand-900 px-8 py-6 flex flex-col sm:flex-row justify-between items-start sm:items-center relative overflow-hidden">
        {/* Background ambient glow */}
        <div className="absolute top-0 right-0 w-64 h-64 bg-white/5 rounded-full blur-3xl -translate-y-1/2 translate-x-1/3"></div>
        
        <div className="flex items-center relative z-10">
          <div className="bg-white/10 p-2.5 rounded-xl mr-4 backdrop-blur-sm border border-white/10">
            <Activity className="text-brand-300" size={24} />
          </div>
          <div>
            <h2 className="text-2xl font-black text-white tracking-tight">Executive Business Insights</h2>
            <p className="text-brand-200 text-sm font-medium">Real-time Data Science Dashboard</p>
          </div>
        </div>
      </div>
      
      <div className="p-8 grid grid-cols-1 lg:grid-cols-2 gap-10">
        
        {/* Most Influential Opportunity */}
        <div className="space-y-6 flex flex-col justify-center">
          <div className="inline-flex items-center space-x-2 bg-amber-50 text-amber-700 font-bold px-4 py-1.5 rounded-full text-sm border border-amber-200 w-max">
            <Lightbulb size={16} className="text-amber-500" />
            <span>Highest Cross-Sell Opportunity</span>
          </div>

          {topRule ? (
            <div className="bg-white border-2 border-brand-100 p-6 rounded-2xl shadow-sm group-hover:border-brand-300 transition-colors">
              <p className="text-xl sm:text-2xl text-slate-800 font-medium leading-relaxed">
                Users who buy <strong className="text-brand-600 bg-brand-50 px-2 rounded">{topRule.rule.split(' -> ')[0]}</strong> have an <strong className="text-emerald-600 bg-emerald-50 px-2 rounded">{(topRule.confidence * 100).toFixed(0)}% probability</strong> of buying <strong className="text-brand-600 bg-brand-50 px-2 rounded">{topRule.rule.split(' -> ')[1]}</strong>.
              </p>
              <div className="mt-6 pt-6 border-t border-slate-100 flex items-center space-x-6">
                <div>
                  <div className="text-xs text-slate-500 uppercase tracking-wider font-semibold">Lift Multiplier</div>
                  <div className="text-2xl font-black text-slate-800 flex items-center">
                   {topRule.lift.toFixed(2)}x <TrendingUp size={20} className="ml-2 text-emerald-500" />
                  </div>
                </div>
                <div>
                  <div className="text-xs text-slate-500 uppercase tracking-wider font-semibold">Confidence</div>
                  <div className="text-2xl font-black text-slate-800">{topRule.confidence.toFixed(2)}</div>
                </div>
              </div>
            </div>
          ) : (
             <div className="bg-white border-2 border-slate-100 p-6 rounded-2xl text-slate-500 flex flex-col items-center justify-center space-y-3 h-48">
               <PackageOpen size={32} className="opacity-50" />
               <span>No dominant rules found at current parameters.</span>
             </div>
          )}
        </div>

        {/* Top Selling Products Chart */}
        <div className="bg-slate-50 rounded-2xl p-6 border border-slate-100">
          <h3 className="font-semibold text-slate-700 mb-6 flex items-center text-lg">
            <BarChart2 size={20} className="mr-2 text-brand-600" />
            Top Selling Products
          </h3>
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={chartData} layout="vertical" margin={{ top: 5, right: 30, left: 20, bottom: 5 }}>
                <CartesianGrid strokeDasharray="3 3" horizontal={false} stroke="#E2E8F0" />
                <XAxis type="number" stroke="#64748B" />
                <YAxis dataKey="name" type="category" width={100} stroke="#64748B" fontSize={12} tick={{fill: '#334155', fontWeight: 600}} />
                <Tooltip 
                  contentStyle={{ borderRadius: '12px', border: 'none', boxShadow: '0 10px 15px -3px rgb(0 0 0 / 0.1)' }}
                  cursor={{fill: '#F1F5F9'}}
                />
                <Bar dataKey="purchases" fill="#3B82F6" radius={[0, 6, 6, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>
        
      </div>
    </div>
  );
};

export default BusinessInsights;
