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

const Landing = () => {

    const [searchActive, setSearchActive] = useState(false);
    const [inputValue, setInputValue] = useState('');
    const [results, setResults] = useState(null);
    const [isLoading, setIsLoading] = useState(false);


    const handleSearch = async () => {
        console.log("-->", inputValue)
        if (!inputValue.trim()) return; 
        setSearchActive(true);
        setIsLoading(true);
        try {
            const response = await axios.get(`http://127.0.0.1:5000/recommend?query=${encodeURIComponent(inputValue)}`);
            setResults(Object.values(response.data));
            console.log(Object.values(response.data))
            setIsLoading(false);
        } catch (error) {
            console.error('Error fetching data:', error);
            setIsLoading(false);
            setResults(null);
        }
    };

    return (
        <div className={`${styles.container}`}>            
             <div className={styles.firstBackground}></div>
             <div className={styles.secondBackground}></div>

             {searchActive ? (
                <>
                    <div className={styles.searchactive}>
                        <div className={styles.actionBoxTop}>
                                <Spark className={styles.iconLeft}/>
                                <input 
                                    type="text" 
                                    placeholder="An action-packed combat game, like Sekiro!" 
                                    className={styles.textbox} 
                                    onChange={(e) => {
                                            console.log("HERE")
                                            setInputValue(e.target.value)
                                        }
                                    }
                                    value={inputValue}
                                />
                                <Rab className={styles.arrowRight} onClick={handleSearch}/>
                        </div>
                        <div style={{display: "flex"}}>
                        {results && results.length > 0 && <img src={results[0].background_image} alt={`Slide ${0}`} style={{ width: '1200px', height: '700px', borderRadius: "50px"}} /> }
                        
                        {results && results.length > 0 &&
                            <>
                            <div className={styles.bginfobox}>
                                <div style={{marginLeft: "50px", marginRight: "50px", fontWeight: "300px"}}>
                                    <div style={{fontSize: '26px', marginTop: "50px", color: "#FFFFFF", fontFamily: "ABeeZee", marginBottom: "250px"}}>{results[0].why}</div>
                                    
                                    <div>
                                        <div style={{ display: 'flex', flexDirection: "column", fontSize: "15px", color: "#FFFFFF", marginBottom: "20px"}}>
                                            <div><span style={{color: "#7C8ECA"}}>Release date: </span> {results[0].released}</div>
                                            <div><span style={{color: "#7C8ECA"}}>Platform: </span> {results[0].parent_platforms.map(platform => platform.platform.name).join(', ')}</div>                                        
                                            <div><span style={{color: "#7C8ECA"}}>Mode: </span> {results[0].released}</div>
                                        </div>    
                                        <div style={{ display: 'flex', justifyContent: 'flex-start'}}>
                                            <div className={styles.tagbox}>{results[0].tags[0].name}</div>
                                            <div className={styles.tagbox} style={{marginLeft: "10px"}}>{results[0].tags[1].name}</div>
                                            <div className={styles.tagbox} style={{marginLeft: "10px"}}>{results[0].tags[2].name}</div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                            </>}
                        </div>
                    </div>
                    
                    {isLoading && <p>Loading...</p>}
                    {results && results.length > 0 && (
                        /* Similar Titles */

                        <div style={{marginLeft: "100px", marginRight: "100px"}}>
                        <div style={{fontFamily: "ABeeZee", color: "rgba(255, 255, 255, 0.6)", fontWeight: "700px", fontSize: "30px", }}>Similar Titles</div> 
                        <Swiper
                            className="min-h-[250px]" // ARBITARY VALUE
                            slidesPerView={6} 
                            navigation
                            spaceBetween={1}
                            autoplay={true}
                            speed={1000}                        
                            modules={[Navigation, Autoplay, Pagination]}                            
                            
                            style={{
                            margin:"10px",
                            }}
                        >
                            {results.map((item, index) => {
                                if(index==0) return(<></>)
                                return (
                                    <SwiperSlide key={index}>
                                        <img src={item.background_image} alt={`Slide ${index}`} style={{ width: '250px', height: '250px', borderRadius: "30px"}} />
                                    </SwiperSlide>
                                )
                            })}
                        </Swiper>
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
                        <Rab className={styles.arrowRight} onClick={handleSearch}/>
                    </div>                    
                </>                
             )}
             
             
        </div>
    )
}

export default Landing;

