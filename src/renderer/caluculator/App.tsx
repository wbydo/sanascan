import * as React from "react";
import {connect} from "react-redux";
import {Dispatch} from "redux";

import Cell from "./Cell";
import {CaluculatorState} from "./reducers";
import {CaluculatorAction, ActionDispatcher} from "./actions";

import * as styles from "./App.css";

const labels: string[] = [
  "7", "8", "9", "＋",
  "4", "5", "6", "−",
  "1", "2", "3", "×",
  "0", ".", "=", "÷",
];

interface Props {
  value: number;
  actions: ActionDispatcher;
}

class App extends React.Component<Props, {}> {
  public render() {
    return(
      <div className={styles.frame}>
        <div className={styles.inner}>
          <Cell label={this.props.value.toString()} output={true}/>
          <Cell label={"C"} output={false}/>
          {labels.map((l) => <Cell label={l} output={false}/>)}
        </div>
      </div>
    );
  }
}

export default connect(
  (state: CaluculatorState) => ({value: state.display}),
  (dispatch: Dispatch<CaluculatorAction>) => ({actions: new ActionDispatcher(dispatch)}),
)(App);
