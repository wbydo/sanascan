import * as React from "react";

import * as styles from "./Buttons.css";

import { StateProps as AppStateProps } from "../App";
import { DispatchProps as AppDispatchProps } from "../App";
import { Props as _Props } from "../util";

import DeveloperControl from "./DeveloperControl";

type StateProps = Pick<
  AppStateProps,
  "timerScanSpeed" | "developerMode"
>;

type DispatchProps = Pick<
  AppDispatchProps,
  "setDeveloperModeActivity" | "configureWindowOpen" | "resetEstimator"
>;

type Props = _Props<StateProps, DispatchProps>;

export default class Buttons extends React.Component<Props> {
  public render() {
    return(
      <div id="buttons" className={styles.container}>
        <div>
          <button onClick={this.configureWindowOpen}>設定</button>
          <button onClick={this.props.dispatch.resetEstimator}>はじめから</button>
        </div>
        <div>
          <input
              type="checkbox"
              checked={this.props.developerMode}
              onClick={this.handleClickDeveloperMode}
              />
          DeveloperMode
          {this.props.developerMode && <DeveloperControl />}
        </div>
      </div>
    );
  }

  private configureWindowOpen = () => {
    this.props.dispatch.configureWindowOpen(this.props.timerScanSpeed);
  }

  private handleClickDeveloperMode = () => {
    this.props.dispatch.setDeveloperModeActivity(!this.props.developerMode);
  }
}
