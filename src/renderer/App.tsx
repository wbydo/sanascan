import * as React from "react";
import {connect} from "react-redux";
import {Dispatch} from "redux";

import CharacterBoard from "./CharacterBoard";
import {Action, increment, asyncIncrement} from "./actions";

interface Props {
  increment: () => void;
  asyncIncrement: () => void;
}

type MapDispatchToProps = (dispatch: Dispatch<Action>) => Props;

class App extends React.Component<Props, {}> {
  public render() {
    return(
      <div>
        <CharacterBoard />
        <button type="button" onClick={this.handleOnClick}>
          sync
        </button>
        <button type="button" onClick={this.handleAsync}>
          async
        </button>
      </div>
    );
  }

  public handleOnClick = (event: React.MouseEvent): void => {
    return this.props.increment();
  }

  public handleAsync = (event: React.MouseEvent): void => {
    return this.props.asyncIncrement();
  }
}

const mdp: MapDispatchToProps = (dispatch) => {
  return {
    asyncIncrement: () => dispatch(asyncIncrement()),
    increment: () => dispatch(increment()),
  };
};

export default connect(null, mdp)(App);
