import { combineReducers } from "redux";

import * as actions from "./actions";
import * as types from "./types";

import { Action as _Action } from "../../util";
type Action = _Action<typeof actions>;

import { RootState } from "../../";

type State = RootState["developerMode"];

const initialState: State = {
  estimatorIsActive: false,
  isActive: true,
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
    return initialState.estimatorIsActive;
  }

  return state;
};

export const reducer = combineReducers({
  estimatorIsActive: estimatorActivityReducer,
  isActive: isActiveReducer,
});
