import { combineReducers } from "redux";

import * as actions from "./actions";
import * as types from "./types";

import { Action as _Action } from "../../util";
type Action = _Action<typeof actions>;

import { RootState } from "../../";

type State = RootState["developerMode"];

const initialState: State = {
  estimator: false,
  isActive: true,
  timer: true,
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

const estimatorActivityReducer = (state: boolean | undefined, action: Action) => {
  if (action.type === types.SET_ESTIMATOR_ACTIVITY) {
    return action.payload.estimatorIsActive;
  }

  if ( state === undefined) {
    return initialState.estimator;
  }

  return state;
};

const timerActivityReducer = (state: boolean | undefined, action: Action) => {
  if (action.type === types.SET_TIMER_ACTIVITY) {
    return action.payload.timerIsActive;
  }

  if ( state === undefined) {
    return initialState.timer;
  }

  return state;
};

export const reducer = combineReducers({
  estimator: estimatorActivityReducer,
  isActive: isActiveReducer,
  timer: timerActivityReducer,
});
