import { Dispatch } from "redux";

import * as actions from "./actions";

import { operations as configWindowOperations } from "./configWindow";
import { actions as configWindowActions } from "./configWindow";

import { actions as estimatorActions } from "./estimator";

import { actions as timerActions } from "./timer";

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

export const doneFetchedId = (dispatch: Dispatch, eid: number) => {
  dispatch(actions.fetchId("done"));
  dispatch(estimatorActions.setId(eid));
};

export const forViews = (dispatch: Dispatch) => {
  return {
    changeDisplayValue: configWindowOperations.setScanSpeed(dispatch),
    configureWindowClose: configWindowClose(dispatch),
    configureWindowOpen: configWindowOpen(dispatch),
    resetEstimator: () => dispatch(actions.reset()),
    sendKey: (key: number) => dispatch(actions.sendKey(key)),
    startFetchEstimatorId: () => dispatch(actions.fetchId("start")),
  };
};
