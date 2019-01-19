import { Dispatch } from "redux";

import { actions as timerActions } from "../timer";
import { actions as httpActions } from "../http";

import { actions as developerModeActions } from "../../state/developerMode";
import { actions as cursolActions } from "../../state/cursol";

export const toggleActivity = (dispatch: Dispatch) => (currentActivity: boolean, timerActivity: boolean) => {
  dispatch(developerModeActions.setActive(!currentActivity));
  dispatch(timerActions.kill());

  if (currentActivity) {
    dispatch(httpActions.fetchId("start"));
    return;
  }

  if (timerActivity) {
    dispatch(timerActions.start());
    return;
  }
};

export const toggleTimerActivity = (dispatch: Dispatch) => (currentActivity: boolean) => {
  dispatch(developerModeActions.setTimerActivity(!currentActivity));

  if (currentActivity) {
    dispatch(timerActions.kill());
  } else {
    dispatch(timerActions.start());
  }
};

export const toggleEstimatorActivity = (dispatch: Dispatch) => (currentActivity: boolean) => {
  dispatch(developerModeActions.setEstimatorActivity(!currentActivity));
  dispatch(cursolActions.reset());
  dispatch(httpActions.reset());
};
