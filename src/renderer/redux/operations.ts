import { Dispatch } from "redux";

import { operations as configWindowOperations } from "./state/configWindow";
import { actions as configWindowActions } from "./state/configWindow";

import { actions as cursolActions } from "./state/cursol";

import { actions as timerActions } from "./state/timer";
import { actions as developerModeActions } from "./state/developerMode";

import { actions as timerEventActions } from "./cross/timerEvent";
import { actions as httpActions } from "./cross/http";

const configWindowOpen = (dispatch: Dispatch) => (scanSpeed: number) => {
  dispatch(timerEventActions.kill());
  dispatch(configWindowActions.setScanSpeed(scanSpeed));
  dispatch(configWindowActions.setActive(true));
};

const configWindowClose = (dispatch: Dispatch) => (lastValue: number) => {
  if (lastValue > 0) {
    dispatch(timerActions.setScanSpeed(lastValue));
  }
  dispatch(configWindowActions.setActive(false));
  dispatch(timerEventActions.start());
};

export const operations = (dispatch: Dispatch) => {
  return {
    changeDisplayValue: configWindowOperations.setScanSpeed(dispatch),
    configureWindowClose: configWindowClose(dispatch),
    configureWindowOpen: configWindowOpen(dispatch),
    developerMode: {
      increment: () => dispatch(cursolActions.increment()),
    },
    resetEstimator: () => dispatch(httpActions.reset()),
    sendKey: (key: number) => dispatch(httpActions.sendKey(key)),
    setCursolDirection: (direction: "column" | "row") => dispatch(cursolActions.setDirection(direction)),
    setCursolMode: (mode: "normal" | "proposal") => dispatch(cursolActions.setMode(mode)),
    setDeveloperModeActivity: (isActive: boolean) => dispatch(developerModeActions.setActive(isActive)),
    startFetchEstimatorId: () => dispatch(httpActions.fetchId("start")),
  };
};
