/* eslint-disable*/
import React, { useRef, useState } from 'react';
import Keyboard from 'react-simple-keyboard';
import 'react-simple-keyboard/build/css/index.css';
import SampleWords from './SampleWords';

import './KeyboardComplete.css';

function KeyboardComplete() {
  const [input, setInput] = useState('');
  const [currentWordNumber, setcurrentWordNumber] = useState(0);

  const keyboard = useRef();
  const wordList = ['random', 'words', 'tooo'];
  var correct = true;
  var word_correct = false;
  var proceedNext = false;

  const onChangeInput = (event) => {
    const inputTB = event.target.value;
    setInput(inputTB);
    keyboard.current.setInput(inputTB);
    const typedLetters = inputTB.split('');
    const currentWord = typedLetters.slice(-1)[0];
    const currentCorrectArray = wordList[currentWordNumber].split('');
    console.log(currentWordNumber, currentWord);
    console.log(typedLetters);
    if (currentWordNumber < wordList.length) {
      if (currentWord !== ' ') {
        if (
          typedLetters.some(
            (letter, index) => letter !== currentCorrectArray[index],
          )
        ) {
          window.correct = false;
          console.log(window.correct);
        } else {
          console.log(window.correct);
          window.correct = true;
        }
      }
      console.log(window.correct, currentCorrectArray.length);
      if (
        currentWord === ' ' &&
        window.correct === true &&
        typedLetters.length - 1 === currentCorrectArray.length
      ) {
        window.word_correct = true;
        proceedNext = true;
      } else if (
        currentWord === ' ' &&
        window.correct === false &&
        typedLetters.length - 1 === currentCorrectArray.length
      ) {
        window.word_correct = false;
        proceedNext = true;
      }
      if (proceedNext) {
        setcurrentWordNumber(currentWordNumber + 1);
        setInput('');
        proceedNext = false;
      }
    }
  };

  return (
    <div className="keyboard">
      <SampleWords
        currentWord={wordList[currentWordNumber]}
        wordList={wordList}
        letterCorrect={window.correct}
        wordCorrect={window.word_correct}
      />
      <input value={input} onChange={onChangeInput} autoFocus />
      <div style={{ pointerEvents: 'none' }}>
        <Keyboard
          keyboardRef={(r) => (keyboard.current = r)}
          layout={{
            default: [
              '` 1 2 3 4 5 6 7 8 9 0 - = {backspace}',
              '{tab} q w e r t y u i o p [ ] \\',
              "{capslock} a s d f g h j k l ; ' {enter}",
              '{shiftleft} z x c v b n m , . / {shiftright}',
              '{controlleft} {altleft} {space} {altright} {controlright}',
            ],
          }}
          display={{
            '{tab}': 'tab',
            '{backspace}': 'backspace',
            '{enter}': 'enter',
            '{capslock}': 'caps lock',
            '{shiftleft}': 'shift',
            '{shiftright}': 'shift',
            '{controlleft}': 'ctrl',
            '{controlright}': 'ctrl',
            '{altleft}': 'alt',
            '{altright}': 'alt',
            '{space}': ' ',
          }}
          layoutName="default"
          physicalKeyboardHighlight
        />
      </div>
    </div>
  );
}

export default KeyboardComplete;
