import * as React from "react";
import {connect} from "react-redux";
import {Dispatch} from "redux";

import { RootState, operations, selectors } from "../../redux";

type Props = ReturnType<typeof selectors> & ReturnType<typeof operations>;

export class DeveloperControl extends React.Component<Props> {
  public render() {
    return(
      <span>
        <button
            onClick={() => this.props.startFetchEstimatorId()}
            >
          FETCH
        </button>
        <button
            onClick={() => this.props.developerMode.increment()}
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
  (state: RootState) => selectors(state),
  (dispatch: Dispatch) => operations(dispatch),
)(DeveloperControl);
