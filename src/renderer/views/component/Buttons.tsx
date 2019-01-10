import * as React from "react";

import * as styles from "./Buttons.css";

interface StateProps {
  timerScanSpeed: number;
  developerMode: boolean;
}

interface DispatchProps {
  setDeveloperModeActivity: (isActive: boolean) => void;
  configureWindowOpen: (scanSpeed: number) => void;
  resetEstimator: () => void;
}

export type Props = StateProps & DispatchProps;

export default class Buttons extends React.Component<Props> {
  public render() {
    return(
      <div id="buttons" className={styles.container}>
        <div>
          <button onClick={this.configureWindowOpen}>設定</button>
          <button onClick={this.props.resetEstimator}>はじめから</button>
        </div>
        <div>
          <input
            type="checkbox"
            checked={this.props.developerMode}
            onClick={this.handleClickDeveloperMode}
          />
          DeveloperMode
          <button>INC</button>
          <button>CLK</button>
        </div>
      </div>
    );
  }

  private configureWindowOpen = () => {
    this.props.configureWindowOpen(this.props.timerScanSpeed);
  }

  private handleClickDeveloperMode = () => {
    this.props.setDeveloperModeActivity(!this.props.developerMode);
  }
}
