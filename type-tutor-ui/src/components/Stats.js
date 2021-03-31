/* eslint-disable */
import React, { useState } from 'react';
import '../styles/App.scss';

function Stats(props) {
  const { wordsperminute, numerrors, accuracyscore} = props;

  const [speed, setSpeed] = useState(0);
  const [speedChange, setSpeedChange] = useState(1.2);

  const [errors, setErrors] = useState([]);
  const [errorsChange, setErrorsChange] = useState(5.5);

  const [score, setScore] = useState(0);
  const [scoreChange, setScoreChange] = useState(4.8);

  const [keyset, setKeyset] = useState([]);
  const [currentKey, setCurrentKey] = useState('');

  return (
    <div className="statbox">
      <div className="statbox__top">
        Speed:
        <span>
          {wordsperminute}
          (↑+
          {speedChange}
          )
        </span>
        Errors:
        <span>
          {numerrors}
          (↑+
          {errorsChange}
          )
        </span>
        Accuracy:
        <span>
          {accuracyscore}%
          (↑+
          {scoreChange}
          )
        </span>
        Score:
        <span>
          {score}
          (↑+
          {scoreChange}
          )
        </span>
      </div>
      <div className="statbox__middle">
        Key Set:
        {' '}
        {keyset}
      </div>
      <div className="statbox__bottom">
        Current Key:
        {' '}
        {currentKey}
      </div>
    </div>
  );
}

export default Stats;
