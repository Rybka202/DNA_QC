import react from 'react'
import RingLoader from 'react-spinners/RingLoader'

const AnalyzeRow = ({id, fileName, time, stage, handleDelete, handleUpload}) => {
    if (stage === "Обработка"){
        return (
            <tr>
                <td>{fileName}</td> 
                <td>{time}</td>
                <td>
                    <RingLoader color={'#1573b0'} size={35} /> Идёт анализ данных
                </td>
            </tr>
        )
    }
    if (stage === "Ошибка"){
        return (
            <tr>
                <td>{fileName}</td> 
                <td>{time}</td>
                <td>
                Неверный формат файла
                <button onClick={() => handleDelete(id)} className = "btn btn-outline-danger btn-sm mr-2">Удалить</button>
                </td>
            </tr>
        )
    }
    return (
        <tr>
            <td>{fileName}</td>
            <td>{time}</td>
            <td>
                <button onClick={() => handleUpload(id)} className="btn btn-outline-info btn-sm ml-1 mr-2">Скачать</button>
                <button onClick={() => handleDelete(id)} className = "btn btn-outline-danger btn-sm mr-2">Удалить</button>
            </td>
        </tr>
    );
}

export default AnalyzeRow