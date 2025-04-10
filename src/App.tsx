import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import { DocumentUpload } from "./pages/DocumentUpload";
import { Navigation } from "./components/Navigation/Navigation";
import "./App.css";

function App() {
  return (
    <Router>
      <div className="app-container">
        <Navigation />
        <main className="main-content">
          <Routes>
            <Route path="/" element={<DocumentUpload />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App;
