import React, { useState } from 'react';
import { Sparkles, TrendingUp, Info, ChevronDown, ChevronUp, Star, Flame, ShieldCheck, AlertTriangle, AlertCircle } from 'lucide-react';

const RecommendationCard = ({ 
  displayItem, item, confidence, lift, support, based_on, explanation, is_trending, 
  isTopRecommendation, product, addToCart
}) => {
  const [showRuleInsight, setShowRuleInsight] = useState(false);

  // Confidence qualitative tier
  let strengthObj = { label: "Strong", color: "text-emerald-700 bg-emerald-50 ring-emerald-200", icon: ShieldCheck };
  if (confidence < 0.4) {
    strengthObj = { label: "Weak", color: "text-red-700 bg-red-50 ring-red-200", icon: AlertCircle };
  } else if (confidence < 0.7) {
    strengthObj = { label: "Moderate", color: "text-amber-700 bg-amber-50 ring-amber-200", icon: AlertTriangle };
  }

  return (
    <div className={`
      bg-white rounded-xl shadow-sm overflow-hidden transition-all duration-300 group flex flex-col h-full
      ${isTopRecommendation ? 'border-2 border-brand-500 shadow-brand-100/50 transform hover:-translate-y-1' : 'border border-slate-200 hover:shadow-md transform hover:-translate-y-1'}
    `}>
      <div className="p-5 flex-grow flex flex-col">
        <div className="flex justify-between items-start mb-4">
          <div className="flex items-center space-x-2 flex-wrap gap-y-2">
            {isTopRecommendation && !is_trending && (
              <div className="flex items-center space-x-1 text-amber-600 bg-amber-50 px-3 py-1 rounded-full text-xs font-bold ring-1 ring-amber-200">
                <Star size={14} className="fill-amber-600" />
                <span>Best Match</span>
              </div>
            )}
            
            {!isTopRecommendation && !is_trending && (
              <div className="flex items-center space-x-1 text-brand-600 bg-brand-50 px-3 py-1 rounded-full text-xs font-semibold">
                <Sparkles size={14} />
                <span>Recommended</span>
              </div>
            )}

            {is_trending && (
              <div className="flex items-center space-x-1 text-rose-600 bg-rose-50 px-3 py-1 rounded-full text-xs font-bold ring-1 ring-rose-200">
                <Flame size={14} className="fill-rose-600" />
                <span>Trending</span>
              </div>
            )}
          </div>
          
          <div className="text-right flex-shrink-0">
            {!is_trending && (
              <>
                <div className="text-xs text-slate-500 font-medium uppercase tracking-wider mb-1">Confidence</div>
                <div className={`flex items-center justify-end space-x-1 text-lg font-bold px-2 py-0.5 rounded-md ring-1 ${strengthObj.color}`}>
                  <strengthObj.icon size={16} />
                  <span>{(confidence * 100).toFixed(0)}%</span>
                </div>
              </>
            )}
          </div>
        </div>
        
        <h3 title={displayItem || item} className={`font-bold mb-2 truncate max-w-full block transition-colors ${isTopRecommendation ? 'text-2xl text-brand-900 group-hover:text-brand-600' : 'text-xl text-slate-800 group-hover:text-brand-600'}`}>
          {displayItem || item}
        </h3>
        
        {explanation && (
          <div className="text-sm text-slate-600 mb-4 bg-slate-50 p-3 rounded-lg border border-slate-100 italic flex-grow">
            "{explanation}"
          </div>
        )}
        
        <div className="mt-auto pt-4 border-t border-slate-100 flex flex-col justify-between">
          <div className="flex justify-between items-center w-full mb-3">
            {!is_trending ? (
              <span className="flex items-center space-x-1 text-xs text-slate-500" title="Lift measures how much more likely items are bought together than expected">
                <TrendingUp size={14} className="text-brand-500" />
                <span className="font-semibold text-slate-700">Lift: {lift.toFixed(2)}x</span>
              </span>
            ) : (
              <span className="text-xs text-slate-500">Popular item across the store</span>
            )}

            <button 
              onClick={() => {
                console.log("Adding product:", product);
                addToCart(product);
              }}
              className="text-brand-600 text-sm flex-shrink-0 font-semibold hover:text-brand-800 hover:underline transition-colors px-4 py-1.5 bg-brand-50 hover:bg-brand-100 rounded-lg">
              Add to Cart
            </button>
          </div>

          {!is_trending && (
             <button 
                onClick={() => setShowRuleInsight(!showRuleInsight)}
                className="flex items-center justify-between text-xs text-slate-400 hover:text-slate-600 transition-colors w-full p-2 bg-slate-50 rounded"
             >
                <div className="flex items-center space-x-1">
                  <Info size={14} />
                  <span>Rule Analytics</span>
                </div>
                {showRuleInsight ? <ChevronUp size={14} /> : <ChevronDown size={14} />}
             </button>
          )}

        </div>
        
        {/* Rule Insight Panel (Expandable) */}
        {!is_trending && showRuleInsight && (
          <div className="mt-3 pt-3 border-t border-slate-100 animate-in slide-in-from-top-2 fade-in duration-200">
            <h4 className="text-xs font-semibold text-slate-700 uppercase tracking-wide mb-2">Association Rule Metrics</h4>
            <div className="grid grid-cols-3 gap-2">
              <div className="bg-slate-50 p-2 rounded border border-slate-200 text-center">
                <div className="text-[10px] text-slate-500 uppercase">Support</div>
                <div className="font-mono text-sm text-slate-800">{(support * 100).toFixed(1)}%</div>
              </div>
              <div className="bg-slate-50 p-2 rounded border border-slate-200 text-center">
                <div className="text-[10px] text-slate-500 uppercase">Confidence</div>
                <div className="font-mono text-sm text-slate-800">{(confidence * 100).toFixed(1)}%</div>
              </div>
              <div className="bg-slate-50 p-2 rounded border border-slate-200 text-center flex-col flex select-none">
                <div className="text-[10px] text-slate-500 uppercase">Lift</div>
                <div className="font-mono text-sm text-slate-800">{lift.toFixed(2)}</div>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default RecommendationCard;
