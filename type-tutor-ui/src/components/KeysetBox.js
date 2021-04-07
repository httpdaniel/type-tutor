/* eslint-disable */
import React from 'react';
import '../styles/App.scss';

function KeysetBox(props) {
  console.log(props);
  const { keys } = props;

  return (
    <div>
      {keys[1] === false ? (
        <div className="keyset__box__closed">
          {keys[0]}
        </div>
      ) : (
        <div className="keyset__box__open">
          {keys[0]}
        </div>
      )}
    </div>
  );
}

export default KeysetBox;
