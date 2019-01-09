import {Dispatch} from "redux";

import * as actions from "./actions";

import { actions as timerActions } from "../timer";

export const windowOpen = (dispatch: Dispatch) => (scanSpeed: number) => {
  dispatch(timerActions.setActive(false));
  dispatch(actions.setScanSpeed(scanSpeed));
  dispatch(actions.setActive(true));
};

export const windowClose = (dispatch: Dispatch) => (lastValue: number) => {
  if (lastValue > 0) {
    dispatch(timerActions.setScanSpeed(lastValue));
  }
  dispatch(actions.setActive(false));
  dispatch(timerActions.start());
};

export const setScanSpeed = (dispatch: Dispatch) => (scanSpeed: number) => {
  dispatch(actions.setScanSpeed(scanSpeed));
};
