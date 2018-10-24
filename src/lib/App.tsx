import * as React from 'react';

import Cell from './Cell'

import * as styles from './App.css'

const labels: string[] = [
  "7", "8", "9", "＋",
  "4", "5", "6", "−",
  "1", "2", "3", "×",
  "0", ".", "=", "÷"
];

export default class App extends React.Component<{}, {}> {
  public render() {
    return(
      <div className={styles.frame}>
        <div className={styles.inner}>
          {labels.map((l) => <Cell label={l} />)}
        </div>
      </div>
    );
  }
}
