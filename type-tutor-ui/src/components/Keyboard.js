import React, { useRef, useState } from 'react';
import Keyboard from 'react-simple-keyboard';
import 'react-simple-keyboard/build/css/index.css';
import { Button } from '@material-ui/core';
import useKeyPress from '../customHooks/useKeyPress';
import SampleWords from './SampleWords';
import 'font-awesome/css/font-awesome.min.css';
import '../styles/KeyboardComplete.scss';
import '../styles/App.scss';
import Stats from './Stats';

function KeyboardComplete() {
  const text = 'seem year keep if also give between those what ask get one or stand now like state or how system and can great late under mean so be find know do person must make number give system get turn lead fact a head call all good tell run want when need each early very may you problem off life eye';
  const wordList = text.split(' ');
  const [input, setInput] = useState('');
  const [currentWordNumber, setcurrentWordNumber] = useState(0);
  const [leftPadding, setLeftPadding] = useState(
    new Array(35).fill(' ').join(''),
  );

  // For displaying text to type
  const [typedChar, setTypedChar] = useState('');
  const [currChar, setCurrChar] = useState(text.charAt(0));
  const [toTypeChar, setToTypeChar] = useState(text.substring(1));

  // For Calculating Words Per Minute
  const [startTime, setStartTime] = useState();
  const [wordCount, setWordCount] = useState(0);
  const [wpm, setWpm] = useState(0);
  const currentTime = () => new Date().getTime();

  useKeyPress((key) => {
    if (!startTime) {
      setStartTime(currentTime());
    }

    let updatedTypedChar = typedChar;
    let updatedToTypeChar = toTypeChar;

    if (key === currChar) {
      if (leftPadding.length > 0) {
        setLeftPadding(leftPadding.substring(1));
      }
      updatedTypedChar += currChar;
      setTypedChar(updatedTypedChar);

      setCurrChar(toTypeChar.charAt(0));

      updatedToTypeChar = toTypeChar.substring(1);
      // if (updatedToTypeChar.split(' ').length < 10) {
      //   updatedToTypeChar += ' ' + generate();
      // }
      setToTypeChar(updatedToTypeChar);

      if (toTypeChar.charAt(0) === ' ') {
        setWordCount(wordCount + 1);

        const durationInMinutes = (currentTime() - startTime) / 60000.0;

        setWpm(((wordCount + 1) / durationInMinutes).toFixed(2));
      }
    }
  });

  const [focused, setFocused] = useState(false);
  const [focusPopup, setFocusPopup] = useState(true);
  const keyboard = useRef();

  const correct = true;
  const word_correct = false;
  let proceedNext = false;

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
        currentWord === ' '
        && window.correct === true
        && typedLetters.length - 1 === currentCorrectArray.length
      ) {
        window.word_correct = true;
        proceedNext = true;
      } else if (
        currentWord === ' '
        && window.correct === false
        && typedLetters.length - 1 === currentCorrectArray.length
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
      <Stats wordsperminute={wpm} />
      <div className="main__text">
        {focusPopup ? (
          <div className="out__of__focus">
            <Button
              style={{ backgroundColor: 'transparent' }}
              onClick={() => { setFocused(true); setFocusPopup(false); }}
            >
              <i className="fa fa-mouse-pointer" />
              Click to activate
            </Button>
          </div>
        ) : (<></>)}
        <div id="words" className={focused ? 'notBlurred' : 'blurred'}>
          {/* <SampleWords
            currentWord={wordList[currentWordNumber]}
            wordList={wordList}
            letterCorrect={window.correct}
            wordCorrect={window.word_correct}
          /> */}
          <p className="Character">
            <span className="Character-out">{(leftPadding + typedChar).slice(-35)}</span>
            <span className="Character-current">{currChar}</span>
            <span className="Character-in">{toTypeChar.substr(0, 32)}</span>
          </p>
        </div>
      </div>
      <input value={input} onChange={onChangeInput} />
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
