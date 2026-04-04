import React from 'react';
import { Database, TrendingUp, SearchCode, Cpu } from 'lucide-react';

const steps = [
  {
    num: 1,
    title: 'Data Ingestion',
    desc: 'Raw transaction histories are parsed, cleaned, and organized into a Data Warehouse structure.',
    icon: Database,
    color: 'from-blue-500 to-cyan-400'
  },
  {
    num: 2,
    title: 'Pattern Discovery',
    desc: 'The Apriori algorithm scans the one-hot encoded dataset to locate frequent product itemsets.',
    icon: SearchCode,
    color: 'from-fuchsia-500 to-purple-500'
  },
  {
    num: 3,
    title: 'Rule Generation',
    desc: 'Association rules are calculated mathematically based on Support, Confidence, and Lift metrics.',
    icon: TrendingUp,
    color: 'from-emerald-400 to-teal-500'
  },
  {
    num: 4,
    title: 'API Inference',
    desc: 'Rules are cached in memory allowing the FastAPI engine to serve real-time predictions <100ms.',
    icon: Cpu,
    color: 'from-brand-500 to-indigo-600'
  }
];

const SystemExplanation = () => {
  return (
    <div className="py-16 mt-24 border-t border-slate-200/60 bg-white/40 backdrop-blur-3xl rounded-[3rem] shadow-sm mb-12">
      <div className="max-w-5xl mx-auto px-6">
        <div className="text-center mb-16">
           <h2 className="text-3xl font-black text-slate-800 tracking-tight">How This System Works</h2>
           <p className="text-lg text-slate-500 mt-4 max-w-2xl mx-auto">
             A high-level overview of the Machine Learning pipeline powering the intelligent recommendations.
           </p>
        </div>
        
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8 relative">
          
          {/* Connecting Line */}
          <div className="hidden lg:block absolute top-12 left-[10%] right-[10%] h-0.5 bg-slate-200 z-0"></div>

          {steps.map((step, idx) => (
            <div key={idx} className="relative z-10 flex flex-col items-center text-center group">
              <div 
                className={`w-24 h-24 rounded-3xl bg-gradient-to-br ${step.color} p-0.5 shadow-xl shadow-slate-200/50 transform group-hover:-translate-y-2 transition-transform duration-300`}
              >
                <div className="w-full h-full bg-white rounded-[22px] flex items-center justify-center relative overflow-hidden">
                   <div className="absolute inset-0 bg-slate-50 opacity-0 group-hover:opacity-100 transition-opacity"></div>
                   <step.icon size={36} className="text-slate-700 relative z-10" strokeWidth={1.5} />
                </div>
              </div>
              
              <div className="mt-8 relative">
                <div className="absolute -top-6 -left-4 text-6xl font-black text-slate-100/80 -z-10 select-none">
                  {step.num}
                </div>
                <h3 className="text-xl font-bold text-slate-800 mb-3">{step.title}</h3>
                <p className="text-slate-500 text-sm leading-relaxed">{step.desc}</p>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default SystemExplanation;
