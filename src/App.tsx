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
import AccessPage from "./pages/AccessPage";

const ScrollToTop = () => {
  const { pathname } = useLocation();

  useEffect(() => {
    window.scrollTo(0, 0);
  }, [pathname]);

  return null;
};

function App() {
  return (
    <Router>
      <ScrollToTop />
      <div className="appContainer">
        <Header />
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/contato" element={<Contato />} />
          <Route path="/termos-condicoes" element={<TermosCondicoes />} />
          <Route path="/accccessss" element={<AccessPage />} />
        </Routes>
        <Footer />
      </div>
    </Router>
  );
}

export default App;
