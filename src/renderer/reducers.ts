import {Action} from "./actions";
import CharacterBoard from "./CharacterBoard";
import {MAX_COLUMN_INDEX} from "./CharacterBoard";
import * as types from "./types";
import SanaScanError from "./error";

export interface State {
  activeColumn: number;
}

const initialState: State = {
  activeColumn: 0,
};

type Reducer = (state: State | undefined, action: Action) => State;
type NonNullableReducer = (state: State, action: Action) => State;

const increment: NonNullableReducer = (state, action) => {
  if (action.type !== types.INCREMENT) {
    throw new SanaScanError();
  }

  if (state.activeColumn === MAX_COLUMN_INDEX) {
    return initialState;
  }
  return {activeColumn: state.activeColumn + 1};
};

const reducer: Reducer = (state, action) => {
  if (!state) {
    return initialState;
  }

  if (action.type === types.INCREMENT) {
    return increment(state, action);
  }
  return state
};

export default reducer;
