import react, {useContext, useEffect, useState} from 'react'
import { useNavigate } from "react-router-dom";
import { Table } from 'react-bootstrap';
import { AnalyzeContext } from '../AnalyzeContext';
import AnalyzeRow from './AnalyzeRow';
import PageTitle from './PageTitle' 

const AnalyzeTable = () => {
    const [analyzes, setAnalyzes] = useContext(AnalyzeContext)

    const handleDelete = (id) => {
        fetch("http://localhost:8000/delete/" + id, {
            method: "DELETE",
            headers: {
                accept: 'application/json'
            }
        })
            .then(resp => {
            return resp.json()
            })
            .then(result => {
                if (result.status === 'ok') {
                    const filteredAnalyzes = analyzes.data.filter((analysis) => analysis.id !== id);
                    setAnalyzes({ data: [...filteredAnalyzes] })
                    alert("Удалено успешно")
                } else {
                    alert("Удаление не удалось")
            }
        })
    }

    const handleUpload = (id) => {
        console.log(id)
        fetch("http://localhost:8000/upload/" + id, {
            headers: {
                Accept: 'application/json'
            }
        }).then((resp) => {
            return resp.json()
        }).then((result) => {
            const link = document.createElement('a');
            link.href = result.data;
            link.setAttribute('download', '');
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
        })
    }

    useEffect(() => {
        fetch("http://localhost:8000/analyzes")
        .then(resp => {
            return resp.json();
        }).then(results => {
            setAnalyzes({"data": [...results.data]})
        })
    })

    return (
        <div>
            <PageTitle title="Анализ секвенированных данных "/>
            <Table striped bordered hower>
                <thead>
                    <tr>
                        <th>Название</th>
                        <th>Дата загрузки</th>
                        <th></th>
                    </tr>
                </thead>
                <tbody>
                    {analyzes.data.map((analysis) => (
                        <AnalyzeRow
                            id = {analysis.id}
                            fileName = {analysis.fileName}
                            time = {analysis.time}
                            stage = {analysis.stage}
                            key={analysis.id}
                            handleDelete = {handleDelete}
                            handleUpload = {handleUpload}
                        />
                    ))}
                </tbody>
            </Table>
        </div>
    );
}

export default AnalyzeTable