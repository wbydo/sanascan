import React from "react";
import ReactDOM from "react-dom";

import * as styles from "./Configure.css";

export class Configure extends React.Component {
  public render() {
    return(
      <div id="Configure" className={styles.frame}>
        <div className={styles.content}>
          <h1>もーだるういんどう</h1>
          <button>Off</button>
        </div>
      </div>
    );
  }
}
