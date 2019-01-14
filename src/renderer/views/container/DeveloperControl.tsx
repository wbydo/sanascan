import * as React from "react";
import {connect} from "react-redux";
import {Dispatch} from "redux";

import Selector from "../component/Selector";
import { Props as _Props } from "../util";

import { RootState, operations } from "../../redux";

export type StateProps = RootState;
export type DispatchProps = ReturnType<typeof operations>;

type Props = _Props<StateProps, DispatchProps>;

export class DeveloperControl extends React.Component<Props> {
  public render() {
    return(
      <span>
        <Selector
            state={this.props.cursol.direction}
            dispatch={this.props.dispatch.setCursolDirection}
            labels={["column", "row"]}
            />

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
}

export default connect(
  (state: RootState) => state,
  (dispatch: Dispatch) => ({ dispatch: operations(dispatch) }),
)(DeveloperControl);
