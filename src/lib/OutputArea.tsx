import * as React from 'react';

import * as styles from './OutputArea.css';

export default class OutputArea extends React.Component<{}, {}> {
  public render() {
    return(
      <div className={styles.area}>
        <div className={styles.label}>1,000</div>
      </div>
    );
  }
}
