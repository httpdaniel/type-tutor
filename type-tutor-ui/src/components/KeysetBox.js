/* eslint-disable */
import React from 'react';
import '../styles/App.scss';

function KeysetBox(props) {
  const { keys, unmastered, current, first } = props;

  return (
    <div>
      {keys[1] === false && current === true ? (
        <div className="keyset__box__current">
          {keys[0]}
        </div>
      ) : (keys[1] === false && unmastered === true ? (
        <div className="keyset__box__unmastered">
          {keys[0]}
        </div>
      ) : (keys[1] === false && unmastered === false ? (
        <div className="keyset__box__closed">
          {keys[0]}
        </div>
      ) : (
        <div className="keyset__box__open">
          {keys[0]}
        </div>
      )
      )
      )}
    </div>
  );
}

export default KeysetBox;
