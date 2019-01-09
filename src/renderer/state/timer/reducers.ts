import { combineReducers } from "redux";

import * as actions from "./actions";
import * as types from "./types";

import { Action as _Action } from "../util";

export type Action = _Action<typeof actions>;

interface RootState {
  isActive: boolean;
  scanSpeed: number;
  id: number | null;
}

const initialState: RootState = {
  id: null,
  isActive: false,
  scanSpeed: 500,
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
  if (action.type === types.SET_SCAN_SPEED) {
    return action.payload.scanSpeed;
  }

  if (state === undefined) {
    return initialState.scanSpeed;
  }

  return state;
};

const idReducer = (state: number | null | undefined, action: Action): number | null => {
  if (action.type === types.SET_ID) {
    return action.payload.id;
  }

  if (state === undefined) {
    return initialState.id;
  }

  return state;
};

const reducer = combineReducers({
  id: idReducer,
  isActive: isActiveReducer,
  scanSpeed: scanSpeedReducer,
});

export default reducer;
