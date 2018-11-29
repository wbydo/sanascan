import React from "react";
import ReactDOM from "react-dom";

import * as styles from "./modal.css";

export class Modal extends React.Component {
  public render() {
    return(
      <div className={styles.frame}>
        <div className={styles.content}>
          <h1>もーだるういんどう</h1>
          <button>Off</button>
        </div>
      </div>
    );
  }
}
