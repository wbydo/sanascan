import { Dispatch } from "redux";

import { operations as configWindowOperations } from "./state/configWindow";
import { actions as configWindowActions } from "./state/configWindow";

import { actions as cursolActions } from "./state/cursol";
import { actions as timerActions } from "./state/timer";

import { operations as cursolOperations } from "./cross/cursol";
import { actions as crossTimerActions } from "./cross/timer";
import { actions as httpActions } from "./cross/http";
import { operations as clickOperations } from "./cross/click";

import { operations as developerModeOperations } from "./cross/developerMode";

const configWindowOpen = (dispatch: Dispatch) => (scanSpeed: number) => {
  dispatch(crossTimerActions.kill());
  dispatch(configWindowActions.setScanSpeed(scanSpeed));
  dispatch(configWindowActions.setActive(true));
};

const configWindowClose = (dispatch: Dispatch) => (lastValue: number) => {
  if (lastValue > 0) {
    dispatch(timerActions.setScanSpeed(lastValue));
  }
  dispatch(configWindowActions.setActive(false));
  dispatch(crossTimerActions.start());
};

export const operations = (dispatch: Dispatch) => {
  return {
    changeDisplayValue: configWindowOperations.setScanSpeed(dispatch),
    click: clickOperations.click(dispatch),
    configWindow: {
      close: configWindowClose(dispatch),
      open: configWindowOpen(dispatch),
    },
    cursol: {
      changeMode: cursolOperations.changeMode(dispatch),
    },
    developerMode: {
      estimator: {
        toggle: developerModeOperations.toggleEstimatorActivity(dispatch),
      },
      increment: () => dispatch(cursolActions.increment()),
      startTimer: () => dispatch(crossTimerActions.start()),
      timer: {
        toggleActivity: developerModeOperations.toggleTimerActivity(dispatch),
      },
      toggleActivity: developerModeOperations.toggleActivity(dispatch),
    },
    resetEstimator: () => dispatch(httpActions.reset()),
    setCursolDirection: (direction: "column" | "row") => dispatch(cursolActions.setDirection(direction)),
    startFetchEstimatorId: () => dispatch(httpActions.fetchId("start")),
  };
};
