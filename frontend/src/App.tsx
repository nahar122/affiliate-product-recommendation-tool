import React from "react";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import "./App.css";
import Navbar from "./components/Navbar";
import AddDomainPage from "./pages/AddDomainPage";
import EditDomainPage from "./pages/EditDomainPage";
import HomePage from "./pages/HomePage";

function App() {
  return (
    <Router>
      <div className="App">
        <Navbar />
        <main className="w-3/4 mx-auto max-w">
          <Routes>
            <Route path="/" element={<HomePage />} />
            <Route path="/edit-domain" element={<EditDomainPage />} />
            <Route path="/add-domain" element={<AddDomainPage />} />
            {/* Add additional routes as needed */}
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App;
