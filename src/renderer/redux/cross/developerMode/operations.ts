import { Dispatch } from "redux";

import { actions as timerActions } from "../timer";
import { actions as httpActions } from "../http";

import { actions as developerModeActions } from "../../state/developerMode";

export const changeMode = (dispatch: Dispatch) => (currentActivity: boolean, timerActivity: boolean) => {
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
