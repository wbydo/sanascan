import { combineReducers } from "redux";

import { Action } from "./actions";
import * as types from "./types";

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
  if (state === undefined) {
    return initialState.isActive;
  }

  if (
      (action.type === types.SET_ACTIVE)
        && action.payload
        && (action.payload.isActive !== undefined)
  ) {
    return action.payload.isActive;
  }

  return state;
};

const scanSpeedReducer = (state: number | undefined, action: Action): number => {
  if (state === undefined) {
    return initialState.scanSpeed;
  }

  if (
      (action.type === types.SET_SCAN_SPEED)
        && action.payload
        && (action.payload.scanSpeed !== undefined)
  ) {
    return action.payload.scanSpeed;
  }

  return state;
};

const idReducer = (state: number | null | undefined, action: Action): number | null => {
  if (state === undefined) {
    return initialState.id;
  }

  if (
      (action.type === types.SET_ID)
      && action.payload
      && (action.payload.id !== undefined)
  ) {
    return action.payload.id;
  }

  return state;
};

const reducer = combineReducers({
  id: idReducer,
  isActive: isActiveReducer,
  scanSpeed: scanSpeedReducer,
});

export default reducer;
