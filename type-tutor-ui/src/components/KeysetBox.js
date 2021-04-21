/* eslint-disable */
import React from 'react';
import '../styles/App.scss';

function KeysetBox(props) {
  const { keys, unlocked } = props;

  return (
    <div>
      {keys[1] === false && unlocked === false ? (
        <div className="keyset__box__closed">
          {keys[0]}
        </div>
      ) : (keys[1] === false && unlocked === true ? (
        <div className="keyset__box__unlocked">
          {keys[0]}
        </div>
      ) : (
        <div className="keyset__box__open">
          {keys[0]}
        </div>
      )
      )}
    </div>
  );
}

export default KeysetBox;
