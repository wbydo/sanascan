import {Action} from "./actions";
import CharacterBoard from "./CharacterBoard";
import {MAX_COLUMN_INDEX} from "./CharacterBoard";
import { INCREMENT } from "./types";
import SanaScanError from "./error";

export interface State {
  activeColumn: number;
}

const initialState: State = {
  activeColumn: 0,
};

const increment = (state: State, action: Action) => {
  if (action.type !== INCREMENT) {
    throw new SanaScanError();
  }

  if (state.activeColumn === MAX_COLUMN_INDEX) {
    return initialState;
  }
  return {activeColumn: state.activeColumn + 1};
};

const reducer = (state: State | undefined, action: Action) => {
  if (!state) {
    return initialState;
  }

  if (action.type === INCREMENT) {
    return increment(state, action);
  }
  return state;
};

export default reducer;
