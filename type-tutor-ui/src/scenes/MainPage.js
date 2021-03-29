import React, { useState } from 'react';
import { Button } from '@material-ui/core';
import Keyboard from '../components/Keyboard';
import Stats from '../components/Stats';
import '../styles/App.scss';

function MainPage() {
  return (
    <div className="main">
      <div className="main__body">
        {/* <Stats /> */}
        <Keyboard />
      </div>
    </div>
  );
}

export default MainPage;
