import * as React from 'react';
import * as ReactDOM from 'react-dom';

import CaluculatorButton from './lib/CaluculatorButton'

const labels: string[] = [
  "7", "8", "9",
  "4", "5", "6",
  "1", "2", "3",
  "0", ".", "="
];

ReactDOM.render(
  <div id="frame">
    <h1>Caluculator</h1>

    <div id="caluculator">
      <div id="output">
        <div id="output-num">1,000</div>
      </div>
      <div id="buttons">
        {labels.map((l) => <CaluculatorButton label={l} />)}
      </div>
    </div>
  </div>,
  document.getElementById('root')
);
