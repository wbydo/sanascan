import * as React from 'react';
import * as ReactDOM from 'react-dom';

import Buttons from './lib/Buttons'

ReactDOM.render(
  <div id="frame">
    <h1>Caluculator</h1>

    <div id="caluculator">
      <div id="output">
        <div id="output-num">1,000</div>
      </div>
      <Buttons />
    </div>
  </div>,
  document.getElementById('root')
);
