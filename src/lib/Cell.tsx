import * as React from 'react';

import * as styles from './Cell.css';

interface KeyProps {
  label: string;
  output: boolean;
}

export default class Cell extends React.Component<KeyProps, {}> {
  public render() {
    const className:string  = this.props.output ? styles.outputFrame : styles.frame;

    return(
      <div className={className}>
        <div className={styles.label}>{this.props.label}</div>
      </div>
    );
  }
}
