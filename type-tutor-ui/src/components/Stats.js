/* eslint-disable */
import React, { useState } from 'react';
import KeysetBox from './KeysetBox';
import '../styles/App.scss';

function Stats(props) {
  const { wordsperminute, numerrors, accuracyscore, keyset, notmastered } = props;

  const [speed, setSpeed] = useState(0);
  const [speedChange, setSpeedChange] = useState(1.2);

  const [errors, setErrors] = useState([]);
  const [errorsChange, setErrorsChange] = useState(5.5);

  const [score, setScore] = useState(0);
  const [scoreChange, setScoreChange] = useState(4.8);

  // const [keyset, setKeyset] = useState(['A', 'B', 'C']);
  const [keybox, setKeybox] = useState([])

  const [currentKey, setCurrentKey] = useState('');

  const alphabet = ['E', 'A', 'R', 'I', 'O', 'T', 'N', 'S', 'L', 'C', 'U', 'D', 'P', 'M', 'H', 'G', 'B', 'F', 'Y', 'W', 'K', 'V', 'X', 'Z', 'J', 'Q'];

  for(let i = 0; i<alphabet.length; i++) {
    const open = keyset.includes(alphabet[i]);
    const unlocked = notmastered.includes(alphabet[i]);
    keybox.push(<KeysetBox key={i} keys={[alphabet[i], open]} unlocked={unlocked}></KeysetBox>)
  }

  return (
    <div className="statbox">
      <div className="statbox__top">
        Speed:
        <span>
          {wordsperminute}
          {/* (↑+
          {speedChange}
          ) */}
        </span>
        Errors:
        <span>
          {numerrors}
          {/* (↑+
          {errorsChange}
          ) */}
        </span>
        Accuracy:
        <span>
          {accuracyscore}%
          {/* (↑+
          {scoreChange}
          ) */}
        </span>
      </div>
      <div className="statbox__middle">
        Key Set:
        {keybox}
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
