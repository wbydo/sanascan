import { combineReducers } from "redux";

import * as actions from "./actions";
import * as types from "./types";

import SanaScanError from "../../error";

import { Action as _Action } from "../util";
export type Action = _Action<typeof actions>;

interface RootState {
  id: number | null;
  result: string;
}

const initialState: RootState = {
  id: null,
  result: "",
};

const setId = (_: number | null | undefined, action: Action) => {
  if (action.type !== types.SET_ID) {
    throw new SanaScanError();
  }

  if (action.payload.id === undefined) {
    throw new SanaScanError();
  }

  return action.payload.id;
};

const idReducer = (state: number | null | undefined, action: Action) => {
  if (action.type === types.SET_ID) {
    return setId(state, action);
  }

  if (state === undefined) {
    return initialState.id;
  }

  return state;
};

const resultReducer = (state: string | undefined, action: Action) => {
  if (state === undefined) {
    return initialState.result;
  }

  switch (action.type) {
    case types.SET_RESULT:
      return action.payload.content;

    default:
      return state;
  }
};

export const reducer = combineReducers({
  id: idReducer,
  result: resultReducer,
});
