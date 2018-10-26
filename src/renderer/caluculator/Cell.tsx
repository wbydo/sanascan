import * as React from "react";

import * as styles from "./Cell.css";

interface KeyProps {
  label: string;
  output: boolean;
  input?: (value: number) => void;
}

export default class Cell extends React.Component<KeyProps, {}> {
  public render() {
    const className: string = this.props.output ? styles.outputFrame : styles.frame;

    return(
      <div className={className} onClick={this.hundleOnClick}>
        <div className={styles.label}>{this.props.label}</div>
      </div>
    );
  }

  public hundleOnClick = (event: React.MouseEvent<HTMLDivElement>): void => {
    const n: number = parseInt(this.props.label, 10);
    if (this.props.input){
      this.props.input(n);
    }
  }
}
