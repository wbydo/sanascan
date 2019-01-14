import { combineReducers } from "redux";

import * as actions from "./actions";
import * as types from "./types";

import { RootState } from "../../";
import { Action as _Action } from "../../util";
export type Action = _Action<typeof actions>;

type State = RootState["timer"];

const initialState: State = {
  isActive: false,
  scanSpeed: 500,
};

const isActiveReducer = (state: boolean | undefined, action: Action) => {
  if (action.type === types.SET_ACTIVE) {
    return action.payload.isActive;
  }

  if ( state === undefined) {
    return initialState.isActive;
  }

  return state;
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
  isActive: isActiveReducer,
  scanSpeed: scanSpeedReducer,
});
