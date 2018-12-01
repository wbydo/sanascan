import { combineReducers } from "redux";

import { Action } from "./actions";
import * as types from "./types";

interface RootState {
  isActive: boolean;
}

const initialState: RootState = {
  isActive: false,
};

const isActiveReducer = (state: boolean | undefined, action: Action): boolean => {
  if (state === undefined) {
    return initialState.isActive;
  }

  if (action.type === types.SET_ACTIVE && action.payload) {
    return action.payload.isActive;
  }
  return state;
};

const reducer = combineReducers({
  isActive: isActiveReducer,
});

export default reducer;
