/* eslint-disable */

import React, {Component} from 'react';
import {Bar, Line, Pie} from 'react-chartjs-2';
import Container from '@material-ui/core/Container';


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


const Visualization = (props) => {
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
                            labels :  ['Boston', 'Worcester', 'Springfield', 'Lowell', 'Cambridge', 'New Bedford'],
                            datasets : [
                            {
                                label:'Stats',
                                data:[10,20,5,2,8,25],
                                backgroundColor:[
                                'rgba(191, 191, 191, 0.5)',
                                ]
                            },
                            {
                                label:'Stats2',
                                data:[19,2,15,22,48,2],
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
                            text:'Words Per Minute',
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
                            labels :  ['Boston', 'Worcester', 'Springfield', 'Lowell', 'Cambridge', 'New Bedford'],
                            datasets : [
                            {
                                label:'Stats',
                                data:[10,20,5,2,8,25],
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
                            text:'Accuracy',
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
                            labels :  ['Boston', 'Worcester', 'Springfield', 'Lowell', 'Cambridge', 'New Bedford'],
                            datasets : [
                            {
                                label:'Stats',
                                data:[10,20,5,2,8,25],
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
