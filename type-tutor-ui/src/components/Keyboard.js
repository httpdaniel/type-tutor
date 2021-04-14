import React, { useRef, useState } from 'react';
import Keyboard from 'react-simple-keyboard';
import 'react-simple-keyboard/build/css/index.css';
import { Button } from '@material-ui/core';
import { Email } from '@material-ui/icons';
import useKeyPress from '../customHooks/useKeyPress';
import SampleWords from './SampleWords';
import 'font-awesome/css/font-awesome.min.css';
import '../styles/KeyboardComplete.scss';
import '../styles/App.scss';
import Stats from './Stats';

const incorrect = [];

function KeyboardComplete() {
  // 'seem year keep if also give between those what ask get
  // one or stand now like state or how system and
  // can great late under mean so be find know do person must
  // make number give system get turn lead fact a head call all
  // good tell run want when need each early very may you problem off life eye';
  const text = 'to tar it or too it are trio oar air ariot ear';
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

  // For saving incorrect characters
  // const [incorrectChars, setIncorrectChars] = useState([]);

  const [errors, setErrors] = useState(0);
  const [correctCount, setCorrectCount] = useState(0);

  const [accuracy, setAccuracy] = useState(0);

  const [gameOver, setGameOver] = useState(false);

  const [gameState, setGameState] = useState({});

  const targetAccuracy = 90;
  const targetWPM = 40;

  const keyset = ['E', 'A', 'R', 'I', 'O', 'T'];

  const count = (str, c) => {
    let result = 0;
    let i = 0;
    for (i; i < str.length; i++) if (str[i] === c) result++;
    return result;
  };

  function generateTest(email, token) {
    const url = '/generate_text?';
    fetch(`${url
    }&token=${
      encodeURIComponent(token)
    }&email=${
      encodeURIComponent(email)}`, {
      method: 'GET',
      headers: {
        'Content-type': 'application/json',
      },
    }).then((res) => res.json()).then(
      (res) => {
        console.log(res);
        const str = JSON.stringify(res);
        console.log(str);
      },
    );
  }

  function submitTest(info, email, token) {
    fetch('/submit', {
      method: 'POST',
      headers: {
        'Content-type': 'application/json',
      },
      body: JSON.stringify(info),
    }).then((res) => res.json()).then(
      (res) => {
        console.log(res);
        const str = JSON.stringify(res);
        console.log(str);
      },
    );
    generateTest(email, token);
  }

  function endGame() {
    setGameOver(true);
    const incorrect_info = {};
    const correct_info = {};
    const acc_info = {};
    const character_time = {};
    const letters = 'abcdefghijklmnopqrstuvwxyz';
    letters.split('').map(
      (x) => [correct_info[x] = 0, incorrect_info[x] = 0, character_time[x] = 0, acc_info[x] = 0],
    );
    const unique = [...new Set(incorrect)];
    for (let i = 0; i < unique.length; i++) {
      const incorrectChar = unique[i];
      if (!letters.includes(incorrectChar)) {
        continue;
      }
      const num_time = count(incorrect.toString(), unique[i]);
      const appears = count(text, unique[i]);
      const acc = appears - num_time >= 0 ? (appears - num_time) / appears : 0;
      incorrect_info[incorrectChar] = num_time;
      acc_info[incorrectChar] = acc;
    }
    const uniqueChars = [...new Set(text)];
    for (let i = 0; i < uniqueChars.length; i++) {
      const correct_char = uniqueChars[i];
      if (!letters.includes(correct_char)) {
        continue;
      }
      const num_correct = count(text, uniqueChars[i]);
      correct_info[correct_char] = num_correct;
    }
    const token = localStorage.getItem('jwt');
    const email = localStorage.getItem('email');
    const game_info = {
      email,
      token,
      wpm,
      total_accuracy: accuracy,
      correct_characters: correct_info,
      incorrect_characters: incorrect_info,
      character_accuracy: acc_info,
      character_time,
    };
    console.log(game_info);
    submitTest(game_info, email, token);
  }

  useKeyPress((key) => {
    if (!startTime) {
      setStartTime(currentTime());
    }

    let updatedTypedChar = typedChar;
    let updatedToTypeChar = toTypeChar;

    if (updatedToTypeChar === '') {
      console.log('OVER');
      endGame();
    }

    if (key === currChar) {
      if (leftPadding.length > 0) {
        setLeftPadding(leftPadding.substring(1));
      }
      updatedTypedChar += currChar;
      setTypedChar(updatedTypedChar);
      setCorrectCount(correctCount + 1);

      setAccuracy(
        ((correctCount * 100) / (errors + correctCount)).toFixed(),
      );

      setCurrChar(toTypeChar.charAt(0));

      updatedToTypeChar = toTypeChar.substring(1);
      // if (updatedToTypeChar.split(' ').length < 10) {
      //   updatedToTypeChar += ' ' + generate();
      // }
      setToTypeChar(updatedToTypeChar);

      if (toTypeChar.charAt(0) === ' ') {
        setWordCount(wordCount + 1);

        const durationInMinutes = (currentTime() - startTime) / 60000.0;

        setWpm(((wordCount + 1) / durationInMinutes).toFixed());
      }
    } else {
      incorrect.push(currChar);
      console.log(incorrect);
      setErrors(errors + 1);
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
    console.log(inputTB);
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
      <Stats wordsperminute={wpm} numerrors={errors} accuracyscore={accuracy} keyset={keyset} />
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
          <div id="words__input">
            <p className="Character">
              <span className="Character-out">{(leftPadding + typedChar).slice(-35)}</span>
              <span className="Character-current">{currChar}</span>
              <span className="Character-in">{toTypeChar.substr(0, 32)}</span>
            </p>
          </div>
        </div>
      </div>
      {/* <input value={input} onChange={onChangeInput} /> */}
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
