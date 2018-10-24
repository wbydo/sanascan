import * as React from 'react';

import Cell from './Cell'
import * as styles from './Buttons.css';


const labels: string[] = [
  "7", "8", "9", "＋",
  "4", "5", "6", "−",
  "1", "2", "3", "×",
  "0", ".", "=", "÷"
];

export default class Buttons extends React.Component<{}, {}> {
  public render() {
    return(
      <div className={styles.buttons}>
        {labels.map((l) => <Cell label={l} />)}
      </div>
    );
  }
}
