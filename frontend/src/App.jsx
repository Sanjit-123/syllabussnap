import React, { useState, useEffect, useRef, useMemo } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import {
  Upload, Sparkles, BarChart3, Clock, Target,
  CheckCircle2, ChevronRight, Zap, Trophy,
  AlertCircle, Search, ArrowRight, Activity,
  Cpu, Terminal
} from 'lucide-react';
import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000/api';

const HUDOverlay = () => {
  const coords = useMemo(() => ({
    x: Math.floor(Math.random() * 1000),
    y: Math.floor(Math.random() * 1000)
  }), []);

  return (
    <div style={{ position: 'fixed', top: 0, left: 0, width: '100%', height: '100%', pointerEvents: 'none', zIndex: 10 }}>
      <div style={{ position: 'absolute', top: '40px', left: '40px', fontFamily: 'Space Mono', fontSize: '0.6rem', opacity: 0.3 }}>
        CORE_OS_v1.0.4<br />STATUS: ACTIVE<br />LATENCY: 12ms
      </div>
      <div style={{ position: 'absolute', bottom: '40px', right: '40px', fontFamily: 'Space Mono', fontSize: '0.6rem', opacity: 0.3, textAlign: 'right' }}>
        COORD_X: {coords.x}<br />COORD_Y: {coords.y}<br />SECURITY: ENCRYPTED
      </div>
    </div>
  );
};

const Navbar = ({ onReset }) => (
  <nav style={{ padding: '40px 0', display: 'flex', justifyContent: 'space-between', alignItems: 'center', maxWidth: '1400px', margin: '0 auto', width: '100%', position: 'relative', zIndex: 20 }}>
    <motion.div whileHover={{ x: 5 }} onClick={onReset} style={{ display: 'flex', alignItems: 'center', gap: '16px', cursor: 'pointer' }}>
      <div style={{ background: '#000', width: '32px', height: '32px', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
        <Activity size={20} color="white" />
      </div>
      <span className="nothing-font" style={{ fontWeight: '400', fontSize: '1.8rem', letterSpacing: '2px' }}>SYLLABUS_SNAP</span>
    </motion.div>
    <div style={{ display: 'flex', gap: '32px', alignItems: 'center' }}>
      <div style={{ display: 'flex', gap: '8px', alignItems: 'center', fontSize: '0.7rem', opacity: 0.5, fontFamily: 'Space Mono' }}>
        <div style={{ width: '6px', height: '6px', background: '#00ff00', borderRadius: '50%' }} />
        SERVER_CONNECTED
      </div>
      <button className="btn-secondary" style={{ border: 'none', fontSize: '0.8rem' }}>MANIFESTO</button>
      <button className="btn-premium" style={{ padding: '8px 24px', fontSize: '0.8rem' }}>ACCESS_PORTAL</button>
    </div>
  </nav>
);

const Hero = ({ onGetStarted }) => (
  <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0, x: -100 }} transition={{ duration: 0.8 }} style={{ textAlign: 'left', padding: '120px 0', maxWidth: '1400px', margin: '0 auto' }}>
    <motion.div initial={{ opacity: 0, x: -20 }} animate={{ opacity: 1, x: 0 }} transition={{ delay: 0.2 }} className="badge" style={{ marginBottom: '40px' }}>
      NEURAL_ENGINE_ONLINE
    </motion.div>
    <h1 style={{ fontSize: 'clamp(4rem, 15vw, 10rem)', marginBottom: '40px', lineHeight: '0.85', fontWeight: 900, letterSpacing: '-0.05em' }}>
      MASTER THE <br /><span style={{ color: 'var(--accent-red)' }}>COMPLEX.</span>
    </h1>
    <div style={{ display: 'flex', gap: '80px', flexWrap: 'wrap', marginTop: '60px' }}>
      <div style={{ maxWidth: '500px' }}>
        <p style={{ color: 'var(--text-muted)', fontSize: '1.25rem', marginBottom: '48px', lineHeight: '1.4', fontFamily: 'Space Mono', textTransform: 'uppercase' }}>
          WE REDUCE ACADEMIC FRICTION. OUR HEURISTIC ALGORITHMS PARSE RAW SYLLABI TO IDENTIFY HIGH-YIELD TARGETS FOR MAXIMUM STUDY EFFICIENCY.
        </p>
        <div style={{ display: 'flex', gap: '24px' }}>
          <motion.button whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.95 }} className="btn-premium" onClick={onGetStarted}>
            INITIALIZE_SCAN <ArrowRight size={20} />
          </motion.button>
          <button className="btn-secondary">LEARN_MORE</button>
        </div>
      </div>
      <div style={{ flex: 1, display: 'flex', justifyContent: 'flex-end', alignItems: 'flex-end' }}>
        <div style={{ textAlign: 'right', borderRight: '4px solid #000', paddingRight: '24px' }}>
          <div className="nothing-font" style={{ fontSize: '6rem', lineHeight: '1' }}>88:00</div>
          <div style={{ fontSize: '0.9rem', opacity: 0.6, fontFamily: 'Space Mono', letterSpacing: '2px' }}>ESTIMATED_SAVINGS</div>
        </div>
      </div>
    </div>
  </motion.div>
);

const LoadingHUD = () => (
  <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} style={{ position: 'absolute', top: 0, left: 0, width: '100%', height: '100%', background: 'rgba(255,255,255,0.95)', zIndex: 5, display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center' }}>
    <div style={{ position: 'relative', width: '200px', height: '200px' }}>
      <motion.div animate={{ rotate: 360 }} transition={{ duration: 4, repeat: Infinity, ease: "linear" }} style={{ position: 'absolute', top: 0, left: 0, width: '100%', height: '100%', border: '1px dashed #000', borderRadius: '50%' }} />
      <motion.div animate={{ rotate: -360 }} transition={{ duration: 8, repeat: Infinity, ease: "linear" }} style={{ position: 'absolute', top: '20px', left: '20px', width: '160px', height: '160px', border: '1px solid #000', borderRadius: '50%', opacity: 0.1 }} />
      <div style={{ position: 'absolute', top: '50%', left: '50%', transform: 'translate(-50%, -50%)' }}>
        <Cpu size={40} />
      </div>
    </div>
    <div style={{ marginTop: '40px', fontFamily: 'Space Mono', textAlign: 'center' }}>
      <div style={{ fontSize: '1.2rem', fontWeight: 700, marginBottom: '8px' }}>ANALYZING_SYLLABUS_DNA...</div>
      <div style={{ fontSize: '0.8rem', opacity: 0.5 }}>EXTRACTING_KEY_ENTITIES // RANKING_BY_WEIGHT</div>
    </div>
  </motion.div>
);

const UploadZone = ({ onUpload, loading }) => (
  <motion.div initial={{ opacity: 0, scale: 0.9 }} animate={{ opacity: 1, scale: 1 }} exit={{ opacity: 0, scale: 1.1 }} className="glass-card" style={{ padding: '120px 0', textAlign: 'center', maxWidth: '1200px', margin: '60px auto', border: '1px dashed var(--glass-border)', position: 'relative' }}>
    <AnimatePresence>{loading && <LoadingHUD />}</AnimatePresence>
    <div style={{ marginBottom: '40px' }}>
      <motion.div animate={loading ? { scale: [1, 1.1, 1], opacity: [1, 0.5, 1] } : {}} transition={{ duration: 1.5, repeat: Infinity }}>
        <Upload size={80} strokeWidth={0.5} />
      </motion.div>
    </div>
    <h2 style={{ fontSize: '4rem', marginBottom: '16px', letterSpacing: '-3px' }}>SOURCE_UPLOAD</h2>
    <p style={{ color: 'var(--text-muted)', marginBottom: '48px', fontFamily: 'Space Mono', fontSize: '1rem', letterSpacing: '2px' }}>ATTACH_MANIFEST [.PDF / .TXT]</p>
    <input type="file" id="file-upload" accept=".pdf,.txt" style={{ display: 'none' }} onChange={(e) => onUpload(e.target.files[0])} disabled={loading} />
    {!loading && (
      <label htmlFor="file-upload">
        <motion.button whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.95 }} className="btn-premium" style={{ cursor: 'pointer', padding: '16px 48px' }}>BROWSE_FILES</motion.button>
      </label>
    )}
    <div style={{ marginTop: '60px', display: 'flex', justifyContent: 'center', gap: '40px', opacity: 0.3, fontFamily: 'Space Mono', fontSize: '0.7rem' }}>
      <div>[01] UPLOAD</div><div>[02] PARSE</div><div>[03] RANK</div><div>[04] OPTIMIZE</div>
    </div>
  </motion.div>
);

const Dashboard = ({ data, analysisId, onStatusChange }) => {
  const [examMode, setExamMode] = useState(false);
  const [searchQuery, setSearchQuery] = useState('');

  const filteredTopics = data.topics.filter(t => {
    const matchesSearch = t.title.toLowerCase().includes(searchQuery.toLowerCase());
    const matchesExamMode = !examMode || t.priority > 6;
    return matchesSearch && matchesExamMode;
  });

  return (
    <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} style={{ padding: '80px 0 100px' }}>
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', gap: '2px', background: 'var(--glass-border)', border: '2px solid #000', marginBottom: '80px' }}>
        {[
          { label: 'CRITICAL_TARGETS', value: data.topics.filter(t => t.priority > 6).length, color: 'var(--accent-red)' },
          { label: 'EST_TIME_REQ', value: data.summary.estimated_study_time, color: 'var(--text-main)' },
          { label: 'HEURISTIC_CONF', value: '82%', color: 'var(--text-main)' }
        ].map((stat, i) => (
          <motion.div key={stat.label} initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: i * 0.1 }} style={{ background: '#fff', padding: '60px 40px' }}>
            <div style={{ fontSize: '0.8rem', color: 'var(--text-muted)', marginBottom: '24px', fontFamily: 'Space Mono', fontWeight: 700 }}>{stat.label}</div>
            <div className="nothing-font" style={{ fontSize: '4rem', color: stat.color, lineHeight: '1' }}>{stat.value}</div>
          </motion.div>
        ))}
      </div>

      <div style={{ marginBottom: '60px', display: 'flex', justifyContent: 'space-between', alignItems: 'center', borderBottom: '2px solid #000', paddingBottom: '30px', flexWrap: 'wrap', gap: '20px' }}>
        <div>
          <h2 style={{ fontSize: '3rem', letterSpacing: '-2px' }}>RANKING_MATRIX</h2>
          <div style={{ fontFamily: 'Space Mono', fontSize: '0.8rem', opacity: 0.5 }}>TOTAL_ENTITIES: {data.topics.length}</div>
        </div>
        <div style={{ display: 'flex', gap: '32px', alignItems: 'center' }}>
          <div style={{ position: 'relative', borderBottom: '1px solid #000' }}>
            <Search size={18} style={{ position: 'absolute', left: '0', top: '50%', transform: 'translateY(-50%)', opacity: 0.4 }} />
            <input type="text" placeholder="SEARCH_MANIFEST..." value={searchQuery} onChange={(e) => setSearchQuery(e.target.value)} style={{ background: 'transparent', border: 'none', padding: '16px 16px 16px 32px', color: 'black', fontFamily: 'Space Mono', fontSize: '1rem', outline: 'none', width: '300px' }} />
          </div>
          <motion.button whileHover={{ scale: 1.02 }} whileTap={{ scale: 0.98 }} onClick={() => setExamMode(!examMode)} className="btn-secondary" style={{ borderRadius: '0', padding: '16px 32px', background: examMode ? 'var(--accent-red)' : 'transparent', borderColor: '#000', color: examMode ? 'white' : 'black' }}>
            {examMode ? 'EXAM_MODE: ON' : 'EXAM_MODE: OFF'}
          </motion.button>
        </div>
      </div>

      <div style={{ display: 'flex', flexDirection: 'column' }}>
        <AnimatePresence mode="popLayout">
          {filteredTopics.map((topic, idx) => (
            <motion.div key={topic.id} layout initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0, scale: 0.95 }} transition={{ delay: idx * 0.04 }} className="topic-row" style={{ cursor: 'pointer' }} whileHover={{ x: 10, background: 'rgba(0,0,0,0.01)' }}>
              <div className="nothing-font" style={{ fontSize: '3rem', width: '100px', color: topic.priority > 6 ? 'var(--accent-red)' : 'var(--text-main)' }}>
                {topic.id.toString().padStart(2, '0')}
              </div>
              <div style={{ flex: 1 }}>
                <h4 style={{ fontSize: '1.6rem', marginBottom: '8px', color: 'var(--text-main)', letterSpacing: '-1px' }}>{topic.title}</h4>
                <div style={{ display: 'flex', gap: '40px', fontSize: '0.85rem', color: 'var(--text-muted)', fontFamily: 'Space Mono', fontWeight: 600 }}>
                  <span>[UNIT_{topic.unit}]</span>
                  <span>[FREQ_{topic.frequency}]</span>
                  <span>[PRI_{topic.priority}]</span>
                </div>
              </div>
              <motion.button whileHover={{ scale: 1.1 }} whileTap={{ scale: 0.9 }} onClick={(e) => { e.stopPropagation(); onStatusChange(topic.id); }} style={{ background: topic.status === 'completed' ? '#000' : 'transparent', border: '2px solid #000', color: topic.status === 'completed' ? '#fff' : '#000', padding: '12px 32px', fontFamily: 'Space Mono', fontSize: '0.8rem', fontWeight: 700, cursor: 'pointer' }}>
                {topic.status === 'completed' ? 'DONE' : 'MARK'}
              </motion.button>
            </motion.div>
          ))}
        </AnimatePresence>
      </div>

      {data.topics.length > 0 && (
        <motion.div initial={{ opacity: 0, y: 40 }} whileInView={{ opacity: 1, y: 0 }} viewport={{ once: true }} style={{ marginTop: '100px', padding: '60px', background: '#000', color: '#fff', border: '1px solid #000', position: 'relative' }}>
          <div style={{ position: 'absolute', top: '20px', right: '20px' }}><Terminal size={24} opacity={0.3} /></div>
          <div className="badge" style={{ borderColor: '#fff', color: '#fff', marginBottom: '32px' }}>SYSTEM_RECOMMENDATION</div>
          <h3 style={{ fontSize: '2.5rem', marginBottom: '24px' }}>FOCUS_DIRECTIVE_01</h3>
          <p style={{ color: 'rgba(255,255,255,0.6)', lineHeight: '1.6', fontSize: '1.1rem', fontFamily: 'Space Mono', maxWidth: '800px' }}>
            PRIMARY ANALYSIS SUGGESTS <span style={{ color: '#fff', fontWeight: 700 }}>{data.topics[0].title}</span> AS THE CRITICAL PATH.
            SYLLABUS TOPOLOGY INDICATES UNIT {data.topics[0].unit} HAS A HIGH FREQUENCY OVERLAP WITH CORE LEARNING OBJECTIVES.
          </p>
        </motion.div>
      )}
    </motion.div>
  );
};

export default function App() {
  const [view, setView] = useState('hero');
  const [loading, setLoading] = useState(false);
  const [data, setData] = useState(null);
  const [analysisId, setAnalysisId] = useState(null);
  const containerRef = useRef(null);

  useEffect(() => {
    const handleMouseMove = (e) => {
      if (containerRef.current) {
        containerRef.current.style.setProperty('--mouse-x', `${(e.clientX / window.innerWidth) * 100}%`);
        containerRef.current.style.setProperty('--mouse-y', `${(e.clientY / window.innerHeight) * 100}%`);
      }
    };
    window.addEventListener('mousemove', handleMouseMove);
    return () => window.removeEventListener('mousemove', handleMouseMove);
  }, []);

  const handleUpload = async (file) => {
    if (!file) return;
    setLoading(true);
    const formData = new FormData();
    formData.append('file', file);
    try {
      const res = await axios.post(`${API_BASE_URL}/analyze`, formData);
      setData(res.data);
      setAnalysisId(res.data.analysis_id || null);
      setView('dashboard');
      window.scrollTo({ top: 0, behavior: 'smooth' });
    } catch (err) {
      const msg = err.response?.data?.error || 'Backend unreachable. Is the server running?';
      alert(`ERROR: ${msg}`);
    } finally {
      setLoading(false);
    }
  };

  const toggleStatus = async (id) => {
    const topic = data.topics.find(t => t.id === id);
    if (!topic) return;
    const newStatus = topic.status === 'completed' ? 'pending' : 'completed';

    setData(prev => ({
      ...prev,
      topics: prev.topics.map(t => t.id === id ? { ...t, status: newStatus } : t)
    }));

    if (analysisId) {
      try {
        await axios.patch(`${API_BASE_URL}/analysis/${analysisId}/topic/${id}`, { status: newStatus });
      } catch (err) {
        console.warn('Could not persist status to DB:', err.message);
      }
    }
  };

  return (
    <div ref={containerRef} className="app-container" style={{ minHeight: '100vh', padding: '0 60px', display: 'flex', flexDirection: 'column' }}>
      <div className="cinematic-bg" />
      <HUDOverlay />
      <Navbar onReset={() => { setView('hero'); setData(null); setAnalysisId(null); }} />
      <main style={{ width: '100%', position: 'relative', zIndex: 1 }}>
        <AnimatePresence mode="wait">
          {view === 'hero' && <Hero key="hero" onGetStarted={() => setView('upload')} />}
          {view === 'upload' && <UploadZone key="upload" onUpload={handleUpload} loading={loading} />}
          {view === 'dashboard' && data && <Dashboard key="dashboard" data={data} analysisId={analysisId} onStatusChange={toggleStatus} />}
        </AnimatePresence>
      </main>
      <footer style={{ marginTop: 'auto', padding: '100px 0 60px', opacity: 0.2, fontSize: '0.8rem', fontFamily: 'Space Mono', letterSpacing: '4px', display: 'flex', justifyContent: 'space-between' }}>
        <div>SYLLABUS_SNAP // N_OS_PREMIUM_EDITION</div>
        <div>[ACCESS_CODE_4482]</div>
      </footer>
    </div>
  );
}
