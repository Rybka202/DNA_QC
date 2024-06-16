import { useState } from "react"
import { Button } from "react-bootstrap"
import { useNavigate } from "react-router-dom";
import PageTitle from './PageTitle' 

function FileForm(){
    const [file, setFile] = useState(null)

    const navigate = useNavigate(); 

    const handleFileInputChange = (event) => {
        console.log(event.target)
        setFile(event.target.files[0])
    }

    const handleSubmit = async (event) =>{
        event.preventDefault();

        const formData = new FormData();
        formData.append('file', file);

        try{
            const endpoint = "http://localhost:8000/download/"
            const response = await fetch(endpoint, {
                method: "POST",
                body: formData
            });

            if (response.ok){
                navigate('/');
            }
        } catch (error){
            navigate('/');
        }
    }

    return (
        <div>
            <PageTitle title="Загрузка файлов"/>
            <h1>Загрузка файлов</h1>
            <form onSubmit={handleSubmit}>
                
                <div style={{marginBottom: "20px"}}>
                    <input type="file" accept=".fastq, .fastq.gz"  onChange={handleFileInputChange}/>
                </div>
                <Button type="submit">Загрузить</Button> 
            </form>
        </div>
    )
}

export default FileForm