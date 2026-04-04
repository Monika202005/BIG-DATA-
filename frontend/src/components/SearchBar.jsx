import React, { useState, useEffect } from 'react';
import { Search, Plus, ShoppingCart, X } from 'lucide-react';

const SearchBar = ({ products, onUpdateCart, cartExternal = [], isSimulating = false }) => {
  const [query, setQuery] = useState('');
  const [filteredProducts, setFilteredProducts] = useState([]);

  // Sync external changes (like Simulator mode) with local cart state.

  useEffect(() => {
    if (query.trim() === '') {
      setFilteredProducts([]);
      return;
    }
    const lowerQuery = query.toLowerCase();
    const results = products.filter(p => p.name.toLowerCase().includes(lowerQuery));
    setFilteredProducts(results);
  }, [query, products]);

  const removeFromCart = (productId) => {
    const newCart = cartExternal.filter(p => p.id !== productId);
    onUpdateCart(newCart);
  };

  return (
    <div className={`w-full max-w-4xl mx-auto space-y-8 animate-in slide-in-from-bottom-5 fade-in duration-700 ${isSimulating ? 'pointer-events-none opacity-80' : ''}`}>

      {/* Premium Search Input Container */}
      <div className="relative z-30">
        <div className="relative flex items-center bg-white/90 backdrop-blur-sm rounded-2xl shadow-xl shadow-slate-200/50 border border-slate-200/80 focus-within:border-brand-500 focus-within:ring-[6px] focus-within:ring-brand-500/20 transition-all duration-300 p-3 h-16">
          <Search className="text-brand-500 ml-4 mr-3" size={24} />
          <input
            type="text"
            className="w-full p-2 outline-none text-slate-800 bg-transparent text-xl font-medium placeholder:text-slate-400"
            placeholder={isSimulating ? "AI Simulator mapping combinations auto-magically..." : "Type 'Laptop', 'Monitor'..."}
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            disabled={isSimulating}
          />
        </div>

        {/* Floating Autocomplete Dropdown */}
        {filteredProducts.length > 0 && (
          <div className="absolute top-[110%] left-0 right-0 bg-white rounded-2xl shadow-2xl border border-slate-200/80 overflow-hidden z-30 max-h-72 overflow-y-auto animate-in slide-in-from-top-2 fade-in duration-200">
            {filteredProducts.map((p, idx) => (
              <div
                key={idx}
                className="px-6 py-4 hover:bg-slate-50 border-b last:border-0 border-slate-100 cursor-pointer flex justify-between items-center group transition-colors"
                onClick={() => onUpdateCart([...cartExternal, p])}
              >
                <div>
                  <div className="font-bold text-lg text-slate-800 group-hover:text-brand-600 transition-colors">{p.name}</div>
                  <div className="text-sm font-medium text-slate-400">{p.category}</div>
                </div>
                <button className="text-white bg-brand-500 p-2 rounded-xl opacity-0 group-hover:opacity-100 transition-all duration-300 transform group-hover:scale-110 shadow-lg shadow-brand-500/30">
                  <Plus size={20} />
                </button>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Docked Cart Display */}
      <div className="bg-white/60 backdrop-blur border border-slate-200/60 rounded-3xl p-6 sm:p-8 shadow-sm relative overflow-hidden">

        {/* Subtle background decoration */}
        <div className="absolute -top-24 -right-24 bg-brand-50 w-64 h-64 rounded-full mix-blend-multiply blur-3xl opacity-50"></div>
        <div className="absolute -bottom-24 -left-24 bg-indigo-50 w-64 h-64 rounded-full mix-blend-multiply blur-3xl opacity-50"></div>

        <div className="relative z-10">
          <h3 className="font-bold text-slate-800 mb-4 flex items-center text-sm uppercase tracking-wider">
            <ShoppingCart size={18} className="mr-2 text-brand-500" /> Active Basket
            {cartExternal.length > 0 && (
              <span className="ml-3 bg-brand-100 text-brand-700 py-0.5 px-2.5 rounded-full text-xs font-black transition-all">
                {cartExternal.length}
              </span>
            )}
          </h3>

          {cartExternal.length === 0 ? (
            <div className="text-slate-500 text-lg py-8 text-center bg-slate-50/50 rounded-2xl border border-dashed border-slate-300 transition-all duration-300">
              Basket is empty. Waiting for input...
            </div>
          ) : (
            <div className="flex flex-wrap gap-3">
              {cartExternal.map((item, idx) => (
                <div key={item.id || idx} className="animate-in zoom-in-50 fade-in duration-300 bg-white border-2 border-slate-200 px-5 py-2.5 rounded-2xl flex items-center shadow-sm text-base font-bold text-slate-800 group hover:border-brand-300 transition-colors">
                  <span className="truncate max-w-[200px] sm:max-w-xs block" title={item.name}>{item.name}</span>
                  <button
                    onClick={() => removeFromCart(item.id)}
                    className="ml-3 flex-shrink-0 bg-slate-100 text-slate-500 hover:bg-rose-100 hover:text-rose-600 focus:outline-none transition-all duration-200 p-1 rounded-lg"
                  >
                    <X size={16} strokeWidth={3} />
                  </button>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>

    </div>
  );
};

export default SearchBar;
