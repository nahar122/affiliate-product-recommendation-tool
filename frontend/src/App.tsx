import { Route, Routes } from "react-router-dom";
import IndexPage from "./routes";
import Navbar from "./components/Navbar";
import SignIn from "./routes/sign-in";
import AddDomainPage from "./routes/add-domain";
import EditDomainPage from "./routes/edit-domain";
import AuthenticatedRoutes from "./components/AuthenticatedRoutes";

function App() {
  return (
    <div>
      <header>
        <Navbar />
      </header>
      <main className="w-3/4 mx-auto">
        <Routes>
          <Route index element={<IndexPage />} />
          <Route path="login" element={<SignIn />} />
          <Route element={<AuthenticatedRoutes />}>
            <Route path="add-domain" element={<AddDomainPage />} />
            <Route path="edit-domain" element={<EditDomainPage />} />
          </Route>
        </Routes>
      </main>
    </div>
  );
}

export default App;
