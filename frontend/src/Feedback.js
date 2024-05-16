import {ReactComponent as FeedbackIcon} from './public/feedback.svg'
import styles from './Feedback.module.css'

const Feedback = () => {

    return (
        <div style={{marginLeft: "1rem", marginBottom: "1rem", display: "flex", alignItems: "center"}}>
            <FeedbackIcon/>
            <span className={styles.text}> Faced an issue? </span>
        </div>
    )
}
export default Feedback;