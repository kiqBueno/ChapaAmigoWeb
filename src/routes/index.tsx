import { Suspense, lazy } from "react";
import { Routes, Route, Navigate } from "react-router-dom";

const Home = lazy(() => import("../pages/HomePage"));
const TermsConditionsPage = lazy(() => import("../pages/TermsConditionsPage"));
const ContactPage = lazy(() => import("../pages/ContactPage"));
const AccessPage = lazy(() => import("../pages/AccessPage"));
const PlansPage = lazy(() => import("../pages/PlansPage"));
const PdfUploadPage = lazy(() => import("../pages/AccessPage/PdfUploadPage"));
const CarouselManagementPage = lazy(
  () => import("../pages/AccessPage/CarouselManagementPage")
);
const ImportantInfoPage = lazy(() => import("../pages/ImportantInfoPage"));
const NotificationPage = lazy(() => import("../pages/NotificationPage"));

const AppRoutes = () => {
  return (
    <Suspense fallback={<div>Carregando...</div>}>
      {" "}
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/contato" element={<ContactPage />} />
        <Route path="/termosCondicoes" element={<TermsConditionsPage />} />
        <Route path="/planos" element={<PlansPage />} />{" "}
        <Route path="/acessoSistema" element={<AccessPage />} />
        <Route path="/acessoSistema/checkUp" element={<PdfUploadPage />} />
        <Route
          path="/acessoSistema/carouselManagement"
          element={<CarouselManagementPage />}
        />
        <Route path="/pagamento" element={<ImportantInfoPage />} />
        <Route path="/notificacao" element={<NotificationPage />} />
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </Suspense>
  );
};

export default AppRoutes;
