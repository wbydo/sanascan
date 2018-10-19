import * as React from 'react';
import * as ReactDOM from 'react-dom';

import OutputArea from './lib/OutputArea'
import Buttons from './lib/Buttons'

ReactDOM.render(
  <div id="frame">
    <h1>Caluculator</h1>

    <div id="caluculator">
      <OutputArea />
      <Buttons />
    </div>
  </div>,
  document.getElementById('root')
);
