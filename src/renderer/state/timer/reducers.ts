import { combineReducers } from "redux";

import { Action } from "./actions";
import * as types from "./types";

interface RootState {
  isActive: boolean;
  scanSpeed: number;
}

const initialState: RootState = {
  isActive: false,
  scanSpeed: 500,
};

const isActiveReducer = (state: boolean | undefined, action: Action): boolean => {
  if (state === undefined) {
    return initialState.isActive;
  }

  if (types.SET_ACTIVE && action.payload && (action.payload.isActive !== undefined)) {
    return action.payload.isActive;
  }

  return state;
};

const scanSpeedReducer = (state: number | undefined, action: Action): number => {
  if (state === undefined) {
    return initialState.scanSpeed;
  }

  if (types.SET_SCAN_SPEED && action.payload && action.payload.scanSpeed) {
    return action.payload.scanSpeed;
  }

  return state;
};

const reducer = combineReducers({
  isActive: isActiveReducer,
  scanSpeed: scanSpeedReducer,
});

export default reducer;
