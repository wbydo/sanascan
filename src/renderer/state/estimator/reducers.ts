import { combineReducers } from "redux";

import * as actions from "./actions";
import * as types from "./types";

import SanaScanError from "../../error";

interface RootState {
  id: number | null;
}

const initialState: RootState = {
  id: null,
};

const setId = (state: number | null, action: actions.Action) => {
  if (action.type !== types.SET_ID) {
    throw new SanaScanError();
  }

  if (action.payload.id === undefined) {
    throw new SanaScanError();
  }

  return action.payload.id;
};

const idReducer = (state: number | null | undefined, action: actions.Action) => {
  if (state === undefined) {
    return initialState.id;
  }

  if (action.type === types.SET_ID) {
    return setId(state, action);
  }
  return state;
};

const reducer = combineReducers({
  id: idReducer,
});

export default reducer;
