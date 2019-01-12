import * as React from "react";
import {connect} from "react-redux";
import {Dispatch} from "redux";

import { Props as _Props } from "../util";

import { RootState, operations, selectors } from "../../redux";

export type StateProps = ReturnType<typeof selectors>;
export type DispatchProps = ReturnType<typeof operations>;

type Props = _Props<StateProps, DispatchProps>;

export class DeveloperControl extends React.Component<Props> {
  public render() {
    return(
      <span>
        <select value={this.props.cursolMode} onChange={this.changeMode}>
          <option value="normal">Normal</option>
          <option value="proposal">Proposal</option>
        </select>
        <select value={this.props.cursolDirection} onChange={this.changeDirection}>
          <option value="column">column</option>
          <option value="row">row</option>
        </select>
        <button
            onClick={() => this.props.dispatch.startFetchEstimatorId()}
            >
          FETCH
        </button>
        <button
            onClick={() => this.props.dispatch.developerMode.increment()}
            >
          INCREMENT
        </button>
        <button><del>START (WITHOUT ESTIMATOR)</del></button>
        <button><del>CLICK</del></button>
      </span>
    );
  }

  private changeMode = (event: React.FormEvent<HTMLSelectElement>) => {
    const target = event.target as HTMLSelectElement;
    this.props.dispatch.setCursolMode(target.value as "normal" | "proposal");
  }

  private changeDirection = (event: React.FormEvent<HTMLSelectElement>) => {
    const target = event.target as HTMLSelectElement;
    this.props.dispatch.setCursolDirection(target.value as "column" | "row");
  }
}

export default connect(
  (state: RootState) => selectors(state),
  (dispatch: Dispatch) => ({ dispatch: operations(dispatch) }),
)(DeveloperControl);
