import { combineReducers } from "redux";

import * as actions from "./actions";
import * as types from "./types";

import { Action as _Action } from "../../util";

export type Action = _Action<typeof actions>;

interface RootState {
  scanSpeed: number;
}

const initialState: RootState = {
  scanSpeed: 500,
};

const scanSpeedReducer = (state: number | undefined, action: Action): number => {
  if (action.type === types.SET_SCAN_SPEED) {
    return action.payload.scanSpeed;
  }

  if (state === undefined) {
    return initialState.scanSpeed;
  }

  return state;
};

export const reducer = combineReducers({
  scanSpeed: scanSpeedReducer,
});
