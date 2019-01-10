import { Dispatch } from "redux";

import { operations as configWindowOperations } from "./state/configWindow";
import { actions as configWindowActions } from "./state/configWindow";
import { actions as timerActions } from "./state/timer";

import { actions as httpActions } from "./cross/http";

const configWindowOpen = (dispatch: Dispatch) => (scanSpeed: number) => {
  dispatch(timerActions.setActive(false));
  dispatch(configWindowActions.setScanSpeed(scanSpeed));
  dispatch(configWindowActions.setActive(true));
};

const configWindowClose = (dispatch: Dispatch) => (lastValue: number) => {
  if (lastValue > 0) {
    dispatch(timerActions.setScanSpeed(lastValue));
  }
  dispatch(configWindowActions.setActive(false));
  dispatch(timerActions.start());
};

export const operations = (dispatch: Dispatch) => {
  return {
    changeDisplayValue: configWindowOperations.setScanSpeed(dispatch),
    configureWindowClose: configWindowClose(dispatch),
    configureWindowOpen: configWindowOpen(dispatch),
    resetEstimator: () => dispatch(httpActions.reset()),
    sendKey: (key: number) => dispatch(httpActions.sendKey(key)),
    startFetchEstimatorId: () => dispatch(httpActions.fetchId("start")),
  };
};
