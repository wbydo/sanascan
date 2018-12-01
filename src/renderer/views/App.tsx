import * as React from "react";
import {connect} from "react-redux";
import {Dispatch} from "redux";

import CharacterBoard from "./component/CharacterBoard";
import { start as startTimer } from "../state/timer/actions";
import Configure from "./Configure";
import * as styles from "./App.css";

import { RootState } from "../state/";

import { configWindowActions } from "../state/configWindow/index";
import { timerActions } from "../state/timer/index";

interface StateProps {
  configureWindowIsActive: boolean;
  activeColumn: number;
  timerScanSpeed: number;
}

interface DispatchProps {
  openConfigureWindow: (scanSpeed: number) => void;
  startTimer: () => void;
}

type Props = StateProps & DispatchProps;

class App extends React.Component<Props> {
  public render() {
    return(
      <div id="App" className={styles.app}>
        <CharacterBoard activeColumn={this.props.activeColumn}/>
        {this.props.configureWindowIsActive && <Configure />}
        <button onClick={this.openConfigureWindow}>設定</button>
      </div>
    );
  }

  public componentDidMount = () => {
    return this.props.startTimer();
  }

  private openConfigureWindow = () => {
    this.props.openConfigureWindow(this.props.timerScanSpeed);
  }
}

export default connect(
  (state: RootState): StateProps => {
    return {
      activeColumn: state.cursol.activeColumn,
      configureWindowIsActive: state.configWindow.isActive,
      timerScanSpeed: state.timer.scanSpeed,
    };
  },
  (dispatch: Dispatch): DispatchProps => {
    return {
      openConfigureWindow: (scanSpeed: number) => {
        dispatch(timerActions.setActive(false));
        dispatch(configWindowActions.setScanSpeed(scanSpeed));
        dispatch(configWindowActions.setActive(true));
      },
      startTimer: () => dispatch(startTimer()),
    };
  },
)(App);
