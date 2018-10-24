import * as React from 'react';

import * as styles from './Cell.css';

interface KeyProps {
  label: string;
}

export default class Cell extends React.Component<KeyProps, {}> {
  public render() {
    return(
      <div className={styles.frame}>
        <div className={styles.label}>{this.props.label}</div>
      </div>
    );
  }
}
