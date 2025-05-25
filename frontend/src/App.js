import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Input from "./pages/Input";

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Input />} />
      </Routes>
    </Router>
  );
}

export default App;
