import * as actions from "./actions";
import * as types from "./types";

import { CursolState } from "../..";

import { Action as _Action } from "../../util";

import { MAX_COLUMN_INDEX, MAX_ROW_INDEX } from "../../../constant";

export type Action = _Action<typeof actions>;

const initialState: CursolState = {
  activeColumn: 0,
  activeRow: 0,
  direction: "column",
  mode: "proposal",
};

const incrementColumn = (state: Exclude<CursolState, {direction: "row"}>): CursolState => {
  if (state.activeColumn >= MAX_COLUMN_INDEX) {
    return {
      ...state,
      activeColumn: 0,
    };
  } else {
    return {
      ...state,
      activeColumn: state.activeColumn + 1,
    };
  }
};

const incrementRow = (state: Extract<CursolState, {direction: "row"}>): CursolState => {
  if (state.activeRow >= MAX_ROW_INDEX) {
    return {
      ...state,
      activeRow: 0,
    };
  } else {
    return {
      ...state,
      activeRow: state.activeRow + 1,
    };
  }
};

const incrementInNormalMode = (state: Extract<CursolState, {mode: "normal"}>): CursolState => {
  if (state.direction === "column") {
    return incrementColumn(state);
  } else {
    return incrementRow(state);
  }
};

const increment = (state: CursolState): CursolState => {
  if (state.mode === "proposal") {
    return incrementColumn(state);
  } else {
    return incrementInNormalMode(state);
  }
};

const setMode = (state: CursolState, action: ReturnType<typeof actions.setMode>): CursolState => {
  if (action.payload.mode === "proposal") {
    return {
      ...state,
      direction: "column",
      mode: action.payload.mode,
    };
  } else {
    return {
      ...state,
      mode: action.payload.mode,
    };
  }
};

const setDirection = (state: CursolState, action: ReturnType<typeof actions.setDirection>): CursolState => {
  if (state.mode === "proposal") {
    return state;
  } else if (action.payload.direction === "row") {
    return {
      ...state,
      direction: action.payload.direction,
    };
  } else {
    return {
      ...state,
      direction: action.payload.direction,
    };
  }
};

const reset = (state: CursolState): CursolState => {
  return {
    ...state,
    activeColumn: 0,
    activeRow: 0,
  };
};

export const reducer = (state: CursolState | undefined, action: Action): CursolState => {
  if (state === undefined) {
    return initialState;
  }

  switch (action.type) {
    case (types.SET_MODE):
      return setMode(state, action);

    case (types.INCREMENT):
      return increment(state);

    case (types.SET_DIRECTION):
      return setDirection(state, action);

    case (types.RESET):
      return reset(state);

    default:
      return state;
  }
};
