import {
  BrowserRouter as Router,
  Route,
  Routes,
  useLocation,
} from "react-router-dom";
import { useEffect } from "react";
import Header from "./components/Header";
import Footer from "./components/Footer";
import Home from "./pages/HomePage";
import TermosCondicoes from "./pages/TermsConditionsPage";
import Contato from "./pages/ContactPage";

const ScrollToTop = () => {
  const { pathname } = useLocation();

  useEffect(() => {
    window.scrollTo(0, 0);
  }, [pathname]);

  return null;
};

declare global {
  interface Window {
    Tawk_API: {
      [key: string]: unknown;
    };
  }
}

function App() {
  useEffect(() => {
    const Tawk_API = window.Tawk_API || {};
    window.Tawk_API = Tawk_API;
    (function () {
      const s1 = document.createElement("script");
      const s0 = document.getElementsByTagName("script")[0];
      s1.async = true;
      s1.src = "https://embed.tawk.to/YOUR_PROPERTY_ID/default";
      s1.charset = "UTF-8";
      s1.setAttribute("crossorigin", "*");
      if (s0.parentNode) {
        s0.parentNode.insertBefore(s1, s0);
      }
    })();
  }, []);

  return (
    <Router>
      <ScrollToTop />
      <div className="appContainer">
        <Header />
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/contato" element={<Contato />} />
          <Route path="/termos-condicoes" element={<TermosCondicoes />} />
        </Routes>
        <Footer />
      </div>
    </Router>
  );
}

export default App;
