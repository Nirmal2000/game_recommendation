import styles from './SearchBar.module.css'
import React, { useState } from 'react';
import {ReactComponent as Spark} from './public/spark.svg'
import {ReactComponent as Rab} from './public/rightarrowbutton.svg'
import {ReactComponent as UserIcon} from './public/usericon.svg'

const SearchBar = ({handleSearch}) => {
    const [inputValue, setInputValue] = useState('');

    return (
        <div className={styles.container}>
            <Spark style={{width: "2rem", height: "2rem"}}/>
            <input 
                type="text" 
                placeholder="An action-packed combat game, like Sekiro!"
                className={styles.input}
                onChange={(e) => {
                        console.log("HERE")
                        setInputValue(e.target.value)
                    }
                }
                value={inputValue}
            />
            <Rab style={{width: "1.5rem", height: "1.5rem", marginRight: "1rem"}} onClick={() => handleSearch(inputValue)}/>
            <UserIcon style={{borderRadius: "100px", width: "3rem", height: "3rem"}}/>
        </div>
    )
}

export default SearchBar