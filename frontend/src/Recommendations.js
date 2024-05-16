import React, { useState } from 'react';
import styles from './Recommendations.module.css'
import CardDetails from './CardDetails'
import {Swiper, SwiperSlide} from 'swiper/react'
import {EffectCoverflow, Pagination, Navigation} from 'swiper'
import {ReactComponent as Spark} from './public/spark.svg'
import Likebar from './Likebar';
import 'swiper/css'
import 'swiper/css/pagination'
import 'swiper/css/navigation'
import 'swiper/css/effect-coverflow'


const Recommendations = ({results}) => {
    const [hoverStates, setHoverStates] = useState({});
    const [activeIndex, setActiveIndex] = useState(0);  // State to track the active index

    const handleSlideChange = (swiper) => {
        console.log("INDEX",swiper.realIndex)
        setActiveIndex(swiper.realIndex);  // Update active index on slide change
    };

    const handleMouseEnter = (index) => {
        setHoverStates(prev => ({ ...prev, [index]: true }));
    };

    const handleMouseLeave = (index) => {
        setHoverStates(prev => ({ ...prev, [index]: false }));
    };
    

    return (
        <div className={styles.container}>
            <Swiper
                effect={'coverflow'}
                grabCursor={true}
                centeredSlides={true}
                loop={true}
                slidesPerView={'auto'}
                coverflowEffect={{
                  rotate: 0,
                  stretch: -10,
                  depth: 100,
                  modifier: 2.5,
                }}                                
                modules={[EffectCoverflow, Pagination, Navigation]}
                className={styles.swiperContainer}           
                onSlideChange={handleSlideChange}
            >
                {results.map((item, index)=>
                    {
                        
                        return (
                        <SwiperSlide key={index} className={styles.swiperslider} onMouseEnter={() => handleMouseEnter(index)} onMouseLeave={() => handleMouseLeave(index)}>
                            <img src={`https://${item.cover_720p}`} className={styles.image}></img>
                            {!hoverStates[index] && 
                                <div className={styles.imagescore} style={{display: "flex", alignItems: "center"}}>
                                    <Spark style={{width: "2rem", height: "2rem"}}/>
                                    {item.reco_score}%
                                </div>
                            }
                            {hoverStates[index] && <CardDetails item={item}/>}
                            {index==activeIndex && <Likebar item={item}/>}
                        </SwiperSlide>
                    )}
                )}
            </Swiper>
            
        </div>
    )
}

export default Recommendations;