import React, { useRef, useState, useEffect } from 'react';
import Keyboard from 'react-simple-keyboard';
import 'react-simple-keyboard/build/css/index.css';
import { Button } from '@material-ui/core';
import useKeyPress from '../customHooks/useKeyPress';
import 'font-awesome/css/font-awesome.min.css';
import '../styles/KeyboardComplete.scss';
import '../styles/App.scss';
import Stats from './Stats';
import Loading from './Loading';

const incorrect = [];

function KeyboardComplete() {
  // const text = 'to tar it or too it are trio oar air ariot ear';

  const [loading, setLoading] = useState(true);

  const token = localStorage.getItem('jwt');
  const email = localStorage.getItem('email');

  if (token === null || email === null) {
    console.log('Not signed in');
    window.location.href = '/login';
  }

  const [text, setText] = useState('');
  const [mastery, setMastery] = useState(0);
  const [masteredChars, setMasteredChars] = useState({});
  const [unlockedChars, setUnlockedChars] = useState({});
  const [notMastered, setNotMastered] = useState([]);
  const [currKey, setCurrKey] = useState('');

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

  const [errors, setErrors] = useState(0);
  const [correctCount, setCorrectCount] = useState(0);

  const [accuracy, setAccuracy] = useState(0);

  const [gameOver, setGameOver] = useState(false);
  const [gameState, setGameState] = useState({});

  // const keyset = ['E', 'A', 'R', 'I', 'O', 'T'];
  const [keyset, setKeyset] = useState(['E', 'A']);

  const count = (str, c) => {
    let result = 0;
    let i = 0;
    for (i; i < str.length; i++) if (str[i] === c) result++;
    return result;
  };

  function getKeyByValue(object, value) {
    return Object.keys(object).find((key) => object[key] === value);
  }

  useEffect(() => {
    setTypedChar('');
    setCurrChar(text.charAt(0));
    setToTypeChar(text.substring(1));
    incorrect.length = 0;
    setCorrectCount(0);
    setAccuracy(0);
    // const uniqueKeyset = String.prototype.concat(...new Set(text));
    // const newKeyset = uniqueKeyset.replace(/\s/g, '');
    // console.log(newKeyset);
    const mchars = Object.keys(masteredChars).filter((k) => masteredChars[k] === true);
    const uchars = Object.keys(unlockedChars).filter((k) => unlockedChars[k] === true);
    const uppercased_m = mchars.map((key) => key.toUpperCase());
    const uppercased_u = uchars.map((key) => key.toUpperCase());
    console.log('MASTER: ', uppercased_m);
    console.log('UNLOCK: ', uppercased_u);
    const difference = uppercased_u.filter((x) => !uppercased_m.includes(x));
    console.log('DIFF: ', difference);
    const curr = difference[difference.length - 1];
    console.log('CURR:', curr);
    difference.pop();
    setNotMastered(difference);
    setCurrKey(curr);
    setKeyset(uppercased_m);
    setLoading(false);
  }, [text]);

  useEffect(() => {
    generateTest();
  }, []);

  function generateTest() {
    setLoading(true);
    const url = '/generate_text?';
    fetch(`${url
    }&token=${
      encodeURIComponent(token)
    }&email=${
      encodeURIComponent(email)}`, {
      method: 'GET',
      headers: {
        'Content-type': 'application/json',
        'Accept': 'application/json',
      },
    }).then((res) => res.json()).then(
      (res) => {
        console.log('Res: ', res);
        const str = JSON.stringify(res);
        const newText = res.text;
        const newMaster = res.master;
        const masterChars = res.mastered_characters;
        const unlockChars = res.unlocked_characters;
        console.log('Text: ', newText);
        console.log('Master: ', newMaster);
        console.log('Mastered: ', masterChars);
        setMastery(newMaster);
        setMasteredChars(masterChars);
        setUnlockedChars(unlockChars);
        // const tests = Object.keys(masterChars).filter((k) => masterChars[k] === 0);
        // console.log('KEYS: ', tests);
        // setKeyset(tests);
        // setKeyset(['A', 'B']);
        setText(newText);
      },
    );
  }

  function submitTest(info) {
    fetch('/submit', {
      method: 'POST',
      headers: {
        'Content-type': 'application/json',
        'Accept': 'application/json',
      },
      body: JSON.stringify(info),
    }).then((res) => res.json()).then(
      (res) => {
        console.log('Res: ', res);
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
      if (!letters.includes(incorrectChar) || incorrectChar === '') {
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
    submitTest(game_info);
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

  return (
    <div className="keyboard">
      {loading === true ? (<Loading />) : (
        <div>
          <Stats
            wordsperminute={wpm}
            numerrors={errors}
            accuracyscore={accuracy}
            key={keyset}
            keyset={keyset}
            notmastered={notMastered}
            current={currKey}
          />
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
              <div id="words__input">
                <p className="Character">
                  <span className="Character-out">{(leftPadding + typedChar).slice(-35)}</span>
                  <span className="Character-current">{currChar}</span>
                  <span className="Character-in">{toTypeChar.substr(0, 32)}</span>
                </p>
              </div>
            </div>
          </div>
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
      )}

    </div>
  );
}

export default KeyboardComplete;
