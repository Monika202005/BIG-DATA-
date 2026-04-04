import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import { PackageOpen, Sparkles, AlertCircle, BarChart3, TrendingUp, Layers, Play, Square, Settings2, Loader2, CheckCircle2 } from 'lucide-react';
import SearchBar from './components/SearchBar';
import RecommendationCard from './components/RecommendationCard';
import BusinessInsights from './components/BusinessInsights';
import SkeletonLoader from './components/SkeletonLoader';
import SystemExplanation from './components/SystemExplanation';

function App() {
  const [products, setProducts] = useState([]);
  const [cart, setCart] = useState([]);
  const [recommendations, setRecommendations] = useState([]);
  const [isFallback, setIsFallback] = useState(false);
  const [loadingRecs, setLoadingRecs] = useState(true);
  const [error, setError] = useState(null);
  const [activity, setActivity] = useState([]);

  async function getActivity() {
    const res = await fetch("http://127.0.0.1:8000/activity");
    const data = await res.json();
    console.log(data);
    setActivity(data);
  }

  // Interactive Demo state
  const [isSimulating, setIsSimulating] = useState(false);

  // Model Configuration State
  const [minSupport, setMinSupport] = useState(0.05);
  const [minConfidence, setMinConfidence] = useState(0.10);
  const [isRecalculating, setIsRecalculating] = useState(false);
  const [recalcSuccess, setRecalcSuccess] = useState(false);

  const fetchedProductsCount = useRef(0);

  useEffect(() => {
    // Fetch available products on load
    const fetchProducts = async () => {
      try {
        const response = await axios.get('http://localhost:8000/products');
        setProducts(response.data);
        fetchedProductsCount.current = response.data.length;
        // Run initial empty cart request only AFTER products are loaded to map fallback names
        handleUpdateCart([], response.data);
      } catch (err) {
        console.error("Error fetching products:", err);
      }
    };
    fetchProducts();
    getActivity();
  }, []);

  // Simulate User Profile
  useEffect(() => {
    let simulator;
    if (isSimulating && products.length > 0) {
      simulator = setInterval(() => {
        // Pick 1 to 2 random products
        const limit = Math.floor(Math.random() * 2) + 1;
        const shuffled = [...products].sort(() => 0.5 - Math.random());
        // Add full product objects to cart
        const randomPicks = shuffled.slice(0, limit);
        handleUpdateCart(randomPicks, products);
      }, 4500); // refresh every 4.5s
    } else if (!isSimulating && simulator) {
      clearInterval(simulator);
    }
    return () => clearInterval(simulator);
  }, [isSimulating, products]);

  const handleUpdateCart = async (newCart, currentProducts = products) => {
    setCart(newCart);
    setLoadingRecs(true);
    setError(null);

    // Send only normalized names to backend
    const normalizedCart = newCart.map(p => p.normalized);
    console.log("DEBUG [Frontend]: Selected cart products:", newCart);
    console.log("DEBUG [Frontend]: Sending API payload /recommend ->", { products: normalizedCart });

    try {
      const response = await axios.post('http://localhost:8000/recommend', {
        products: normalizedCart
      });

      const recs = response.data.recommendations || [];

      // Hydrate recommendations with Display Names from the Products dictionary
      const hydratedRecs = recs.map(rec => {
        const match = currentProducts.find(p => p.normalized === rec.item);
        return {
          ...rec,
          originalProductObject: match || null,
          displayItem: match ? match.name : rec.item,
        };
      });

      setRecommendations(hydratedRecs);
      setIsFallback(response.data.is_fallback || false);
    } catch (err) {
      console.error("Error fetching recommendations:", err);
      setError("Failed to fetch intelligent recommendations. Please ensure the backend is running.");
      setRecommendations([]);
    } finally {
      setTimeout(() => setLoadingRecs(false), 400);
    }
  };

  const handeRecalculate = async () => {
    setIsRecalculating(true);
    setRecalcSuccess(false);
    console.log(`DEBUG [Frontend]: Recalculating graph with support=${minSupport}, confidence=${minConfidence}`);
    try {
      await axios.post('http://localhost:8000/recalculate', {
        min_support: parseFloat(minSupport),
        min_confidence: parseFloat(minConfidence)
      });
      setRecalcSuccess(true);
      // Re-trigger recommendations to show changes
      handleUpdateCart(cart, products);
      setTimeout(() => setRecalcSuccess(false), 3000);
    } catch (err) {
      console.error("Error recalculating API", err);
      setError("Error recalculating the machine learning model.");
    } finally {
      setIsRecalculating(false);
    }
  };

  // Custom helper for nested add-to-cart clicks
  const handleAddToCartDirectly = (productObj) => {
    if (!productObj) return;
    if (!cart.find(c => c.id === productObj.id)) {
      handleUpdateCart([...cart, productObj], products);
    }
  };

  return (
    <div className="min-h-screen font-sans bg-[#F8F9FB] selection:bg-brand-100 selection:text-brand-900 pb-12 text-slate-800">
      <h3>User Activity</h3>
      <div style={{ display: "flex", gap: "10px", flexWrap: "wrap" }}>
        {activity.map((item, index) => (
          <div key={index} style={{
            border: "1px solid #ccc",
            padding: "10px",
            borderRadius: "8px",
            background: "#f9f9f9"
          }}>
            <p><b>User:</b> {item.user_id}</p>
            <p><b>Product:</b> {item.product}</p>
            <p><b>Action:</b> {item.action}</p>
          </div>
        ))}
      </div>

      {/* Simulation Banner */}
      {isSimulating && (
        <div className="bg-brand-600 text-white py-1.5 px-4 text-center text-sm font-semibold animate-in slide-in-from-top-12 z-50 relative">
          Interactive Demo Mode Active: Injecting random basket permutations automatically...
        </div>
      )}

      {/* Premium Header */}
      <header className="bg-white/80 backdrop-blur-md border-b border-slate-200/60 sticky top-0 z-40 transition-all">
        <div className="max-w-7xl mx-auto px-4 py-4 sm:px-6 lg:px-8 flex items-center justify-between">
          <div className="flex items-center space-x-3 group cursor-pointer">
            <div className="bg-gradient-to-br from-brand-600 to-indigo-700 p-2.5 rounded-xl group-hover:shadow-lg group-hover:shadow-brand-500/20 transition-all duration-300 transform group-hover:-translate-y-0.5">
              <Layers className="text-white" size={24} strokeWidth={2.5} />
            </div>
            <h1 className="text-2xl font-black tracking-tight">
              Nexus<span className="text-brand-600">AI</span>
            </h1>
          </div>

          <div className="flex items-center space-x-4">
            {/* Simulator Toggle */}
            <button
              onClick={() => setIsSimulating(!isSimulating)}
              className={`flex items-center space-x-2 text-sm font-bold border px-4 py-2 rounded-full transition-all duration-300 ${isSimulating ? 'bg-rose-50 border-rose-200 text-rose-700 shadow-sm' : 'bg-slate-100 border-slate-200 text-slate-600 hover:bg-slate-200'}`}
            >
              {isSimulating ? <Square fill="currentColor" size={14} className="animate-pulse" /> : <Play fill="currentColor" size={14} />}
              <span>{isSimulating ? 'Stop Simulator' : 'Simulate User'}</span>
            </button>

            <div className="hidden sm:flex items-center space-x-2 text-sm font-semibold text-slate-500 bg-slate-100 px-3 py-1.5 rounded-full border border-slate-200">
              <BarChart3 size={16} className="text-brand-500" />
              <span>Apriori Engine <span className="text-brand-600 ml-1">v3.0</span></span>
            </div>
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pt-12 space-y-16">

        {/* ML Configuration Panel */}
        <section className="bg-white border rounded-2xl shadow-sm border-slate-200/60 p-6 flex flex-col md:flex-row items-center justify-between z-10 animate-in fade-in zoom-in-95 duration-700 gap-6">
          <div className="flex items-center space-x-3 w-full md:w-auto">
            <div className="bg-indigo-50 p-2 rounded-xl text-indigo-600 hidden sm:block">
              <Settings2 size={24} />
            </div>
            <div>
              <h3 className="font-bold text-slate-800 text-lg">Model Parameters</h3>
              <p className="text-xs text-slate-500">Recalculate SQLite Association Graph natively</p>
            </div>
          </div>

          <div className="flex flex-col sm:flex-row items-center gap-6 w-full md:w-auto">
            <div className="w-full sm:w-48 text-sm">
              <div className="flex justify-between font-semibold mb-2">
                <label className="text-slate-600">Min Support</label>
                <span className="text-brand-600 bg-brand-50 px-2 rounded">{(minSupport * 100).toFixed(0)}%</span>
              </div>
              <input type="range" min="0.01" max="0.30" step="0.01" value={minSupport} onChange={e => setMinSupport(e.target.value)} className="w-full accent-brand-600" />
            </div>

            <div className="w-full sm:w-48 text-sm">
              <div className="flex justify-between font-semibold mb-2">
                <label className="text-slate-600">Min Confidence</label>
                <span className="text-brand-600 bg-brand-50 px-2 rounded">{(minConfidence * 100).toFixed(0)}%</span>
              </div>
              <input type="range" min="0.05" max="0.80" step="0.05" value={minConfidence} onChange={e => setMinConfidence(e.target.value)} className="w-full accent-brand-600" />
            </div>

            <button
              onClick={handeRecalculate}
              disabled={isRecalculating}
              className="w-full sm:w-auto bg-slate-800 hover:bg-slate-900 text-white font-semibold py-2.5 px-6 rounded-xl shadow-lg shadow-slate-800/20 transition-all flex items-center justify-center space-x-2 whitespace-nowrap disabled:opacity-75 disabled:cursor-wait"
            >
              {isRecalculating ? (
                <><Loader2 size={18} className="animate-spin" /><span>Recalculating...</span></>
              ) : recalcSuccess ? (
                <><CheckCircle2 size={18} className="text-emerald-400" /><span>Graph Updated</span></>
              ) : (
                <span>Apply Constraints</span>
              )}
            </button>
          </div>
        </section>

        {/* Search Hero Section */}
        <section className="text-center space-y-8 max-w-4xl mx-auto pt-4 relative">
          <h2 className="text-5xl border-b-0 sm:text-6xl font-extrabold text-slate-900 tracking-tight leading-[1.15]">
            Smarter Suggestions, <br />
            <span className="bg-clip-text text-transparent bg-gradient-to-r from-brand-600 to-indigo-600">
              Explainable Results.
            </span>
          </h2>
          <p className="text-lg text-slate-500 max-w-2xl mx-auto leading-relaxed">
            Build your basket. Our model combines Association Rules algorithmically to predict your exact needs with human-readable reasoning.
          </p>

          <div className="pt-8 relative z-30 pointer-events-auto">
            <SearchBar products={products} onUpdateCart={(newCart) => handleUpdateCart(newCart, products)} cartExternal={cart} isSimulating={isSimulating} />
          </div>
        </section>

        {/* Dynamic Recommendations Engine */}
        <section className="bg-white rounded-[2rem] shadow-xl shadow-slate-200/40 border border-slate-200/60 p-8 sm:p-12 relative z-10 transition-all duration-500">

          {/* Header Title Switch */}
          <div className="flex items-center space-x-3 mb-10 relative z-10 border-b border-slate-100 pb-6">
            <div className={`p-3 rounded-2xl ${isFallback ? 'bg-amber-100 text-amber-600' : 'bg-brand-100 text-brand-600'}`}>
              {isFallback ? <TrendingUp size={28} /> : <Sparkles size={28} />}
            </div>
            <div>
              <h2 className="text-3xl font-black text-slate-800 tracking-tight">
                {isFallback ? "Global Trending Products" : "AI Recommended For You"}
              </h2>
              <p className="text-slate-500 font-medium">
                {isFallback ? "Global fallback behavior invoked due to empty basket graph." : "Based on deep Association Rules derived via Apriori probability mappings."}
              </p>
            </div>
          </div>

          {error && (
            <div className="animate-in fade-in slide-in-from-top-4 bg-red-50 border-l-4 border-red-500 p-5 rounded-r-xl flex space-x-4 text-red-800 items-start mb-8 shadow-sm">
              <AlertCircle size={24} className="mt-0.5 text-red-500" />
              <div>
                <h3 className="font-bold text-lg mb-1">Connection Error</h3>
                <p className="text-red-700/80">{error}</p>
              </div>
            </div>
          )}

          {loadingRecs ? (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8 relative z-10">
              {[1, 2, 3].map((n) => (
                <SkeletonLoader key={n} />
              ))}
            </div>
          ) : recommendations.length === 0 ? (
            <div className="flex flex-col items-center justify-center py-20 text-slate-500 space-y-4 animate-in fade-in duration-500">
              <div className="bg-slate-50 p-6 rounded-full border border-slate-100 mb-4">
                <PackageOpen size={64} className="opacity-20 text-slate-400" />
              </div>
              <p className="font-bold text-2xl text-slate-700">No strict associations found</p>
              <p className="text-lg">Try lowering the Minimum Confidence constraints.</p>
            </div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8 relative">
              {recommendations.map((rec, idx) => (
                <div
                  key={idx}
                  style={{ animationDelay: `${idx * 100}ms` }}
                  className="animate-fade-in"
                >
                  <RecommendationCard
                    displayItem={rec.displayItem}
                    item={rec.item}
                    confidence={rec.confidence}
                    lift={rec.lift}
                    support={rec.support}
                    explanation={rec.explanation}
                    is_trending={rec.is_trending}
                    isTopRecommendation={rec.isTopRecommendation}
                    product={{ name: rec.displayItem || rec.item }}
                    addToCart={(product) => {
                      console.log("Adding from recommendation:", product);
                      setCart((prevCart) => [...prevCart, product]);
                    }}
                  />
                </div>
              ))}
            </div>
          )}
        </section>

        {/* Premium Data Science Analytics Section */}
        <section className="pt-4 animate-in fade-in relative z-0">
          <BusinessInsights />
        </section>

      </main>

      {/* System Architect Overview */}
      <SystemExplanation />

    </div>

  );
}

export default App;
