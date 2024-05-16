import React, { useState } from 'react';
import styles from './Landing.module.css';
import axios from 'axios';
import {ReactComponent as WhatGame} from './public/whatgame.svg'
import { Swiper, SwiperSlide } from 'swiper/react';
import { Navigation, Pagination, Autoplay } from 'swiper'; // Import modules here
import {ReactComponent as Shy} from './public/shy.svg'
import {ReactComponent as Spark} from './public/spark.svg'
import "swiper/css";
import {ReactComponent as Rab} from './public/rightarrowbutton.svg'
import {ReactComponent as UserIcon} from './public/usericon.svg'
import SearchBar from './SearchBar';
import Recommendations from './Recommendations';
import Likebar from './Likebar';
import Feedback from './Feedback';
import { GoogleLogin } from '@react-oauth/google';
import { jwtDecode } from "jwt-decode";
import userEvent from '@testing-library/user-event';

const Landing = () => {

    const [searchActive, setSearchActive] = useState(false);
    const [inputValue, setInputValue] = useState('');
    const [results, setResults] = useState(null);
    const [isLoading, setIsLoading] = useState(false);
    const [isHovered, setIsHovered] = useState(null);
    const [logged, setLogged] = useState(false);
    

    const handleSearch = async (inputValue) => {
        console.log(inputValue)
        // if (!inputValue.trim()) return; 
        setSearchActive(true);
        setIsLoading(true);
        try {
            console.log("IN",inputValue)
            const email = localStorage.getItem('email');  // Retrieve email from localStorage
            const response = await axios.post('http://127.0.0.1:5001/recommend', {
                query: inputValue,
                email: email
            });
            let temp = response.data.map(e => e[1]).sort((a, b) => b.reco_reason - a.reco_reason);
            console.log(temp)
            setResults(temp);
            console.log(temp)
            setIsLoading(false);
        } catch (error) {
            console.error('Error fetching data:', error);
            setIsLoading(false);
            setResults(null);
        }
    };

    const loginButton = async () => {
        window.location.href = 'http://127.0.0.1:5001/google-login';
    }
    const logoutButton = async () => {
        window.location.href = 'http://127.0.0.1:5001/logout';
    }

    return (
        <div className={`${styles.container}`}>            
             <div className={styles.firstBackground}></div>
             <div className={styles.secondBackground}></div>

             {searchActive ? (
                <>
                    <div style={{display: "flex", flexDirection: "row"}}>
                    <SearchBar handleSearch={handleSearch}/>                    
                    </div>
                    
                    {isLoading && <p>Loading...</p>}
                    {results && results.length > 0 && (                        

                        <div >                        
                        <Recommendations results={results}/>
                        
                        <Feedback/>
                        </div>
                    )}                    
               
               </>
             ): (
                <>
                    <WhatGame className={styles.whatgame}/>
                    <Shy className={styles.shy}/>
                    <div className={styles.actionBox}>
                        <Spark className={styles.iconLeft}/>
                        <input 
                            type="text" 
                            placeholder="An action-packed combat game, like Sekiro!" 
                            className={styles.textbox} 
                            onChange={(e) => {
                                    console.log(e.target.value)
                                    setInputValue(e.target.value)
                                }
                            }
                            value={inputValue}
                        />
                        <Rab className={styles.arrowRight} onClick={() => handleSearch(inputValue)}/>
                    </div>
                    <button onClick={loginButton}>Login</button>
                    <button onClick={logoutButton}>Logout</button>
                </>                
             )}
             
            
        { !logged && !localStorage.getItem('email') && <GoogleLogin
            onSuccess={credentialResponse => {
                var credentialResponse = jwtDecode(credentialResponse.credential)
                localStorage.setItem('email', credentialResponse['email'])
                setLogged(true)
            }}
            onError={() => {
                console.log('Login Failed');
            }}
        /> }
        </div>
    )
}

export default Landing;

