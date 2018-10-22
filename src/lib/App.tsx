import * as React from 'react';

import OutputArea from './OutputArea'
import Buttons from './Buttons'

import * as styles from './App.css'

export default class App extends React.Component<{}, {}> {
  public render() {
    return(
      <div className={styles.frame}>
        <div className={styles.inner}>
          <OutputArea />
          <Buttons />
        </div>
      </div>
    );
  }
}
