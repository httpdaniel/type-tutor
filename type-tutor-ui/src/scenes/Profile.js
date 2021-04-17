/* eslint-disable */

import React,  {useState, useEffect} from 'react';
import Avatar from '@material-ui/core/Avatar';
import Button from '@material-ui/core/Button';
import CssBaseline from '@material-ui/core/CssBaseline';
import TextField from '@material-ui/core/TextField';
import FormControlLabel from '@material-ui/core/FormControlLabel';
import Checkbox from '@material-ui/core/Checkbox';
import Link from '@material-ui/core/Link';
import Grid from '@material-ui/core/Grid';
import PersonOutlinedIcon from '@material-ui/icons/PersonOutlineOutlined';
import Typography from '@material-ui/core/Typography';
import { makeStyles } from '@material-ui/core/styles';
import Container from '@material-ui/core/Container';
import {Bar, Line, Pie} from 'react-chartjs-2';

const useStyles = makeStyles((theme) => ({
    paper: {
        marginTop: theme.spacing(8),
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
    },
    avatar: {
        margin: theme.spacing(1),
        backgroundColor: theme.palette.secondary.main,
    },
}));

function Profile() {
  const classes = useStyles();
  const [charAcc, setCharAcc] = useState(null)
  const [charCorr, setCharCorr] = useState(null)
  const [charIncorr, setCharIncorr] = useState(null)
  const [metricData, setMetricData] = useState(null)
  const [sessData, setSessData] = useState(null);
  const [wpmData, setWpmData] = useState(null);
  const [accData, setAccData] = useState(null);
  const [sessLabels, setSessLabels] = useState([]);
  const [jwt, setJwt] = useState(localStorage.getItem('jwt'));
  const [email, setEmail] = useState(localStorage.getItem('email'));

  useEffect(async ()=>{
    window.addEventListener('storage', async () => {
      console.log('Storage Update');
      setJwt(localStorage.getItem('jwt'));
      setEmail(localStorage.getItem('email'));
      if(jwt && email){
        const url = "/getSessions"
        const data = await fetch(url, {
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            },
            method: "POST",
            body: JSON.stringify({ token:jwt, email: email })
        }).then(res =>{ res.json()
        let alphaObj = {}
        let metricObj = {}
        let sessObj = {}
        // console.log(data)
        Object.entries(data).forEach(el => {
            const [key, value] = el
            if (key.length == 1) {
                alphaObj[key] = value
            } else {
                metricObj[key] = value
            }
        })
    
        const character_accuracy = Object.values(alphaObj).map(el => {
            return el.character_accuracy
        })
    
        const correct_characters = Object.values(alphaObj).map(el => {
            return el.correct_characters
        })
    
        const incorrect_characters = Object.values(alphaObj).map(el => {
            return el.incorrect_characters
        })
    
    
        Object.entries(data).forEach(el => {
            const [key, value] = el
            if (key.includes("session")) {
                sessObj[key] = value
            } 
        })
    
        console.log(sessObj)
    
        setSessData(sessObj);
    
        const sess_wpm = Object.values(sessObj).map(el => {
            return el.WPM;
        })
    
        const sess_acc = Object.values(sessObj).map(el => {
            return el.totalAccuracy;
        })
    
        console.log(sess_wpm)
        setSessLabels(Array.from({length: sess_wpm.length}, (_, i) => i + 1)        )
        setAccData(sess_acc)
        setWpmData(sess_wpm)
        
        setCharAcc(character_accuracy)
        setCharCorr(correct_characters)
        setCharIncorr(incorrect_characters)
    
        
        })
      }
    });
    }, [])

  return (
    <Container className="vis-container" maxWidth={1}>
        <CssBaseline />
        <div className={classes.paper}>
            <Avatar className={classes.avatar}>
            <PersonOutlinedIcon />
            </Avatar>
            <Typography component="h1" variant="h5">
            Profile
            </Typography>
        </div>
    <Grid container
  direction="row"
  justify="space-evenly"
  alignItems="flex-start">
    <Grid xs="9">
      <h1>User Statistics</h1>
            
            <div className="chart-container">
                <Line className="wpm-chart"
                    data={{
                            labels :  sessLabels,
                            datasets :  [
                            {
                                label:'Accuracy',
                                data:[
                                    {
                                        label:'Accuracy',
                                        data:accData,
                                        backgroundColor:[
                                        'rgba(191, 191, 191, 0.5)',
                                        ]
                                    }
                                    ]
                                
                            }
                            ]
                        }}


                    options={{
                        maintainAspectRatio: false,
                        title:{
                            display: true,
                            text:'Accuracy Per Session',
                            fontSize:20
                        },
                        legend:{
                            display: true,
                            position:'right'
                        }
                    }}
                />
            </div>

            <div className="chart-container">
                <Line className="wpm-chart"
                    data={{
                            labels :  sessLabels,
                            datasets : [
                            {
                                label:'WPM',
                                data:wpmData,
                                backgroundColor:[
                                'rgba(191, 191, 191, 0.5)',
                                ]
                            }
                            ]
                        }}


                    options={{
                        maintainAspectRatio: false,
                        title:{
                            display: true,
                            text:'WPM Per Session',
                            fontSize:20
                        },
                        legend:{
                            display: true,
                            position:'right'
                        }
                    }}
                />
            </div>

            <div className="chart-container">
                <Bar className="wpm-chart"
                    data={{
                            labels :  ['A', 'B', 'C', 'D', 'E', 'F', 'J', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'],
                            datasets : [
                            {
                                label:'Character Correctness',
                                data: charCorr,
                                backgroundColor:[
                                'rgba(191, 191, 191, 0.5)',
                                ]
                            }, 
                            {
                                label:'Character Accuracy',
                                data: charAcc,
                                backgroundColor:[
                                'rgba(191, 191, 191, 0.7)',
                                ]

                            },
                            {
                                label:'Character Incorrectness',
                                data: charIncorr,
                                backgroundColor:[
                                'rgba(191, 191, 191, 0.9)',
                                ]

                            }
                            ]
                        }}


                    options={{
                        maintainAspectRatio: false,
                        title:{
                            display: true,
                            text:'Key Frequency',
                            fontSize:20
                        },
                        legend:{
                            display: true,
                            position:'right'
                        }
                    }}
                />
            </div>
        </Grid>

        <Grid xs="1" zeroMinWidth>    
        <h1 style={{ whiteSpace: 'nowrap'}}>User Control</h1>            
                <Grid container direction="column" spacing={1} style={{ marginTop: '20px' }}>
                <Grid item>
                    <Link href="/update_email" variant="body2">
                    Update Email
                    </Link>
                </Grid>
                <Grid item>
                    <Link href="/update_password" variant="body2">
                    Update Password
                    </Link>
                </Grid>
                <Grid item style={{ marginTop: '10px' }}>
                    <Link href="/delete_account" variant="body2" style={{ color: 'red' }}>
                    Delete Account
                    </Link>
                </Grid>
                </Grid>
        </Grid>
        </Grid>
    </Container>
  );
}

export default Profile;
