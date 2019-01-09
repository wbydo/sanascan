import {Dispatch} from "redux";

import * as actions from "./actions";

import { actions as timerActions } from "../timer";

export const windowOpen = (dispatch: Dispatch) => (scanSpeed: number) => {
  dispatch(timerActions.setActive(false));
  dispatch(actions.setScanSpeed(scanSpeed));
  dispatch(actions.setActive(true));
};
