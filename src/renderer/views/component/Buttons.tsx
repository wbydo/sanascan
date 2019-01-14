import * as React from "react";

import * as styles from "./Buttons.css";
import Selector from "./Selector";

import { Props } from "../App";
import { Props as _Props } from "../util";

import DeveloperControl from "../container/DeveloperControl";

export default class Buttons extends React.Component<Props> {
  public render() {
    return(
      <div id="buttons" className={styles.container}>
        <div>
          <button onClick={this.configureWindowOpen}>設定</button>
          <button onClick={this.props.dispatch.resetEstimator}>はじめから</button>
          <Selector
              state={this.props.cursol.mode}
              dispatch={this.props.dispatch.setCursolMode}
              labels={["normal", "proposal"]}
              />
        </div>
        <div>
          <input
              type="checkbox"
              checked={this.props.developerMode.isActive}
              onClick={this.handleClickDeveloperMode}
              />
          DeveloperMode
          {this.props.developerMode.isActive && <DeveloperControl />}
        </div>
      </div>
    );
  }

  private configureWindowOpen = () => {
    this.props.dispatch.configureWindowOpen(this.props.timer.scanSpeed);
  }

  private handleClickDeveloperMode = () => {
    this.props.dispatch.setDeveloperModeActivity(!this.props.developerMode.isActive);
  }
}
