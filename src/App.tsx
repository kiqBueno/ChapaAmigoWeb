import {
  BrowserRouter as Router,
  Route,
  Routes,
  useLocation,
} from "react-router-dom";
import { useEffect } from "react";
import Header from "./components/Header";
import Footer from "./components/Footer";
import Home from "./pages/Home";
import TermosCondicoes from "./pages/TermosCondicoes";

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
          <Route path="/termos-condicoes" element={<TermosCondicoes />} />
        </Routes>
        <Footer />
      </div>
    </Router>
  );
}

export default App;
