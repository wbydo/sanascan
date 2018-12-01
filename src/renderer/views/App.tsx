import * as React from "react";
import {connect} from "react-redux";
import {Dispatch} from "redux";

import CharacterBoard from "./CharacterBoard";
import { start as startTimer } from "../state/timer/actions";
import Configure from "./Configure";
import * as styles from "./App.css";

import { RootState } from "../state/index";
import * as Actions from "../state/actions";

interface StateProps {
  configureWindowIsActive: boolean;
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
        <CharacterBoard />
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
      configureWindowIsActive: state.window.configure.isActive,
    };
  },
  (dispatch: Dispatch): DispatchProps => {
    return {
      openConfigureWindow: () => dispatch(Actions.activateConfigure()),
      startTimer: () => dispatch(startTimer()),
    };
  },
)(App);
