import { BrowserRouter as Router, useLocation } from "react-router-dom";
import { useEffect } from "react";
import Header from "../src/components/Header";
import Footer from "../src/components/Footer";
import AppRoutes from "../src/routes";

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
        <AppRoutes />
        <Footer />
      </div>
    </Router>
  );
}

export default App;
