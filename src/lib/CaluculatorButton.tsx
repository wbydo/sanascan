import * as React from 'react';

import * as styles from './CaluculatorButton.css';

interface KeyProps {
  label: string;
}

export default class CaluculatorButton extends React.Component<KeyProps, {}> {
  public render() {
    return(
      <div className={styles.button}>
        <div className={styles.label}>{this.props.label}</div>
      </div>
    );
  }
}
