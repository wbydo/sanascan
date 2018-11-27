import * as React from "react";
import {connect} from "react-redux";
import {Dispatch} from "redux";

import CharacterBoard from "./CharacterBoard";
import {Action, startIncrement} from "./actions";

interface Props {
  startIncrement: () => void;
}

type MapDispatchToProps = (dispatch: Dispatch<Action>) => Props;

class App extends React.Component<Props, {}> {
  public render() {
    return(
      <div>
        <CharacterBoard />
        <button type="button" onClick={this.handleOnClick}>
          start
        </button>
      </div>
    );
  }

  public handleOnClick = (event: React.MouseEvent): void => {
    return this.props.startIncrement();
  }
}

const mdp: MapDispatchToProps = (dispatch) => {
  return {
    startIncrement: () => dispatch(startIncrement()),
  };
};

export default connect(null, mdp)(App);
