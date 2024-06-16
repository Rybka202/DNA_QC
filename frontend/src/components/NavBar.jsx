import react, {useContext, useState} from 'react'
import { Navbar, Nav, Form, FormControl, Button, Badge } from 'react-bootstrap'
import { Link } from 'react-router-dom'
import { AnalyzeContext } from '../AnalyzeContext'

const NavBar = () =>{
    const [search, setSearch] = useState("")
    const [analyzes, setAnalyzes] = useContext(AnalyzeContext)

    const updateSearch = (e) => {
        setSearch(e.target.value)
    }

    const filterAnalyze = (e) => {
        e.preventDefault()
        const analysis = analyzes.data.filter(analysis => analysis.fileName.toLowerCase() === search.toLowerCase())
        setAnalyzes({"data" : [...analysis]})
    }

    return(
        <Navbar bg="dark" expand="lg" variant="dark">
            <Navbar.Brand href="/">Анализ качества FastQ файлов</Navbar.Brand>
            <Navbar.Toggle aria-controls="basic-navbar-nav" />
            <Navbar.Collapse id="basic-navbar-nav">
                <Nav className="mr-auto">            
                    <Badge className="mt-2" variant="primary">Количество анализов {analyzes.data.length}</Badge>
                </Nav>
                <Form onSubmit={ filterAnalyze } className="d-flex">
                    <Link to="/addanalysis" className="btn btn-primary btn-sm mr-3">Загрузить файл</Link>
                    <FormControl value = {search} onChange={updateSearch} type="text" placeholder="Поиск" className="mr-sm-2" />
                    <Button type="submit"  variant="outline-primary">Найти</Button>
                </Form>
            </Navbar.Collapse>
        </Navbar>
    );
}

export default NavBar;