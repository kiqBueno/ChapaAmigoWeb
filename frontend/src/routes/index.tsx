import { Suspense, lazy } from "react";
import { Routes, Route } from "react-router-dom";

const Home = lazy(() => import("../pages/HomePage"));
const TermosCondicoes = lazy(() => import("../pages/TermsConditionsPage"));
const Contato = lazy(() => import("../pages/ContactPage"));
const AccessPage = lazy(() => import("../pages/AccessPage"));
const PlansPage = lazy(() => import("../pages/PlansPage"));
const PdfUploadPage = lazy(() => import("../pages/AccessPage/PdfUploadPage"));
const ImportantInfoPage = lazy(() => import("../pages/ImportantInfoPage"));

const AppRoutes = () => {
  return (
    <Suspense fallback={<div>Carregando...</div>}>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/contato" element={<Contato />} />
        <Route path="/termos-condicoes" element={<TermosCondicoes />} />
        <Route path="/planos" element={<PlansPage />} />
        <Route path="/acesso_sistema" element={<AccessPage />} />
        <Route path="/acesso_sistema/check-up" element={<PdfUploadPage />} />
        <Route path="/pagamento" element={<ImportantInfoPage />} />
      </Routes>
    </Suspense>
  );
};

export default AppRoutes;
