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
        <input
            type="checkbox"
            checked={this.props.developerMode.estimator}
            onClick={this.toggleEstimatorActivity}
            />
        ESTIMATOR

        <input
            type="checkbox"
            checked={this.props.developerMode.timer}
            onClick={this.toggleTimerActivity}
            />
        Timer
        {!this.props.developerMode.timer &&
          <button
              onClick={() => this.props.dispatch.developerMode.increment()}
              >
            INCREMENT
          </button>
        }

        <Selector
            state={this.props.cursol.direction}
            dispatch={this.props.dispatch.setCursolDirection}
            labels={["column", "row"]}
            />
        <button><del>CLICK</del></button>
      </span>
    );
  }

  private toggleTimerActivity = () => {
    const currentActivity = this.props.developerMode.timer;
    this.props.dispatch.developerMode.timer.toggleActivity(currentActivity);
  }

  private toggleEstimatorActivity = () => {
    const currentActivity = this.props.developerMode.estimator;
    this.props.dispatch.developerMode.estimator.toggle(currentActivity);
  }
}

export default connect(
  (state: RootState) => state,
  (dispatch: Dispatch) => ({ dispatch: operations(dispatch) }),
)(DeveloperControl);
