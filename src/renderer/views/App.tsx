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
}

interface DispatchProps {
  openConfigureWindow: () => void;
  startTimer: () => void;
}

type Props = StateProps & DispatchProps;

class App extends React.Component<Props> {
  public render() {
    return(
      <div id="App" className={styles.app}>
        <CharacterBoard activeColumn={this.props.activeColumn}/>
        {this.props.configureWindowIsActive && <Configure />}
        <button onClick={this.props.openConfigureWindow}>設定</button>
      </div>
    );
  }

  public componentDidMount = () => {
    return this.props.startTimer();
  }
}

export default connect(
  (state: RootState): StateProps => {
    return {
      activeColumn: state.cursol.activeColumn,
      configureWindowIsActive: state.configWindow.isActive,
    };
  },
  (dispatch: Dispatch): DispatchProps => {
    return {
      openConfigureWindow: () => {
        dispatch(configWindowActions.setActive(true));
        dispatch(timerActions.setActive(false));
      },
      startTimer: () => dispatch(startTimer()),
    };
  },
)(App);
