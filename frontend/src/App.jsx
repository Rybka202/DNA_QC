import react from 'react'
import { BrowserRouter as Router, Link, Route, Routes } from 'react-router-dom'
import NavBar from "./components/NavBar"
import { AnalyzeProvider } from './AnalyzeContext'
import AnalyzeTable from './components/AnalyzeTable'
import FileForm from './components/FileForm'

function App() {

  return (
    <div>
      <Router>
      <AnalyzeProvider>
        <NavBar />
        <div className='row'>
          <div className="col-sm-10 col-xm-12 mr-auto ml-auto mt-4 mb-4">
            <Routes>
              <Route exact path = "/" element={<AnalyzeTable />} />
              <Route exact path = "/addanalysis" element={<FileForm />} />
            </Routes>
          </div>
        </div>
      </AnalyzeProvider>
      </Router>
    </div>
  )
}

export default App
