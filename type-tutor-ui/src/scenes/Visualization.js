/* eslint-disable */

import React, {useState, useEffect} from 'react';
import {Bar, Line, Pie} from 'react-chartjs-2';
import Container from '@material-ui/core/Container';

const Visualization = (props) => {    

    const [charAcc, setCharAcc] = useState(null)
    const [charCorr, setCharCorr] = useState(null)
    const [charIncorr, setCharIncorr] = useState(null)
    const [metricData, setMetricData] = useState(null)
    const [sessData, setSessData] = useState(null);
    const [wpmData, setWpmData] = useState(null);
    const [accData, setAccData] = useState(null);
    const [sessLabels, setSessLabels] = useState([]);



    useEffect(async ()=>{
        const url = "http://127.0.0.1:8000/getSessions"
        const data = await fetch(url, {
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            },
            method: "POST",
            body: JSON.stringify({ user_id: 1 })
        }).then(res => res.json())
        let alphaObj = {}
        let metricObj = {}
        let sessObj = {}
        console.log(data)
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

        

    }, [])




    return (
        <Container className="vis-container">
            {/* <div className="wpm-container">
                <p>wpm</p>
                <h3>5</h3>

                <br/>
                <p>acc</p>
                <h3>60%</h3>
            </div> */}
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
        </Container>
    )
}

export default Visualization



// class Visualization extends Component{
//   constructor(props){
//     super(props);
//     this.state = {
//       chartData:props.chartData
//     }
//   }

//   static defaultProps = {
//     displayTitle:true,
//     displayLegend: true,
//     legendPosition:'right',
//     location:'City'
//   }

//   render(){
//     return (
//       <div className="chart">
//         <Bar
//           data={this.state.chartData}
//           options={{
//             title:{
//               display:this.props.displayTitle,
//               text:'Largest Cities In '+this.props.location,
//               fontSize:25
//             },
//             legend:{
//               display:this.props.displayLegend,
//               position:this.props.legendPosition
//             }
//           }}
//         />

        

//         <Pie
//           data={this.state.chartData}
//           options={{
//             title:{
//               display:this.props.displayTitle,
//               text:'Largest Cities In '+this.props.location,
//               fontSize:25
//             },
//             legend:{
//               display:this.props.displayLegend,
//               position:this.props.legendPosition
//             }
//           }}
//         />
//       </div>
//     )
//   }
// }

// export default Visualization;