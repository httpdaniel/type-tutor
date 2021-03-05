/*eslint-disable*/

import './SampleWords.css';

function SampleWords(props) {
  const { wordList, currentWord, letterCorrect, wordCorrect } = props;
  console.log(wordCorrect);
  return (
    <div className="SampleWords">
      {wordList.map((word, index) => {
        if (word === currentWord && letterCorrect === true) {
          return (
            <span key={index} className="active-word-correct">
              {word}
            </span>
          );
        }
        if (word === currentWord && letterCorrect === false) {
          return (
            <span key={index} className="active-word-wrong">
              {word}
            </span>
          );
        }
        return <span key={index}>{word}</span>;
      })}
    </div>
  );
}
export default SampleWords;
