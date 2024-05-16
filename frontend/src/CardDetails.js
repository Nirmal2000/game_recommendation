import styles from './CardDetails.module.css'
import {ReactComponent as Spark} from './public/spark.svg'
import {ReactComponent as PC} from './public/steam.svg'
import {ReactComponent as PS} from './public/playstation.svg'
import {ReactComponent as Xbox} from './public/xbox.svg'
import {ReactComponent as Switch} from './public/switch.svg'

const CardDetails = ({item}) => {

    const platforms = {
        PC: <PC className={styles.plticon} />,
        PlayStation: <PS className={styles.plticon} />,
        Xbox: <Xbox className={styles.plticon} />,
        Switch: <Switch className={styles.plticon} />
    };

    const renderPlatformIcons = (platformsInfo) => {
        return platformsInfo.map(p => {
            const IconComponent = platforms[p.platform.name];
            const url = p.platform.url;            
            return url ? (
                <a href={url} key={p.platform.name} target="_blank" rel="noopener noreferrer" style={{ display: 'inline-block' }}>
                    {IconComponent}
                </a>
            ) : (
                <div key={p.platform.name} style={{ display: 'inline-block' }}>
                    {IconComponent}
                </div>
            );
        });
    };

    return (
        <div className={styles.container}>
            <div className={styles.scoreAndPlatform}>
                <div className={styles.imagescore} style={{display: "flex", alignItems: "center"}}>
                                    <Spark style={{width: "2rem", height: "2rem"}}/>
                                    {item.reco_score}%
                </div>
                <div className={styles.platformIcons}>
                    {/* {renderPlatformIcons(item.parent_platforms)} */}
                </div>
            </div>

            <div className={styles.title}>{item.name} </div>
            <div className={styles.reason}>“ {item.reco_reason} ”</div>

            <div className={styles.ratings}>
                {/* <div>IGN: </div> */}
                <div>Metacritic: {Math.round(item.aggregated_rating)}</div>
            </div>
            {/* <div>Check it out</div>             */}
        </div>
    )
}

export default CardDetails;