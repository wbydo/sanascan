import React from "react";
import ReactDOM from "react-dom";

import * as styles from "./modal.css";

export class Modal extends React.Component {
  public render() {
    return(
      ReactDOM.createPortal(
        <div className={styles.frame}>
          <div className={styles.content}>
            <h1>もーだるういんどう</h1>
            <button>Off</button>
          </div>
        </div>,
        document.getElementById("root") as HTMLElement,
      )
    );
  }
}
