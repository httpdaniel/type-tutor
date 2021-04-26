import React from 'react';
import '../styles/App.scss';
import 'react-loader-spinner/dist/loader/css/react-spinner-loader.css';
import Loader from 'react-loader-spinner';

function Loading() {
  return (
    <div className="loading__screen">
      <div className="loader">
        <Loader
          type="Oval"
          color="#b2b2b2"
          height={80}
          width={80}
        />
        <h2 id="loading__text">Loading next test...</h2>
      </div>
    </div>
  );
}

export default Loading;
