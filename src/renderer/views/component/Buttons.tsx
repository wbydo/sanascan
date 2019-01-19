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
              dispatch={this.props.dispatch.cursol.changeMode}
              labels={["normal", "proposal"]}
              />
        </div>
        <div>
          <input
              type="checkbox"
              checked={this.props.developerMode.isActive}
              onClick={this.changeActivity}
              />
          DeveloperMode
          {this.props.developerMode.isActive && <DeveloperControl />}
        </div>
      </div>
    );
  }

  private configureWindowOpen = () => {
    this.props.dispatch.configWindow.open(this.props.timer.scanSpeed);
  }

  private changeActivity = () => {
    this.props.dispatch.developerMode.changeMode(
      this.props.developerMode.isActive,
      this.props.developerMode.timer,
    );
  }
}
