import { combineReducers } from "redux";

import * as actions from "./actions";
import * as types from "./types";

import { Action as _Action } from "../util";
export type Action = _Action<typeof actions>;

interface RootState {
  isActive: boolean;
  scanSpeed: number;
}

const initialState: RootState = {
  isActive: false,
  scanSpeed: 0,
};

const isActiveReducer = (state: boolean | undefined, action: Action): boolean => {
  if (action.type === types.SET_ACTIVE) {
    return action.payload.isActive;
  }

  if (state === undefined) {
    return initialState.isActive;
  }

  return state;
};

const scanSpeedReducer = (state: number | undefined, action: Action): number => {
  if (state === undefined) {
    return initialState.scanSpeed;
  }

  if (action.type === types.SET_SCAN_SPEED) {
    return action.payload.scanSpeed;
  }
  return state;
};

export const reducer = combineReducers({
  isActive: isActiveReducer,
  scanSpeed: scanSpeedReducer,
});
