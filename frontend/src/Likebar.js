import styles from './Likebar.module.css'
import {ReactComponent as Cart} from './public/cart.svg'
import {ReactComponent as CircleTick} from './public/circletick.svg'
import {ReactComponent as ThumbsUp} from './public/thumbsup.svg'
import {ReactComponent as ThumbsDown} from './public/thumbsdown.svg'
import {ReactComponent as AddGame} from './public/addgame.svg'

import {ReactComponent as CircleTickG} from './public/circletickglow.svg'
import {ReactComponent as ThumbsUpG} from './public/thumbsupglow.svg'
import {ReactComponent as ThumbsDownG} from './public/thumbsdownglow.svg'
import {ReactComponent as AddGameG} from './public/addgameglow.svg'

import axios from 'axios';
import { useState } from 'react'
import { Tooltip, ThemeProvider } from '@mui/material';
import { createTheme } from '@mui/material/styles';
import { Widgets } from '@mui/icons-material'


const theme = createTheme({
    components: {
      MuiTooltip: {
        styleOverrides: {
          tooltip: {
            // Directly apply your custom styles
            background: 'radial-gradient(78.5% 78.5% at 50% 2.8%, rgba(217, 217, 217, 0.3) 0%, rgba(115, 115, 115, 0.3) 100%)',
            backdropFilter: 'blur(10px)',
            borderRadius: '6px',
            color: '#e0e0e0',
            textAlign: 'center',
            fontSize: '1rem',
            fontFamily: 'ABeeZee, sans-serif',
            fontWeight: 400,
          }
        }
      }
    }
  });

const IconWithTooltip = ({ Icon, title, onClick, style, className }) => (
    <Tooltip title={title} placement="top" arrow PopperProps={{
        modifiers: [{
            name: 'offset',
            options: {
                offset: [0, 1],  // Adjust the offset if necessary
            },
        }],
    }}>
        <div onClick={onClick} style={{ ...style, cursor: 'pointer' }} className={className}>
            <Icon style={{width: "2rem", height: "2rem"}}/>
        </div>
    </Tooltip>
);

const Likebar = ({item}) => {
    const getIcon = (condition, GlowIcon, NormalIcon) => condition ? GlowIcon : NormalIcon;

    const [likeBarButtons, setLikeBarButtons] = useState({
        addgame: item.addgame || 0,        
        like: item.like === undefined ? -1 : item.like,
        completed: item.completed || 0
    });

    const iconProps = {
        'addgame': { Icon: getIcon(likeBarButtons.addgame === 1, AddGameG, AddGame), title: "Let's buy this game" },        
        'dislike': { Icon: getIcon(likeBarButtons.like === 0, ThumbsDownG, ThumbsDown), title: "Dislike this game" },
        'like': { Icon: getIcon(likeBarButtons.like === 1, ThumbsUpG, ThumbsUp), title: "Like this game" },
        'completed': { Icon: getIcon(likeBarButtons.completed === 1, CircleTickG, CircleTick), title: "Mark as completed" },
        'cart': { Icon: Cart, title: "Mark as completed" }
    };

    

    const handleButton = async (key, action=null) => {
        let newValue;
        console.log(likeBarButtons)
        if (key === 'like' && [-1, 0].includes(likeBarButtons['like'])) {
            newValue = 1
        } else if(key == 'dislike' && [-1, 1].includes(likeBarButtons['like'])){
            newValue = 0
            key='like'
        } else if(key == 'like' && likeBarButtons[key] == 1){
            newValue = -1
        } else if(key == 'dislike' && likeBarButtons['like'] == 0){
            
            newValue = -1
            key='like'
        }            
        else {            
            newValue = likeBarButtons[key] === 1 ? 0 : 1;
        }
        console.log(newValue, key)
        const response = await axios.post('http://127.0.0.1:5001/like_dislike', {
            email: localStorage.getItem('email'),
            key: key,
            value: newValue,
            game_name: item.name
        });
        console.log('Server response:', response.data);

        // Update the local state to reflect the change
        setLikeBarButtons(prev => ({
            ...prev,
            [key]: newValue
        }));
    }
    return (
        <ThemeProvider theme={theme}>
            <div className={styles.container}>
                {Object.entries(iconProps).map(([key, { Icon, title }]) => (
                    <IconWithTooltip
                        key={key}
                        Icon={Icon}
                        title={title}
                        onClick={() => handleButton(key)}
                        // style={{ marginRight: "rem" }}
                        className={styles.iconsize}
                    />
                ))}                
            </div>    
        </ThemeProvider>

    )
}

export default Likebar;