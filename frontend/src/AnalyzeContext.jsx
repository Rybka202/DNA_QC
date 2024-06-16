import react, {useState, createContext} from 'react'

export const AnalyzeContext = createContext();

export const AnalyzeProvider = (props) => {
    const[analyzes, setAnalyzes] = useState({"data": []});

    return (
        <AnalyzeContext.Provider value = {[analyzes, setAnalyzes]}>
            {props.children}
        </AnalyzeContext.Provider>
    )
}