import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Input from "./pages/Input";
import Loading from "./pages/Loading";
import Output from "./pages/Output";

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Input />} />
        <Route path="/loading" element={<Loading />} />
        <Route path="/output" element={<Output />} />
      </Routes>
    </Router>
  );
}

export default App;
